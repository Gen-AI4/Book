from typing import List, Dict, Any, AsyncGenerator
import openai
from openai import OpenAI
from backend.config import settings
import logging
import asyncio
import time
import random
from backend.utils import get_system_prompt

logger = logging.getLogger(__name__)


class OpenAIService:
    def __init__(self):
        # Determine which API to use based on available keys
        if settings.openrouter_api_key:
            # Use OpenRouter
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=settings.openrouter_api_key,
            )
            self.model = settings.openrouter_model
            self.is_openrouter = True
        elif settings.openai_api_key:
            # Use OpenAI
            self.client = OpenAI(api_key=settings.openai_api_key)
            self.model = settings.openai_model
            self.is_openrouter = False
        else:
            raise ValueError("No API key available - either OPENAI_API_KEY or OPENROUTER_API_KEY must be set in environment variables")

    def generate_response(self, system_prompt: str, user_message: str, history: List[Dict[str, str]] = None, max_retries: int = 5) -> str:
        """
        Generate a response using OpenAI or OpenRouter API with the provided context
        """
        for attempt in range(max_retries):
            try:
                # Prepare the messages for the API call
                messages = [{"role": "system", "content": system_prompt}]

                # Add conversation history if provided
                if history:
                    for msg in history:
                        role = msg.get("role", "user")
                        content = msg.get("content", "")
                        if role in ["user", "assistant", "system"]:
                            messages.append({"role": role, "content": content})

                # Add the current user message
                messages.append({"role": "user", "content": user_message})

                # Call the appropriate API
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000
                )

                return response.choices[0].message.content
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Error calling {'OpenRouter' if self.is_openrouter else 'OpenAI'} API (attempt {attempt + 1}): {error_msg}")

                # Check if it's a quota/429 error and apply longer backoff
                if "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                    # For quota/429 errors, use longer exponential backoff
                    # Use a more conservative approach with jitter to avoid thundering herd
                    base_wait = (2 ** attempt) * 5  # Start with 5 seconds and exponential backoff
                    jitter = random.uniform(0, 1)  # Add jitter to avoid synchronized retries
                    wait_time = min(120, base_wait + jitter)  # Max 120 seconds
                    logger.warning(f"Rate limit or quota error, waiting {wait_time:.2f} seconds before retry (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(wait_time)
                elif attempt == max_retries - 1:  # Last attempt
                    logger.error(f"Failed to generate response after {max_retries} attempts")
                    raise
                else:
                    # For other errors, use standard backoff with jitter
                    base_wait = 2 ** attempt
                    jitter = random.uniform(0, 1)
                    wait_time = base_wait + jitter
                    time.sleep(wait_time)

        raise Exception(f"Failed to generate response after {max_retries} attempts")

    async def generate_streaming_response(self, system_prompt: str, user_message: str,
                                         history: List[Dict[str, str]] = None, max_retries: int = 5) -> AsyncGenerator[str, None]:
        """
        Generate a streaming response using OpenAI or OpenRouter API
        """
        for attempt in range(max_retries):
            try:
                # Prepare the messages for the API call
                messages = [{"role": "system", "content": system_prompt}]

                # Add conversation history if provided
                if history:
                    for msg in history:
                        role = msg.get("role", "user")
                        content = msg.get("content", "")
                        if role in ["user", "assistant", "system"]:
                            messages.append({"role": role, "content": content})

                # Add the current user message
                messages.append({"role": "user", "content": user_message})

                # Call the appropriate API with streaming
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000,
                    stream=True
                )

                # Yield each chunk as it arrives
                async for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
                return  # Success, exit the retry loop
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Error calling {'OpenRouter' if self.is_openrouter else 'OpenAI'} API for streaming (attempt {attempt + 1}): {error_msg}")

                # Check if it's a quota/429 error and apply longer backoff
                if "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                    # For quota/429 errors, use longer exponential backoff with jitter
                    base_wait = (2 ** attempt) * 5  # Start with 5 seconds and exponential backoff
                    jitter = random.uniform(0, 1)  # Add jitter to avoid synchronized retries
                    wait_time = min(120, base_wait + jitter)  # Max 120 seconds
                    logger.warning(f"Rate limit or quota error, waiting {wait_time:.2f} seconds before retry (attempt {attempt + 1}/{max_retries})...")
                    await asyncio.sleep(wait_time)
                elif attempt == max_retries - 1:  # Last attempt
                    logger.error(f"Failed to generate streaming response after {max_retries} attempts")
                    raise
                else:
                    # For other errors, use standard backoff with jitter
                    base_wait = 2 ** attempt
                    jitter = random.uniform(0, 1)
                    wait_time = base_wait + jitter
                    await asyncio.sleep(wait_time)

        raise Exception(f"Failed to generate streaming response after {max_retries} attempts")
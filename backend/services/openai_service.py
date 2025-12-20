from typing import List, Dict, Any, AsyncGenerator
import openai
from backend.config import settings
import logging
import asyncio
import time
from backend.utils import get_system_prompt

logger = logging.getLogger(__name__)


class OpenAIService:
    def __init__(self):
        openai.api_key = settings.openai_api_key
        self.model = settings.openai_model

    def generate_response(self, system_prompt: str, user_message: str, history: List[Dict[str, str]] = None, max_retries: int = 3) -> str:
        """
        Generate a response using OpenAI API with the provided context
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

                # Call the OpenAI API
                response = openai.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000
                )

                return response.choices[0].message.content
            except Exception as e:
                logger.error(f"Error calling OpenAI API (attempt {attempt + 1}): {str(e)}")
                if attempt == max_retries - 1:  # Last attempt
                    raise
                # Wait before retrying (exponential backoff)
                time.sleep(2 ** attempt)

        raise Exception(f"Failed to generate response after {max_retries} attempts")

    async def generate_streaming_response(self, system_prompt: str, user_message: str,
                                         history: List[Dict[str, str]] = None, max_retries: int = 3) -> AsyncGenerator[str, None]:
        """
        Generate a streaming response using OpenAI API
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

                # Call the OpenAI API with streaming
                response = await openai.chat.completions.create(
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
                logger.error(f"Error calling OpenAI API for streaming (attempt {attempt + 1}): {str(e)}")
                if attempt == max_retries - 1:  # Last attempt
                    raise
                # Wait before retrying (exponential backoff)
                await asyncio.sleep(2 ** attempt)

        raise Exception(f"Failed to generate streaming response after {max_retries} attempts")
from typing import List, Dict
from openai import OpenAI
from backend.config import settings
import logging
import time

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        # Check for API Key
        if not settings.openrouter_api_key:
            logger.error("No OpenRouter API key available")
            raise ValueError("OPENROUTER_API_KEY must be set in environment variables")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key,
        )
        self.model = settings.openrouter_model
        logger.info("OpenAIService initialized with OpenRouter")

    def get_chat_completion(self, messages: List[Dict[str, str]], max_retries: int = 3) -> str:
        """
        Generates a chat completion. 
        Crucial: This method name matches what ChatService calls.
        """
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000
                )
                return response.choices[0].message.content

            except Exception as e:
                logger.error(f"Error calling API (attempt {attempt + 1}): {e}")
                if attempt == max_retries - 1:
                    raise e
                time.sleep(1)
        
        return "Error: Failed to generate response."
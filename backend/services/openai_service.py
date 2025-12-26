from openai import OpenAI
import logging
import os
# Import settings directly
from backend.config import settings

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        # Initialize OpenRouter client
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key,
        )
        self.model = settings.openrouter_model

    def get_chat_completion(self, messages, model=None, temperature=0.7, max_tokens=1000):
        """
        Generates a chat completion using OpenRouter/OpenAI.
        """
        try:
            target_model = model or self.model
            
            response = self.client.chat.completions.create(
                model=target_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error in OpenAI service: {str(e)}")
            raise e
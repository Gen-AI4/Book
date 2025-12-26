from typing import List, Dict, Any
import logging
from backend.services.context_retrieval_service import ContextRetrievalService
from backend.services.openai_service import OpenAIService

logger = logging.getLogger(__name__)

# --- SYSTEM PROMPT ---
SYSTEM_PROMPT = """You are an expert Teaching Assistant for a comprehensive textbook on Physical AI & Humanoid Robotics.
Your goal is to help students understand complex concepts in robotics, sim-to-real transfer, embodied intelligence, and hardware integration.

Instructions:
1. Answer questions based STRICTLY on the provided context from the textbook.
2. If the answer is not found in the context, politely state that the information is not available in the provided course materials.
3. Be concise, academic, and encouraging.
4. Do not identify yourself as a "Physics" assistant; you are a "Physical AI & Robotics" assistant.
"""
# ---------------------

class ChatService:
    def __init__(self):
        self.context_service = ContextRetrievalService()
        self.openai_service = OpenAIService()

    # CRITICAL FIX: The 'async' keyword below fixes the "str object can't be awaited" error
    async def process_chat_request(self, message: Any, chat_history: List[Dict[str, str]] = None) -> str:
        try:
            # 1. SAFETY: Handle Object/Dict input to prevent validation errors
            query_text = ""
            if isinstance(message, str):
                query_text = message
            elif isinstance(message, dict):
                query_text = message.get("message") or message.get("content") or str(message)
            else:
                query_text = str(message)

            logger.info(f"Processing query: {query_text}")

            # 2. Retrieve Context
            context_results = self.context_service.retrieve_context(query_text)
            context_block = self.context_service.construct_context_block(context_results)

            # 3. Build Messages
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            
            # Add History
            if chat_history:
                # Ensure history is a clean list of dicts
                clean_history = [msg for msg in chat_history if isinstance(msg, dict)]
                messages.extend(clean_history[-4:])

            # 4. Add User Query + Context
            user_content = f"""
            Context:
            {context_block}
            
            Question: {query_text}
            """
            messages.append({"role": "user", "content": user_content})

            # 5. Get Response
            response = self.openai_service.get_chat_completion(messages)
            
            return response

        except Exception as e:
            logger.error(f"CRITICAL ERROR in process_chat_request: {str(e)}")
            return "I apologize, but I encountered an internal error. Please check the logs."
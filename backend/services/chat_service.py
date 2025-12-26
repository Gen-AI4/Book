from typing import List, Dict, Any, Optional
import logging
from backend.services.context_retrieval_service import ContextRetrievalService
from backend.services.openai_service import OpenAIService

logger = logging.getLogger(__name__)

# --- UPDATED SYSTEM PROMPT ---
SYSTEM_PROMPT = """You are an expert Teaching Assistant for a comprehensive textbook on Physical AI & Humanoid Robotics.
Your goal is to help students understand complex concepts in robotics, sim-to-real transfer, embodied intelligence, and hardware integration.

Instructions:
1. Answer questions based STRICTLY on the provided context from the textbook.
2. If the answer is not found in the context, politely state that the information is not available in the provided course materials. Do not make up answers.
3. Be concise, academic, and encouraging.
4. When explaining technical terms (like 'Zero-Shot Transfer', 'Domain Randomization', or 'Sim-to-Real'), provide clear definitions from the text.
5. Do not identify yourself as a "Physics" assistant; you are a "Physical AI & Robotics" assistant.
"""
# -----------------------------

class ChatService:
    def __init__(self):
        self.context_service = ContextRetrievalService()
        self.openai_service = OpenAIService()

    def generate_response(self, message: str, chat_history: List[Dict[str, str]] = None) -> str:
        """
        Generate a response using RAG (Retrieval Augmented Generation)
        """
        try:
            # 1. Retrieve relevant context
            context_results = self.context_service.retrieve_context(message)
            context_block = self.context_service.construct_context_block(context_results)

            # 2. Prepare messages for the LLM
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
            ]

            # Add chat history if available (optional, for context)
            if chat_history:
                for msg in chat_history[-4:]: # Keep last 4 messages for context window
                    messages.append(msg)

            # 3. Add the user's current query with the retrieved context
            user_content = f"""
            Context information is below.
            ---------------------
            {context_block}
            ---------------------
            Given the context information and not prior knowledge, answer the query.
            Query: {message}
            """
            
            messages.append({"role": "user", "content": user_content})

            # 4. Generate response using OpenAIService
            response = self.openai_service.get_chat_completion(messages)
            
            return response

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I apologize, but I encountered an error while processing your request. Please try again."
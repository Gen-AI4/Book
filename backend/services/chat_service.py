from typing import List, Dict, Any, AsyncGenerator
from fastapi import HTTPException
import logging
from datetime import datetime

from backend.models import ChatRequest, ChatResponse
from backend.services.context_retrieval_service import ContextRetrievalService
from backend.services.openai_service import OpenAIService

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.context_service = ContextRetrievalService()
        self.openai_service = OpenAIService()

    async def process_chat_request(self, request: ChatRequest) -> ChatResponse:
        """
        Process a chat request by retrieving context and generating a response
        """
        try:
            # Validate message
            if not request.message:
                raise HTTPException(status_code=400, detail="Message cannot be empty")

            # Retrieve context
            try:
                context_items = self.context_service.retrieve_context(
                    query=request.message,
                    top_k=5,
                    min_score=0.3
                )
            except Exception as context_error:
                logger.warning(f"Context retrieval failed: {str(context_error)}, proceeding without context")
                context_items = []

            # Construct context block
            context_block = self.context_service.construct_context_block(context_items or [])

            # Build system prompt
            system_prompt = (
                f"You are a Physical AI Teaching Assistant. Use the provided context to answer. If unsure or if the question is outside the scope of the provided context, clearly state that you can only answer questions related to the textbook content.\n\n{context_block}"
                if context_block else
                "You are a Physical AI Teaching Assistant. You can only answer questions related to the textbook content. No general knowledge questions can be answered. If the user asks a question not related to the textbook, politely explain that you can only help with physics concepts from the textbook."
            )

            # Ensure history exists
            history = getattr(request, "history", []) or []

            # Generate response
            try:
                response_text = self.openai_service.generate_response(
                    system_prompt=system_prompt,
                    user_message=request.message,
                    history=history
                )
            except Exception as openai_error:
                error_msg = str(openai_error)
                logger.exception(f"OpenAI API call failed: {str(openai_error)}")

                # Check if it's a quota/429 error and provide more specific message
                if "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                    response_text = "I'm sorry, but I've reached my API usage limits. Please try again later or check back soon."
                else:
                    response_text = "I'm sorry, but I'm currently unable to process your request. Please try again later."

            # Determine if context was retrieved
            context_retrieved = len(context_items) > 0 and bool(context_block)
            sources = [item.get("source", "") for item in context_items if item.get("source")]

            # If no context was retrieved, ensure the response is restricted to textbook content
            if not context_retrieved:
                # Replace general knowledge responses with a proper restriction message
                if ("i don't know" not in response_text.lower() and
                    "i do not know" not in response_text.lower() and
                    "i cannot answer" not in response_text.lower() and
                    "i can only answer" not in response_text.lower() and
                    "i can only help" not in response_text.lower() and
                    "outside the scope" not in response_text.lower()):
                    # This appears to be a general knowledge response, replace with restriction message
                    response_text = "I'm a Physics AI Teaching Assistant. I can only answer questions related to the textbook content. I cannot answer general knowledge questions that are outside the scope of the provided physics materials."

            return ChatResponse(
                response=response_text,
                context_retrieved=context_retrieved,
                sources=sources,
                timestamp=datetime.now()
            )

        except HTTPException:
            # Re-raise HTTPExceptions (e.g., message validation)
            raise
        except Exception as e:
            logger.exception(f"Unexpected error processing chat request: {str(e)}")
            raise HTTPException(status_code=500, detail="Unexpected error processing chat request")

    async def process_chat_request_streaming(self, request: ChatRequest) -> AsyncGenerator[str, None]:
        """
        Process a chat request and return a streaming response
        """
        try:
            if not request.message:
                raise HTTPException(status_code=400, detail="Message cannot be empty")

            # Retrieve context safely
            try:
                context_items = self.context_service.retrieve_context(
                    query=request.message,
                    top_k=5,
                    min_score=0.3
                )
            except Exception as context_error:
                logger.warning(f"Context retrieval failed: {str(context_error)}, proceeding without context")
                context_items = []

            context_block = self.context_service.construct_context_block(context_items or [])

            system_prompt = (
                f"You are a Physical AI Teaching Assistant. Use the provided context to answer. If unsure or if the question is outside the scope of the provided context, clearly state that you can only answer questions related to the textbook content.\n\n{context_block}"
                if context_block else
                "You are a Physical AI Teaching Assistant. You can only answer questions related to the textbook content. No general knowledge questions can be answered. If the user asks a question not related to the textbook, politely explain that you can only help with physics concepts from the textbook."
            )

            history = getattr(request, "history", []) or []

            # Determine if context was retrieved
            context_retrieved = len(context_items) > 0 and bool(context_block)

            # Generate streaming response
            try:
                # If context was not retrieved, we can't do streaming restriction effectively
                # So we'll rely on the system prompt to guide the response
                async for chunk in self.openai_service.generate_streaming_response(
                    system_prompt=system_prompt,
                    user_message=request.message,
                    history=history
                ):
                    yield chunk
            except Exception as openai_error:
                error_msg = str(openai_error)
                logger.exception(f"OpenAI streaming API call failed: {str(openai_error)}")

                # Check if it's a quota/429 error and provide more specific message
                if "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                    yield "I'm sorry, but I've reached my API usage limits. Please try again later or check back soon."
                else:
                    yield "I'm sorry, but I'm currently unable to process your request in streaming mode."

        except HTTPException:
            raise
        except Exception as e:
            logger.exception(f"Unexpected error processing streaming chat request: {str(e)}")
            raise HTTPException(status_code=500, detail="Unexpected error processing streaming chat request")

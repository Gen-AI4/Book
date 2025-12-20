from typing import List, Dict, Any, AsyncGenerator
from fastapi import HTTPException
import logging

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
            # Retrieve context from Qdrant based on the user's message
            try:
                context_items = self.context_service.retrieve_context(
                    query=request.message,
                    top_k=5,
                    min_score=0.3
                )
            except Exception as context_error:
                logger.warning(f"Context retrieval failed: {str(context_error)}, proceeding without context")
                context_items = []

            # Construct context block as specified in implementation directives
            context_block = self.context_service.construct_context_block(context_items)

            # Create system prompt with context (or without if context retrieval failed)
            system_prompt = f"You are a Physical AI Teaching Assistant. Use the provided context to answer. If unsure, admit it.\n\n{context_block}" if context_block else "You are a Physical AI Teaching Assistant. Answer the user's question to the best of your ability."

            # Generate response using OpenAI
            try:
                response_text = self.openai_service.generate_response(
                    system_prompt=system_prompt,
                    user_message=request.message,
                    history=request.history or []
                )
            except Exception as openai_error:
                logger.error(f"OpenAI API call failed: {str(openai_error)}")
                # Provide a fallback response if OpenAI call fails
                response_text = "I'm sorry, but I'm currently unable to process your request. Please try again later."

            # Determine if context was retrieved
            context_retrieved = len(context_items) > 0 and bool(context_block)
            sources = [item.get("source", "") for item in context_items if item.get("source")]

            # Create and return the response
            return ChatResponse(
                response=response_text,
                context_retrieved=context_retrieved,
                sources=sources
            )
        except Exception as e:
            logger.error(f"Error processing chat request: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing chat request")

    async def process_chat_request_streaming(self, request: ChatRequest) -> AsyncGenerator[str, None]:
        """
        Process a chat request and return a streaming response
        """
        try:
            # Retrieve context from Qdrant based on the user's message
            context_items = self.context_service.retrieve_context(
                query=request.message,
                top_k=5,
                min_score=0.3
            )

            # Construct context block as specified in implementation directives
            context_block = self.context_service.construct_context_block(context_items)

            # Create system prompt with context
            system_prompt = f"You are a Physical AI Teaching Assistant. Use the provided context to answer. If unsure, admit it.\n\n{context_block}"

            # Generate streaming response using OpenAI
            async for chunk in self.openai_service.generate_streaming_response(
                system_prompt=system_prompt,
                user_message=request.message,
                history=request.history or []
            ):
                yield chunk
        except Exception as e:
            logger.error(f"Error processing streaming chat request: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing streaming chat request")
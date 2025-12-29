#!/usr/bin/env python3
"""
Simple test to verify the chat functionality is working with the ingested content.
"""
import asyncio
import sys
import os

# Add the parent directory to the path for proper imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from backend.models import ChatRequest
from backend.services.chat_service import ChatService

async def test_chat_functionality():
    """Test the chat functionality with a query about hardware requirements."""
    print("Testing chat functionality with ingested content...")

    # Initialize chat service
    chat_service = ChatService()

    # Create a test request
    test_request = ChatRequest(
        message="What are the hardware requirements mentioned in the textbook?",
        session_id="test-session-123"
    )

    try:
        # Process the chat request
        response = await chat_service.process_chat_request(test_request)

        print(f"[SUCCESS] Chat response received successfully")
        print(f"Response: {response.response[:200]}...")
        print(f"Context retrieved: {response.context_retrieved}")
        print(f"Sources: {response.sources}")

        if response.context_retrieved:
            print("[SUCCESS] Chat system successfully accessed ingested book content!")
            return True
        else:
            print("[WARNING] Chat system did not retrieve context from book content")
            return False

    except Exception as e:
        print(f"[ERROR] Error during chat functionality test: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_chat_functionality())
    if success:
        print("\n[SUCCESS] Chat functionality test PASSED - book content is accessible")
    else:
        print("\n[ERROR] Chat functionality test FAILED")
    sys.exit(0 if success else 1)
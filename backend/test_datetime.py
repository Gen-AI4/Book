#!/usr/bin/env python3
"""
Test script to check the datetime error specifically
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from backend.models import ChatResponse
from backend.services.chat_service import ChatService
from backend.models import ChatRequest

def test_datetime_in_model():
    """Test creating ChatResponse with datetime"""
    print("Testing datetime usage in models...")

    try:
        # Test creating ChatResponse with timestamp
        response = ChatResponse(
            response="Test response",
            context_retrieved=True,
            sources=["source1"],
            timestamp=datetime.now()
        )
        print(f"✅ Created ChatResponse successfully: {response.timestamp}")
        return True
    except Exception as e:
        print(f"❌ Error creating ChatResponse: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_datetime_in_field():
    """Test datetime field creation"""
    print("\nTesting datetime field creation...")

    try:
        # Test creating ChatResponse without specifying timestamp (should use default_factory)
        response = ChatResponse(
            response="Test response",
            context_retrieved=True,
            sources=["source1"]
        )
        print(f"✅ Created ChatResponse with default timestamp: {response.timestamp}")
        return True
    except Exception as e:
        print(f"❌ Error creating ChatResponse with default timestamp: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chat_service():
    """Test basic chat service functionality"""
    print("\nTesting ChatService initialization...")

    try:
        service = ChatService()
        print("✅ ChatService initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Error initializing ChatService: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing datetime-related functionality...")
    print("=" * 50)

    test1 = test_datetime_in_model()
    test2 = test_datetime_in_field()
    test3 = test_chat_service()

    print("=" * 50)
    print("Test Summary:")
    print(f"ChatResponse with explicit timestamp: {'✅ OK' if test1 else '❌ ERROR'}")
    print(f"ChatResponse with default timestamp: {'✅ OK' if test2 else '❌ ERROR'}")
    print(f"ChatService initialization: {'✅ OK' if test3 else '❌ ERROR'}")
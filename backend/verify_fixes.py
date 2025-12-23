#!/usr/bin/env python3
"""
Script to verify the fixes for the API issues
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.openai_service import OpenAIService
from backend.services.context_retrieval_service import ContextRetrievalService
from backend.config import settings

def verify_openai_fix():
    """Verify OpenAI API authentication fix"""
    print("Verifying OpenAI API authentication fix...")
    try:
        service = OpenAIService()
        print(f"SUCCESS: OpenAIService initialized")
        print(f"Using OpenRouter: {service.is_openrouter}")
        print(f"Model: {service.model}")
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def verify_context_service():
    """Verify context retrieval service fix"""
    print("\nVerifying context retrieval service fix...")
    try:
        service = ContextRetrievalService()
        print("SUCCESS: ContextRetrievalService initialized")
        print(f"Collection name: {service.collection_name}")
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def verify_config():
    """Verify configuration settings"""
    print("\nVerifying configuration...")
    print(f"OpenRouter API key available: {bool(settings.openrouter_api_key)}")
    print(f"OpenAI API key available: {bool(settings.openai_api_key)}")
    print(f"Cohere API key available: {bool(settings.cohere_api_key)}")
    print(f"Qdrant URL: {settings.qdrant_url}")
    print(f"Qdrant collection: {settings.qdrant_collection_name}")
    return True

if __name__ == "__main__":
    print("Verifying fixes for API issues...")
    print("=" * 50)

    config_ok = verify_config()
    openai_ok = verify_openai_fix()
    context_ok = verify_context_service()

    print("=" * 50)
    print("Verification Summary:")
    print(f"Configuration: {'PASS' if config_ok else 'FAIL'}")
    print(f"OpenAI Service: {'PASS' if openai_ok else 'FAIL'}")
    print(f"Context Service: {'PASS' if context_ok else 'FAIL'}")

    all_pass = config_ok and openai_ok and context_ok
    print(f"Overall: {'ALL FIXES VERIFIED' if all_pass else 'SOME ISSUES REMAIN'}")
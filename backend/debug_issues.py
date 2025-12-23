#!/usr/bin/env python3
"""
Debug script to check what's happening with embeddings and API calls
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.context_retrieval_service import ContextRetrievalService
from backend.services.openai_service import OpenAIService
from backend.config import settings

def debug_cohere_embeddings():
    """Debug the Cohere embedding generation"""
    print("Debugging Cohere embeddings...")
    try:
        service = ContextRetrievalService()

        # Test the exact same call that's failing
        test_query = "test query"
        response = service.cohere_client.embed(
            texts=[test_query],
            model="embed-english-v3.0",
            input_type="search_query"
        )
        query_embedding = response.embeddings[0]

        print(f"Query embedding dimension: {len(query_embedding)}")
        print(f"Expected: 1024, Actual: {len(query_embedding)}")

        if len(query_embedding) != 1024:
            print(f"❌ PROBLEM: Cohere is generating {len(query_embedding)}-dimensional vectors instead of 1024!")
        else:
            print("✅ Cohere is generating correct 1024-dimensional vectors")

        return len(query_embedding) == 1024

    except Exception as e:
        print(f"❌ Error in Cohere embedding: {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_openrouter_service():
    """Debug the OpenRouter service configuration"""
    print("\nDebugging OpenRouter service...")
    try:
        service = OpenAIService()

        print(f"Using OpenRouter: {service.is_openrouter}")
        print(f"Model: {service.model}")

        if service.is_openrouter:
            print("✅ OpenAIService is configured to use OpenRouter")
        else:
            print("❌ OpenAIService is not configured to use OpenRouter")

        # Check the client configuration
        print(f"Client base URL: {getattr(service.client, '_base_url', 'Not available')}")

        return True

    except Exception as e:
        print(f"❌ Error in OpenRouter service: {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_config():
    """Debug the configuration"""
    print("\nDebugging configuration...")
    print(f"OpenRouter API Key available: {bool(settings.openrouter_api_key)}")
    print(f"OpenRouter Model: {settings.openrouter_model}")

    if settings.openrouter_api_key:
        print("✅ OpenRouter API key is available")
        return True
    else:
        print("❌ No OpenRouter API key available")
        return False

def main():
    print("Running debug checks...")
    print("=" * 50)

    config_ok = debug_config()
    cohere_ok = debug_cohere_embeddings()
    openrouter_ok = debug_openrouter_service()

    print("=" * 50)
    print("Debug Summary:")
    print(f"Configuration: {'✅ OK' if config_ok else '❌ ERROR'}")
    print(f"Cohere Embeddings: {'✅ OK' if cohere_ok else '❌ ERROR'}")
    print(f"OpenRouter Service: {'✅ OK' if openrouter_ok else '❌ ERROR'}")

    if not cohere_ok:
        print("\n🔍 The main issue appears to be with Cohere embeddings generating 768 dimensions instead of 1024!")
        print("This suggests either:")
        print("1. The Cohere API is returning different dimensions than expected")
        print("2. There's a different embedding service being used")
        print("3. The collection was created with wrong dimensions")

    return config_ok and cohere_ok and openrouter_ok

if __name__ == "__main__":
    main()
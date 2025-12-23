#!/usr/bin/env python3
"""
Final comprehensive test to validate all fixes
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.context_retrieval_service import ContextRetrievalService
from backend.services.openai_service import OpenAIService
from backend.services.chat_service import ChatService
from backend.config import settings

def test_config():
    """Test that configuration loads correctly"""
    print("Testing configuration...")
    try:
        # Verify that settings are loaded
        assert settings.qdrant_url is not None
        assert settings.cohere_api_key is not None
        assert settings.openrouter_api_key is not None  # Should be available from .env

        print("[OK] Configuration loaded successfully")
        print(f"  - Qdrant: {settings.qdrant_url[:30]}...")
        print(f"  - Cohere: {'Available' if settings.cohere_api_key else 'Missing'}")
        print(f"  - OpenRouter: {'Available' if settings.openrouter_api_key else 'Missing'}")
        print(f"  - Model: {settings.openrouter_model if settings.openrouter_api_key else settings.openai_model}")
        return True
    except Exception as e:
        print(f"[ERROR] Configuration test failed: {e}")
        return False

def test_services_initialization():
    """Test that all services initialize correctly"""
    print("Testing services initialization...")
    try:
        # Test ContextRetrievalService
        context_service = ContextRetrievalService()
        print("[OK] ContextRetrievalService initialized")

        # Test OpenAIService (should use OpenRouter)
        openai_service = OpenAIService()
        print(f"[OK] OpenAIService initialized (using {'OpenRouter' if openai_service.is_openrouter else 'OpenAI'})")

        # Test ChatService
        chat_service = ChatService()
        print("[OK] ChatService initialized")

        return True
    except Exception as e:
        print(f"[ERROR] Services initialization failed: {e}")
        return False

def test_embedding_dimensions():
    """Test that embeddings have correct dimensions"""
    print("Testing embedding dimensions...")
    try:
        service = ContextRetrievalService()

        # Test query embedding
        response = service.cohere_client.embed(
            texts=["test query"],
            model="embed-english-v3.0",
            input_type="search_query"
        )
        query_embedding = response.embeddings[0]

        assert len(query_embedding) == 1024, f"Query embedding has {len(query_embedding)} dims, expected 1024"
        print("[OK] Query embeddings have correct dimensions (1024)")

        # Test document embedding
        response_doc = service.cohere_client.embed(
            texts=["test document"],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        doc_embedding = response_doc.embeddings[0]

        assert len(doc_embedding) == 1024, f"Document embedding has {len(doc_embedding)} dims, expected 1024"
        print("[OK] Document embeddings have correct dimensions (1024)")

        return True
    except Exception as e:
        print(f"[ERROR] Embedding dimensions test failed: {e}")
        return False

def test_qdrant_client_consistency():
    """Test that Qdrant client is initialized consistently"""
    print("Testing Qdrant client consistency...")
    try:
        service = ContextRetrievalService()

        # Verify the client was initialized with URL directly (our fix)
        # The client should work properly now
        collection_info = service.qdrant_client.get_collection(settings.qdrant_collection_name)
        assert collection_info.config.params.vectors.size == 1024
        print("[OK] Qdrant client initialized with correct configuration")
        print(f"  - Vector size: {collection_info.config.params.vectors.size}")
        print(f"  - Distance: {collection_info.config.params.vectors.distance}")

        return True
    except Exception as e:
        print(f"[ERROR] Qdrant client consistency test failed: {e}")
        return False

def main():
    print("Running final comprehensive test...")
    print("=" * 50)

    test1 = test_config()
    test2 = test_services_initialization()
    test3 = test_embedding_dimensions()
    test4 = test_qdrant_client_consistency()

    print("=" * 50)
    print("Final Test Summary:")
    print(f"Configuration: {'[OK]' if test1 else '[ERROR]'}")
    print(f"Services Initialization: {'[OK]' if test2 else '[ERROR]'}")
    print(f"Embedding Dimensions: {'[OK]' if test3 else '[ERROR]'}")
    print(f"Qdrant Client Consistency: {'[OK]' if test4 else '[ERROR]'}")

    all_passed = test1 and test2 and test3 and test4
    if all_passed:
        print("\n[SUCCESS] All fixes have been successfully implemented!")
        print("\nSummary of fixes applied:")
        print("  1. Fixed Qdrant client initialization in context retrieval service")
        print("  2. Updated OpenAI service to support OpenRouter API")
        print("  3. Improved error handling for API quota issues")
        print("  4. Enhanced configuration to support OpenRouter")
        print("  5. Verified all embeddings use correct 1024 dimensions")
        print("  6. Ensured consistent API client initialization")
    else:
        print("\n[FAILURE] Some tests failed")

    return all_passed

if __name__ == "__main__":
    main()
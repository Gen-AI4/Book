#!/usr/bin/env python3
"""
Script to test the fixes for the application
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.context_retrieval_service import ContextRetrievalService
from backend.services.openai_service import OpenAIService
from backend.config import settings

def test_context_retrieval_service():
    """Test that the context retrieval service can be initialized properly"""
    print("Testing ContextRetrievalService initialization...")
    try:
        service = ContextRetrievalService()
        print("[OK] ContextRetrievalService initialized successfully")
        return True
    except Exception as e:
        print(f"[ERROR] ContextRetrievalService initialization failed: {e}")
        return False

def test_openai_service():
    """Test that the OpenAIService can be initialized properly"""
    print("Testing OpenAIService initialization...")
    try:
        service = OpenAIService()
        print("[OK] OpenAIService initialized successfully")
        return True
    except Exception as e:
        print(f"[ERROR] OpenAIService initialization failed: {e}")
        return False

def test_embedding_consistency():
    """Test that Cohere embeddings are generated with correct dimensions"""
    print("Testing Cohere embedding consistency...")
    try:
        service = ContextRetrievalService()

        # Test query embedding
        response = service.cohere_client.embed(
            texts=["test query"],
            model="embed-english-v3.0",
            input_type="search_query"
        )
        query_embedding = response.embeddings[0]

        if len(query_embedding) == 1024:
            print("[OK] Cohere query embeddings have correct dimensions (1024)")
        else:
            print(f"[ERROR] Cohere query embeddings have wrong dimensions: {len(query_embedding)}")
            return False

        # Test document embedding
        response_doc = service.cohere_client.embed(
            texts=["test document"],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        doc_embedding = response_doc.embeddings[0]

        if len(doc_embedding) == 1024:
            print("[OK] Cohere document embeddings have correct dimensions (1024)")
        else:
            print(f"[ERROR] Cohere document embeddings have wrong dimensions: {len(doc_embedding)}")
            return False

        return True
    except Exception as e:
        print(f"[ERROR] Cohere embedding test failed: {e}")
        return False

def main():
    print("Testing application fixes...")
    print("=" * 40)

    test1 = test_context_retrieval_service()
    test2 = test_openai_service()
    test3 = test_embedding_consistency()

    print("=" * 40)
    print("Test Summary:")
    print(f"Context Retrieval Service: {'[OK]' if test1 else '[ERROR]'}")
    print(f"OpenAI Service: {'[OK]' if test2 else '[ERROR]'}")
    print(f"Embedding Consistency: {'[OK]' if test3 else '[ERROR]'}")

    all_passed = test1 and test2 and test3
    print(f"Overall: {'[OK] All tests passed' if all_passed else '[ERROR] Some tests failed'}")

    return all_passed

if __name__ == "__main__":
    main()
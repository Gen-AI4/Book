#!/usr/bin/env python3
"""
Test script to check Cohere embedding dimensions
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.context_retrieval_service import ContextRetrievalService
from backend.config import settings
import cohere

def test_cohere_embeddings():
    """Test the exact embedding generation that's happening in the context retrieval service"""
    print("Testing Cohere embedding dimensions...")

    # Initialize Cohere client the same way as the service
    cohere_client = cohere.Client(settings.cohere_api_key)

    # Test query embedding (like in context retrieval)
    try:
        response = cohere_client.embed(
            texts=["test query"],
            model="embed-english-v3.0",
            input_type="search_query"  # This is important for v3 models
        )
        query_embedding = response.embeddings[0]
        print(f"Query embedding dimension: {len(query_embedding)}")
    except Exception as e:
        print(f"Error generating query embedding: {e}")
        return False

    # Test document embedding (like in ingestion)
    try:
        response_doc = cohere_client.embed(
            texts=["test document"],
            model="embed-english-v3.0",
            input_type="search_document"  # This is important for v3 models
        )
        doc_embedding = response_doc.embeddings[0]
        print(f"Document embedding dimension: {len(doc_embedding)}")
    except Exception as e:
        print(f"Error generating document embedding: {e}")
        return False

    # Check if dimensions are correct
    if len(query_embedding) == 1024 and len(doc_embedding) == 1024:
        print("✅ Cohere embeddings have correct dimensions (1024)")
        return True
    else:
        print(f"❌ Cohere embeddings have incorrect dimensions (query: {len(query_embedding)}, doc: {len(doc_embedding)})")
        return False

def test_context_service():
    """Test the actual context retrieval service"""
    print("\nTesting ContextRetrievalService...")
    try:
        service = ContextRetrievalService()

        # Test retrieval (this is where the error might occur)
        result = service.retrieve_context("test query", top_k=1, min_score=0.0)
        print(f"Context retrieval successful, got {len(result)} results")

        if result:
            print(f"First result score: {result[0]['score']}")

        return True
    except Exception as e:
        print(f"Error in context retrieval: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running embedding dimension tests...")
    print("=" * 50)

    # Test the embeddings
    embeddings_ok = test_cohere_embeddings()

    # Test the service
    service_ok = test_context_service()

    print("=" * 50)
    print("Test Summary:")
    print(f"Cohere Embeddings: {'✅ OK' if embeddings_ok else '❌ ERROR'}")
    print(f"Context Service: {'✅ OK' if service_ok else '❌ ERROR'}")
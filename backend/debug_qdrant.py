#!/usr/bin/env python3
"""
Debug script to test Qdrant API calls and identify the exact issue
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.context_retrieval_service import ContextRetrievalService
from backend.config import settings
from qdrant_client import QdrantClient
import cohere

def debug_qdrant():
    print("Debugging Qdrant connection and query...")

    # Test 1: Check if we can connect to Qdrant
    print("\n1. Testing Qdrant connection...")
    try:
        if settings.qdrant_api_key:
            client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
            )
        else:
            client = QdrantClient(url=settings.qdrant_url)

        print("[OK] Qdrant client initialized successfully")

        # Test if collection exists
        collection_info = client.get_collection(settings.qdrant_collection_name)
        print(f"[OK] Collection '{settings.qdrant_collection_name}' exists")
        print(f"  - Vector size: {collection_info.config.params.vectors.size}")
        print(f"  - Distance: {collection_info.config.params.vectors.distance}")

    except Exception as e:
        print(f"[ERROR] Qdrant connection error: {e}")
        return False

    # Test 2: Check Cohere embedding
    print("\n2. Testing Cohere embedding generation...")
    try:
        cohere_client = cohere.Client(settings.cohere_api_key)
        response = cohere_client.embed(
            texts=["test query"],
            model="embed-english-v3.0",
            input_type="search_query"
        )
        query_embedding = response.embeddings[0]
        print(f"[OK] Cohere embedding generated successfully with {len(query_embedding)} dimensions")

        if len(query_embedding) != 1024:
            print(f"[ERROR] Expected 1024 dimensions, got {len(query_embedding)}")
            return False

    except Exception as e:
        print(f"[ERROR] Cohere embedding error: {e}")
        return False

    # Test 3: Test the actual query that's failing
    print("\n3. Testing Qdrant query_points method...")
    try:
        # Try the query_points method with different parameter formats
        print("  Trying query_points with current parameters...")
        search_result = client.query_points(
            collection_name=settings.qdrant_collection_name,
            query=query_embedding,
            limit=1,
            with_payload=True
        )
        print(f"[OK] query_points succeeded, got {len(search_result.points)} results")

    except Exception as e:
        print(f"[ERROR] query_points failed: {e}")

        # Try with different parameter format
        try:
            print("  Trying with query_vector instead of query...")
            search_result = client.query_points(
                collection_name=settings.qdrant_collection_name,
                query_vector=query_embedding,  # Different parameter name
                limit=1,
                with_payload=True
            )
            print(f"[OK] query_points with query_vector succeeded, got {len(search_result.points)} results")
        except Exception as e2:
            print(f"[ERROR] query_points with query_vector also failed: {e2}")
            return False

    print("\n[OK] All tests passed!")
    return True

if __name__ == "__main__":
    success = debug_qdrant()
    if success:
        print("\nDebug completed successfully!")
    else:
        print("\nDebug failed!")
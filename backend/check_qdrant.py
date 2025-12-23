#!/usr/bin/env python3
"""
Script to check and fix the Qdrant collection configuration
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import settings
from qdrant_client import QdrantClient

def check_qdrant_collection():
    """Check the Qdrant collection configuration"""
    print("Checking Qdrant collection configuration...")

    # Initialize Qdrant client
    if settings.qdrant_api_key:
        client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
    else:
        client = QdrantClient(url=settings.qdrant_url)

    collection_name = settings.qdrant_collection_name

    try:
        # Get collection info
        collection_info = client.get_collection(collection_name)
        print(f"Collection '{collection_name}' exists")
        print(f"Vector configuration: {collection_info.config.params.vectors}")

        # Check if vector size is correct
        vector_size = collection_info.config.params.vectors.size
        print(f"Vector size: {vector_size}")

        if vector_size == 1024:
            print("✅ Vector size is correct (1024)")
            return True
        else:
            print(f"❌ Vector size is {vector_size}, expected 1024")
            return False

    except Exception as e:
        print(f"❌ Error checking collection: {e}")
        return False

if __name__ == "__main__":
    success = check_qdrant_collection()
    if not success:
        print("\nTo fix this issue, you may need to recreate the collection:")
        print("python -c \"from backend.init_db import create_collection_if_not_exists; create_collection_if_not_exists()\"")
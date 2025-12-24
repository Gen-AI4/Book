#!/usr/bin/env python3
"""
Script to completely recreate the Qdrant collection to ensure consistency
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import settings
from qdrant_client import QdrantClient
from qdrant_client.http import models

def recreate_collection():
    """Delete and recreate the collection to ensure clean state"""
    if settings.qdrant_api_key:
        client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
    else:
        client = QdrantClient(url=settings.qdrant_url)

    collection_name = settings.qdrant_collection_name

    try:
        # Delete the existing collection
        print(f"Deleting collection '{collection_name}'...")
        client.delete_collection(collection_name)
        print(f"Collection '{collection_name}' deleted.")
    except Exception as e:
        print(f"Collection '{collection_name}' may not have existed: {e}")

    # Create collection with correct configuration
    print(f"Creating collection '{collection_name}' with 1024 dimensions and Cosine distance...")
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=1024,  # Cohere embed-english-v3.0 produces 1024-dimensional vectors
            distance=models.Distance.COSINE
        )
    )
    print(f"Collection '{collection_name}' created successfully with correct configuration!")

    # Verify the creation
    collection_info = client.get_collection(collection_name)
    print(f"Verification - Collection vector size: {collection_info.config.params.vectors.size}")
    print(f"Verification - Collection distance: {collection_info.config.params.vectors.distance}")

if __name__ == "__main__":
    recreate_collection()
#!/usr/bin/env python3
"""
Script to verify that the vectors were stored correctly in Qdrant.
"""

import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv

# Load environment variables from backend directory
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

def verify_qdrant_storage():
    print("Verifying Qdrant storage...")

    # Initialize Qdrant client
    qdrant_host = os.getenv("QDRANT_HOST")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_host or not qdrant_api_key:
        raise ValueError("QDRANT_HOST and QDRANT_API_KEY must be set in environment variables")

    client = QdrantClient(
        url=qdrant_host,
        api_key=qdrant_api_key,
    )

    # Get collection info
    collection_name = "physical_ai_textbook"
    try:
        collection_info = client.get_collection(collection_name)
        print(f"Collection '{collection_name}' exists")
        print(f"  - Vector count: {collection_info.points_count}")
        print(f"  - Vector dimensions: {collection_info.config.params.vectors.size}")
        print(f"  - Distance: {collection_info.config.params.vectors.distance}")

        # Get a few sample points to verify content
        points = client.scroll(
            collection_name=collection_name,
            limit=2,
            with_payload=True,
            with_vectors=False
        )

        print(f"\nSample points retrieved: {len(points[0])}")
        for i, point in enumerate(points[0]):
            print(f"  Point {i+1}:")
            print(f"    ID: {point.id}")
            print(f"    Source URL: {point.payload.get('source_url', 'N/A')}")
            print(f"    Chapter Title: {point.payload.get('chapter_title', 'N/A')}")
            print(f"    Content Preview: {point.payload.get('content_preview', 'N/A')[:100]}...")

    except Exception as e:
        print(f"Error verifying Qdrant storage: {e}")
        return False

    print("\nQdrant storage verification completed successfully!")
    return True

if __name__ == "__main__":
    verify_qdrant_storage()
#!/usr/bin/env python3
"""
Script to verify Qdrant collection configuration
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qdrant_client import QdrantClient
from backend.config import settings
import urllib.parse

def verify_collection():
    """Verify the Qdrant collection configuration and test embeddings"""
    import cohere

    # Parse the URL to extract host, port, and protocol for proper initialization
    parsed_url = urllib.parse.urlparse(settings.qdrant_url)

    # Extract host and port
    host = parsed_url.hostname
    port = parsed_url.port if parsed_url.port else (443 if parsed_url.scheme == 'https' else 6333)
    is_https = parsed_url.scheme == 'https'

    # Initialize Qdrant client
    if settings.qdrant_api_key:
        client = QdrantClient(
            host=host,
            port=port,
            api_key=settings.qdrant_api_key,
            https=is_https
        )
    else:
        client = QdrantClient(
            host=host,
            port=port,
            https=is_https
        )

    collection_name = settings.qdrant_collection_name

    try:
        # Get collection info
        collection_info = client.get_collection(collection_name)
        print(f"Collection '{collection_name}' exists")
        print(f"Vector size: {collection_info.config.params.vectors.size}")
        print(f"Distance: {collection_info.config.params.vectors.distance}")

        # Check if the configuration is correct
        expected_size = 1024
        if collection_info.config.params.vectors.size == expected_size:
            print(f"Collection has correct vector size ({expected_size})")
        else:
            print(f"Collection has incorrect vector size ({collection_info.config.params.vectors.size}), expected {expected_size}")

    except Exception as e:
        print(f"Error getting collection info: {e}")
        print(f"Collection '{collection_name}' may not exist or there's a connection issue")
        return False

    # Test Cohere embedding generation
    try:
        cohere_client = cohere.Client(settings.cohere_api_key)

        # Test query embedding (like in context retrieval)
        test_query = "test query for verification"
        response = cohere_client.embed(
            texts=[test_query],
            model="embed-english-v3.0",
            input_type="search_query"
        )
        query_embedding = response.embeddings[0]
        print(f"Query embedding dimension: {len(query_embedding)}")

        # Test document embedding (like in ingestion)
        response_doc = cohere_client.embed(
            texts=[test_query],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        doc_embedding = response_doc.embeddings[0]
        print(f"Document embedding dimension: {len(doc_embedding)}")

        if len(query_embedding) == 1024 and len(doc_embedding) == 1024:
            print("Cohere embeddings have correct dimensions (1024)")
        else:
            print(f"Cohere embeddings have incorrect dimensions (query: {len(query_embedding)}, doc: {len(doc_embedding)})")

        # Test a simple query to the collection
        try:
            # Use the newer query_points API as in the context retrieval service
            search_result = client.query_points(
                collection_name=collection_name,
                query=query_embedding,
                limit=1,
                with_payload=True
            )
            print("Query to collection successful")
            print(f"Found {len(search_result.points)} results")
        except Exception as query_error:
            print(f"Query to collection failed: {query_error}")

        return True
    except Exception as e:
        print(f"Error testing Cohere embeddings: {e}")
        return False

if __name__ == "__main__":
    verify_collection()
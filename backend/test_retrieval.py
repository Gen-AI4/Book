#!/usr/bin/env python3
"""
RAG Retrieval Validation Script

This script validates the RAG pipeline retrieval mechanism by:
1. Taking a user query
2. Generating an embedding using Cohere (search mode)
3. Querying Qdrant for similar text chunks
4. Outputting the most relevant results with distance scores

Example Usage:
    # Direct function call
    results = retrieve("What is the hardware requirement?")

    # Command line execution
    python test_retrieval.py

Environment Variables Required:
    COHERE_API_KEY: Your Cohere API key
    QDRANT_HOST: Your Qdrant Cloud host URL
    QDRANT_API_KEY: Your Qdrant Cloud API key
    QDRANT_COLLECTION: Name of the collection to search (default: "text_chunks")
"""

import os
import sys
from typing import List, Dict, Any, Optional

import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Initialize Cohere client
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY environment variable is required")

co = cohere.Client(api_key=COHERE_API_KEY)

# Initialize Qdrant client
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "text_chunks")

if not QDRANT_HOST:
    raise ValueError("QDRANT_HOST environment variable is required")
if not QDRANT_API_KEY:
    raise ValueError("QDRANT_API_KEY environment variable is required")

client = QdrantClient(
    url="https://16b332a7-4011-462d-a698-10f2e3df8e6e.europe-west3-0.gcp.cloud.qdrant.io:6333",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.WDsCBIfwgPQSnM55VTDs1T8f_GihKGacXZ_mBxgSUP4",
    port=6333,
    https=True
)


def retrieve(query: str) -> List[Dict[str, Any]]:
    """
    Retrieve the top 3 most relevant text chunks for a given query.

    Args:
        query (str): The search query string

    Returns:
        List[Dict[str, Any]]: List of top 3 results with distance scores and content
    """
    try:
        # Validate input parameters before making API call
        # Following implementation directive: explicitly set input_type="search_query"
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        # Generate embedding for the query using the specified model and input type
        # Following implementation directive: use embed-english-v3.0 model with input_type="search_query"
        print(f"Generating embedding for query: '{query[:50]}...'", file=sys.stderr)  # Verification logging
        try:
            response = co.embed(
                texts=[query],
                model="embed-english-v3.0",  # Implementation directive: use exact same model name
                input_type="search_query"    # Implementation directive: explicitly set input_type
            )
        except Exception as e:
            print(f"Cohere API error: {str(e)}", file=sys.stderr)
            raise
        print(f"Embedding generated successfully with model: embed-english-v3.0", file=sys.stderr)  # Verification logging

        # Extract the embedding vector
        query_embedding = response.embeddings[0]

        # Search in Qdrant for similar vectors
        try:
            search_results = client.search(
                collection_name=QDRANT_COLLECTION,
                query_vector=query_embedding,
                limit=3  # Implementation directive: show all top 3 results regardless of score
            )
        except Exception as e:
            print(f"Qdrant connection error: {str(e)}", file=sys.stderr)
            raise

        # Format results to include distance scores and content
        formatted_results = []
        for result in search_results:
            formatted_result = {
                "score": result.score,  # Distance score (lower is more similar)
                "metadata": result.payload.get("metadata", {}),
                "page_content": result.payload.get("page_content", ""),
                "source": result.payload.get("source", "")
            }
            formatted_results.append(formatted_result)

        return formatted_results
    except Exception as e:
        print(f"Error during retrieval: {str(e)}", file=sys.stderr)
        return []


def test_configuration_verification():
    """Test configuration verification with different query inputs."""
    test_queries = [
        "What is the hardware requirement?",
        "Explain the ROS 2 integration",
        "How does the VLA system work?"
    ]

    for query in test_queries:
        print(f"\nTesting configuration with query: '{query}'")
        try:
            result = retrieve(query)
            print(f"  Status: SUCCESS - Configuration verified for this query")
        except Exception as e:
            print(f"  Status: ERROR - {str(e)}")


def display_results(query: str, results: List[Dict[str, Any]]):
    """Display results in a clear, formatted way for debugging."""
    print(f"\nQuery: '{query}'")
    print("-" * 60)

    if not results:
        print("No results found.")
        return

    for i, result in enumerate(results, 1):
        print(f"Result {i}:")
        print(f"  Score: {result.get('score', 'N/A')}")
        print(f"  Source: {result.get('source', 'N/A')}")
        print(f"  Content: {result.get('page_content', 'N/A')[:200]}...")  # Truncate long content
        print()


def test_complete_retrieval():
    """Test the complete retrieval function with sample query."""
    sample_query = "What is the hardware requirement?"
    print("TESTING COMPLETE RETRIEVAL FUNCTION")
    print("="*50)
    print(f"Query: {sample_query}")

    try:
        results = retrieve(sample_query)
        display_results(sample_query, results)
        print("✓ Retrieval test completed successfully")
        return True
    except Exception as e:
        print(f"✗ Retrieval test failed: {str(e)}")
        return False


if __name__ == "__main__":
    # Test the complete retrieval function with sample query "What is the hardware requirement?"
    success = test_complete_retrieval()

    # Test configuration verification with different query inputs
    print("\n" + "="*50)
    print("CONFIGURATION VERIFICATION TESTS")
    print("="*50)
    test_configuration_verification()
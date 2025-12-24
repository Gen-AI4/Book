#!/usr/bin/env python3
"""
Debug script to test what dimensions the Cohere API is actually returning
"""
import os
import cohere
from dotenv import load_dotenv

load_dotenv()

def test_cohere_embeddings():
    print("Testing Cohere embedding dimensions...")

    # Initialize Cohere client
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        print("ERROR: COHERE_API_KEY not found in environment")
        return

    co = cohere.Client(cohere_api_key)

    # Test different models and input types
    test_cases = [
        ("embed-english-v3.0", "search_query"),
        ("embed-english-v3.0", "search_document"),
        ("embed-multilingual-v3.0", "search_query"),
        ("embed-multilingual-v3.0", "search_document"),
    ]

    for model, input_type in test_cases:
        print(f"\nTesting model: {model}, input_type: {input_type}")
        try:
            response = co.embed(
                texts=["test query"],
                model=model,
                input_type=input_type
            )
            embedding = response.embeddings[0]
            print(f"  Dimensions: {len(embedding)}")

            if len(embedding) == 1024:
                print(f"  ✓ {model} with {input_type} produces 1024 dimensions")
            elif len(embedding) == 768:
                print(f"  ⚠ {model} with {input_type} produces 768 dimensions (this is the issue!)")
            else:
                print(f"  ? {model} with {input_type} produces {len(embedding)} dimensions")

        except Exception as e:
            print(f"  ERROR: {e}")

if __name__ == "__main__":
    test_cohere_embeddings()
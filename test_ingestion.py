#!/usr/bin/env python3
"""
Simple test script to verify the ingestion pipeline components work correctly.
This doesn't run the full pipeline but tests key functions individually.
"""

import os
from dotenv import load_dotenv
from backend.ingest import get_all_urls, extract_text_from_url, chunk_text, get_embeddings, save_chunk_to_qdrant

# Load environment variables
load_dotenv()

def test_ingestion_pipeline():
    print("Testing ingestion pipeline components...")

    # Test 1: URL extraction (using a known URL)
    print("\n1. Testing URL extraction...")
    try:
        urls = get_all_urls("https://the-book-iota.vercel.app/")
        print(f"   Found {len(urls)} URLs")
        if urls:
            print(f"   First URL: {urls[0]}")
    except Exception as e:
        print(f"   Error in URL extraction: {e}")

    # Test 2: Text extraction (using a sample URL)
    print("\n2. Testing text extraction...")
    sample_url = "https://the-book-iota.vercel.app/"  # Use the main page as sample
    try:
        text = extract_text_from_url(sample_url)
        print(f"   Extracted {len(text)} characters from {sample_url}")
        print(f"   Text preview: {text[:100]}...")
    except Exception as e:
        print(f"   Error in text extraction: {e}")

    # Test 3: Text chunking
    print("\n3. Testing text chunking...")
    sample_text = "This is a sample text for testing the chunking functionality. " * 50  # Make it long enough to chunk
    try:
        chunks = chunk_text(sample_text, chunk_size=100, overlap=20)
        print(f"   Split {len(sample_text)} characters into {len(chunks)} chunks")
        if chunks:
            print(f"   First chunk: {chunks[0][:50]}...")
    except Exception as e:
        print(f"   Error in text chunking: {e}")

    # Test 4: Embedding generation (only if API key is available)
    print("\n4. Testing embedding generation...")
    if os.getenv("COHERE_API_KEY"):
        try:
            sample_texts = ["This is a test sentence.", "Another test sentence for embedding."]
            embeddings = get_embeddings(sample_texts)
            print(f"   Generated {len(embeddings)} embeddings")
            if embeddings:
                print(f"   First embedding has {len(embeddings[0])} dimensions")
                print(f"   First few values: {embeddings[0][:5]}...")
        except Exception as e:
            print(f"   Error in embedding generation: {e}")
    else:
        print("   Skipping embedding test - COHERE_API_KEY not set")

    print("\nTest completed!")

if __name__ == "__main__":
    test_ingestion_pipeline()
#!/usr/bin/env python3
"""
Script to test API connectivity and health
"""
import os
import sys
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cohere
from qdrant_client import QdrantClient
from backend.config import settings

def test_cohere_connection():
    """Test Cohere API connection"""
    try:
        cohere_client = cohere.Client(settings.cohere_api_key)

        # Test embedding generation
        response = cohere_client.embed(
            texts=["test"],
            model="embed-english-v3.0",
            input_type="search_query"
        )

        if len(response.embeddings[0]) == 1024:
            print("[OK] Cohere API connection successful")
            return True
        else:
            print("[ERROR] Cohere API returned unexpected embedding dimensions")
            return False
    except Exception as e:
        print(f"[ERROR] Cohere API connection failed: {e}")
        return False

def test_qdrant_connection():
    """Test Qdrant connection"""
    try:
        # Initialize Qdrant client
        client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )

        # Test collection info
        collection_info = client.get_collection(settings.qdrant_collection_name)

        if collection_info.config.params.vectors.size == 1024:
            print("[OK] Qdrant connection successful")
            return True
        else:
            print("[ERROR] Qdrant collection has unexpected configuration")
            return False
    except Exception as e:
        print(f"[ERROR] Qdrant connection failed: {e}")
        return False

def test_openai_connection():
    """Test OpenAI API connection with minimal request"""
    try:
        import openai
        openai.api_key = settings.openai_api_key

        # Make a minimal test request
        response = openai.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5,
            temperature=0
        )

        print("[OK] OpenAI API connection successful")
        return True
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
            print(f"[WARN] OpenAI API connection failed due to rate limit or quota: {error_msg}")
        else:
            print(f"[ERROR] OpenAI API connection failed: {error_msg}")
        return False

async def test_openai_connection_async():
    """Async version to test OpenAI API"""
    try:
        import openai
        openai.api_key = settings.openai_api_key

        # Make a minimal test request
        response = await openai.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5,
            temperature=0
        )

        print("[OK] OpenAI API async connection successful")
        return True
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
            print(f"[WARN] OpenAI API async connection failed due to rate limit or quota: {error_msg}")
        else:
            print(f"[ERROR] OpenAI API async connection failed: {error_msg}")
        return False

def main():
    print("Testing API connections...")
    print("=" * 40)

    # Test Cohere
    cohere_ok = test_cohere_connection()

    # Test Qdrant
    qdrant_ok = test_qdrant_connection()

    # Test OpenAI
    openai_ok = test_openai_connection()

    # Async OpenAI test
    try:
        openai_async_ok = asyncio.run(test_openai_connection_async())
    except Exception as e:
        print(f"✗ OpenAI async test failed: {e}")
        openai_async_ok = False

    print("=" * 40)
    print("Summary:")
    print(f"Cohere: {'[OK]' if cohere_ok else '[ERROR]'}")
    print(f"Qdrant:  {'[OK]' if qdrant_ok else '[ERROR]'}")
    print(f"OpenAI:  {'[OK]' if openai_ok else '[ERROR]'}")
    print(f"OpenAI Async:  {'[OK]' if openai_async_ok else '[ERROR]'}")

    all_ok = cohere_ok and qdrant_ok and (openai_ok or openai_async_ok)
    print(f"Overall: {'[OK] All services connected' if all_ok else '[ERROR] Some services failed'}")

    return all_ok

if __name__ == "__main__":
    main()
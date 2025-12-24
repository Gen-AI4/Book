#!/usr/bin/env python3
"""
Test script to verify that the original 400 Bad Request error is fixed
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.context_retrieval_service import ContextRetrievalService

def test_original_issue():
    """Test that reproduces the original issue scenario"""
    print("Testing the original issue scenario...")

    # Initialize the service that was causing the 400 error
    service = ContextRetrievalService()

    # This is the same call that was causing the 400 error in the logs
    try:
        results = service.retrieve_context("test query for verification", top_k=1)
        print(f"[SUCCESS] Query completed without 400 error, got {len(results)} results")

        if results:
            print(f"First result score: {results[0]['score']:.4f}")
            print(f"First result content preview: {results[0]['content'][:100]}...")

        return True
    except Exception as e:
        print(f"[ERROR] Query failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing original 400 Bad Request error scenario...")
    print("Original error: POST .../collections/textbook_content/points/query 'HTTP/1.1 400 Bad Request'")
    print()

    success = test_original_issue()

    if success:
        print("\n[VERIFIED] The original 400 Bad Request error has been fixed!")
        print("The Qdrant query_points method is working correctly with the proper API parameters.")
    else:
        print("\n[ISSUE REMAINS] The original error still exists.")
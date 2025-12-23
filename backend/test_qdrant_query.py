#!/usr/bin/env python3
"""
Script to test Qdrant query functionality with the fixed client initialization
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.context_retrieval_service import ContextRetrievalService

def test_qdrant_query():
    """Test that Qdrant queries work properly with the fixed client initialization"""
    print("Testing Qdrant query functionality...")
    try:
        service = ContextRetrievalService()

        # Test a simple query to ensure the client works properly
        # This should work now that we've fixed the client initialization
        results = service.retrieve_context("test query for verification", top_k=1)

        print(f"[OK] Qdrant query successful, found {len(results)} results")
        print("[OK] ContextRetrievalService client initialization is working correctly")
        return True
    except Exception as e:
        print(f"[ERROR] Qdrant query failed: {e}")
        return False

def main():
    print("Testing Qdrant query functionality...")
    print("=" * 40)

    test_passed = test_qdrant_query()

    print("=" * 40)
    print("Test Summary:")
    print(f"Qdrant Query Test: {'[OK]' if test_passed else '[ERROR]'}")

    if test_passed:
        print("Overall: [OK] Qdrant query functionality working correctly")
    else:
        print("Overall: [ERROR] Qdrant query functionality has issues")

    return test_passed

if __name__ == "__main__":
    main()
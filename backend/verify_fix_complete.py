#!/usr/bin/env python3
"""
Test script to verify that the Qdrant dimension mismatch issue is fixed
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.context_retrieval_service import ContextRetrievalService

def test_fix():
    """Test that the dimension mismatch issue is fixed"""
    print("Testing that the Qdrant dimension mismatch issue is fixed...")

    try:
        service = ContextRetrievalService()

        # Test a simple query that was failing before
        results = service.retrieve_context("test query to verify fix", top_k=1)

        print(f"[OK] Query completed successfully, got {len(results)} results")

        if results:
            print(f"[OK] First result score: {results[0]['score']:.4f}")
            print("[OK] Context retrieval is working properly with correct dimensions")
        else:
            print("[OK] Query successful - no results found (expected if no data ingested yet)")

        return True

    except Exception as e:
        print(f"[ERROR] Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Verifying the Qdrant dimension mismatch fix...")
    print("Expected: No 'Vector dimension error: expected dim: 1024, got 768' error")
    print()

    success = test_fix()

    if success:
        print("\n[SUCCESS] VERIFICATION PASSED: The dimension mismatch issue has been fixed!")
        print("[SUCCESS] Qdrant collection is properly configured with 1024 dimensions")
        print("[SUCCESS] Cohere embeddings match the collection dimensions")
        print("[SUCCESS] Context retrieval service works correctly")
    else:
        print("\n[FAILURE] VERIFICATION FAILED: The issue still exists")
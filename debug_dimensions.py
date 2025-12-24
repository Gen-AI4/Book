import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.context_retrieval_service import ContextRetrievalService

# Test what dimensions are actually being returned
service = ContextRetrievalService()

try:
    response = service.cohere_client.embed(
        texts=["test query"],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    embedding = response.embeddings[0]
    print(f"Actual embedding dimension: {len(embedding)}")
    print(f"Success: Using search_query input type")
except Exception as e:
    print(f"Error: {e}")

# Also test what might be happening with search_document for comparison
try:
    response2 = service.cohere_client.embed(
        texts=["test query"],
        model="embed-english-v3.0",
        input_type="search_document"
    )
    embedding2 = response2.embeddings[0]
    print(f"For comparison - search_document dimension: {len(embedding2)}")
except Exception as e:
    print(f"Error with search_document: {e}")
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
import cohere
import logging
import os
import time
from functools import wraps

# Import settings directly
from backend.config import settings

logger = logging.getLogger(__name__)

# Simple in-memory cache with TTL
class SimpleCache:
    def __init__(self, ttl_seconds: int = 300):  # 5 minutes default TTL
        self.cache = {}
        self.ttl_seconds = ttl_seconds

    def get(self, key: str):
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl_seconds:
                return value
            else:
                # Remove expired entry
                del self.cache[key]
        return None

    def set(self, key: str, value):
        self.cache[key] = (value, time.time())

    def clear_expired(self):
        current_time = time.time()
        expired_keys = [
            key for key, (_, timestamp) in self.cache.items()
            if current_time - timestamp >= self.ttl_seconds
        ]
        for key in expired_keys:
            del self.cache[key]


class ContextRetrievalService:
    def __init__(self):
        # Initialize Qdrant client
        if settings.qdrant_api_key:
            self.qdrant_client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key
            )
        else:
            self.qdrant_client = QdrantClient(url=settings.qdrant_url)

        # Initialize Cohere client
        self.cohere_client = cohere.Client(settings.cohere_api_key)

        self.collection_name = settings.qdrant_collection_name

        # Initialize cache
        self.cache = SimpleCache(ttl_seconds=300)  # 5 minute TTL

    def retrieve_context(self, query: str, top_k: int = 5, min_score: float = 0.3) -> List[Dict[str, Any]]:
        """
        Retrieve context from Qdrant based on the query
        """
        # Create cache key
        cache_key = f"{query}:{top_k}:{min_score}"

        # Try to get from cache first
        cached_result = self.cache.get(cache_key)
        if cached_result is not None:
            logger.info(f"Cache hit for query: {query[:50]}...")
            return cached_result

        try:
            # Generate embedding for the query using Cohere
            response = self.cohere_client.embed(
                texts=[query],
                model="multilingual-22-12"  # Using a good general-purpose embedding model
            )
            query_embedding = response.embeddings[0]

            # Search in Qdrant for similar vectors
            search_result = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k * 2  # Get more results to allow for filtering
            )

            # Format the results and apply filtering
            context_items = []
            for result in search_result:
                # Apply minimum score filtering
                if result.score >= min_score:
                    context_items.append({
                        "id": result.id,
                        "content": result.payload.get("content", ""),
                        "score": result.score,
                        "source": result.payload.get("source", ""),
                        "metadata": result.payload
                    })

            # Sort by score in descending order and limit to top_k
            context_items.sort(key=lambda x: x["score"], reverse=True)
            result = context_items[:top_k]

            # Cache the result
            self.cache.set(cache_key, result)

            return result
        except Exception as e:
            logger.error(f"Error retrieving context from Qdrant: {str(e)}")
            return []

    def construct_context_block(self, context_items: List[Dict[str, Any]]) -> str:
        """
        Construct a context block by concatenating retrieved chunks
        Format: Context:\n---\n{chunk1}\n---\n{chunk2}...
        """
        if not context_items:
            return ""

        context_parts = ["Context:"]
        for item in context_items:
            content = item.get("content", "")
            context_parts.append("---")
            context_parts.append(content)

        return "\n".join(context_parts)
import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_collection_if_not_exists(collection_name: str = "physical_ai_textbook"):
    """
    Creates a Qdrant collection if it doesn't exist, with the correct vector configuration
    for Cohere embeddings (1024 dimensions, Cosine distance).
    """
    # Initialize Qdrant client
    qdrant_host = os.getenv("QDRANT_HOST")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_host or not qdrant_api_key:
        raise ValueError("QDRANT_HOST and QDRANT_API_KEY must be set in environment variables")

    client = QdrantClient(
        url=qdrant_host,
        api_key=qdrant_api_key,
    )

    # Check if collection exists
    try:
        collections = client.get_collections()
        collection_names = [collection.name for collection in collections.collections]

        if collection_name not in collection_names:
            print(f"Creating collection '{collection_name}' with 1024 dimensions and Cosine distance...")

            # Create collection with 1024 dimensions for Cohere embeddings and Cosine distance
            client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=1024,  # Cohere embed-english-v3.0 produces 1024-dimensional vectors
                    distance=models.Distance.COSINE
                )
            )
            print(f"Collection '{collection_name}' created successfully!")
        else:
            print(f"Collection '{collection_name}' already exists.")

    except Exception as e:
        print(f"Error creating or checking collection: {e}")
        raise e

    return client

if __name__ == "__main__":
    create_collection_if_not_exists()
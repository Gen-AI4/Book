import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import settings
from qdrant_client import QdrantClient

def check_collection():
    """Check the actual collection configuration"""
    if settings.qdrant_api_key:
        client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
    else:
        client = QdrantClient(url=settings.qdrant_url)

    try:
        collection_info = client.get_collection(settings.qdrant_collection_name)
        print(f"Collection '{settings.qdrant_collection_name}' exists")
        print(f"Vector size: {collection_info.config.params.vectors.size}")
        print(f"Distance: {collection_info.config.params.vectors.distance}")

        # Get collection info to see how many points are in it
        count_info = client.count(
            collection_name=settings.qdrant_collection_name
        )
        print(f"Number of points in collection: {count_info.count}")

        if count_info.count > 0:
            # Check a few points to see actual dimensions
            records, next_page = client.scroll(
                collection_name=settings.qdrant_collection_name,
                limit=1
            )

            if records:  # If there are records
                sample_record = records[0]
                if hasattr(sample_record, 'vector') and sample_record.vector:
                    vector_size = len(sample_record.vector) if isinstance(sample_record.vector, list) else 'N/A'
                    print(f"Sample point vector size: {vector_size}")
                else:
                    print("Sample record has no vector or vector is not a list")
            else:
                print("No records returned from scroll")
        else:
            print("Collection is empty")

    except Exception as e:
        print(f"Error checking collection: {e}")

if __name__ == "__main__":
    check_collection()
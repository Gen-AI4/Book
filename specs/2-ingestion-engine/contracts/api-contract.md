# Ingestion Pipeline API Contract

**Feature**: 2-ingestion-engine
**Created**: 2025-12-20

## Function Definitions

### get_all_urls(base_url: str) -> List[str]
- **Purpose**: Retrieves all textbook page URLs from the deployed site
- **Input**: Base URL of the textbook site
- **Output**: List of all content page URLs
- **Errors**: NetworkError if base URL is unreachable

### extract_text_from_url(url: str) -> str
- **Purpose**: Extracts clean text content from a specific URL
- **Input**: URL of a textbook page
- **Output**: Clean text content from the page
- **Errors**: ContentExtractionError if content cannot be extracted

### chunk_text(text: str, chunk_size: int = 1000) -> List[str]
- **Purpose**: Splits text into manageable chunks
- **Input**: Text content and optional chunk size
- **Output**: List of text chunks
- **Errors**: None

### embed(texts: List[str]) -> List[List[float]]
- **Purpose**: Generates vector embeddings for text chunks
- **Input**: List of text chunks
- **Output**: List of 1024-dimensional embedding vectors
- **Errors**: EmbeddingError if API call fails

### create_collection(name: str) -> bool
- **Purpose**: Creates Qdrant collection for embeddings
- **Input**: Collection name
- **Output**: Success status
- **Errors**: CollectionCreationError if creation fails

### save_chunk_to_qdrant(chunk: str, embedding: List[float], metadata: Dict) -> bool
- **Purpose**: Stores chunk in Qdrant with metadata
- **Input**: Text chunk, embedding vector, and metadata dictionary
- **Output**: Success status
- **Errors**: StorageError if saving fails

### main() -> None
- **Purpose**: Coordinates the entire ingestion process
- **Input**: None (uses environment variables)
- **Output**: None (logs progress and results)
- **Errors**: Various errors depending on failure point
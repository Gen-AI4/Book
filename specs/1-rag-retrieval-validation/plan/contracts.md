# API Contracts: RAG Retrieval Validation

**Feature**: RAG Retrieval Validation
**Created**: 2025-12-20
**Status**: Complete

## Primary Function Contract

### Function: `retrieve(query)`

**Description**: Validates the RAG pipeline retrieval by taking a user query, generating an embedding, querying a vector database, and returning the most relevant text chunks.

**Signature**: `retrieve(query: str) -> List[SearchResult]`

#### Parameters
- `query` (string, required): The text query to validate against the RAG pipeline
  - Must be non-empty
  - Should be between 1 and 1000 characters
  - Cannot be null or undefined

#### Return Value
- `List[SearchResult]`: An array containing up to 3 SearchResult objects, ordered by relevance (most relevant first)

#### SearchResult Object
- `distance` (number): The similarity distance score (lower values indicate higher similarity)
- `content` (string): The text content of the retrieved chunk
- `metadata` (object, optional): Additional metadata from the vector database

#### Error Responses
- `ServiceUnavailableError`: Thrown when Cohere or Qdrant services are unavailable
- `InvalidQueryError`: Thrown when the query is malformed or empty
- `RetrievalError`: Thrown when the retrieval process fails for any other reason

## Secondary Functions

### Function: `validate_rag_pipeline(query)`

**Description**: Wrapper function that calls retrieve and validates the results for quality assurance.

**Signature**: `validate_rag_pipeline(query: str) -> ValidationReport`

#### Parameters
- `query` (string, required): The text query to validate

#### Return Value
- `ValidationReport` object containing:
  - `success` (boolean): Whether the validation was successful
  - `results` (List[SearchResult]): The retrieved results
  - `execution_time` (number): Time taken for the operation in milliseconds
  - `error` (string, optional): Error message if validation failed

## Environment Variables Contract

### Required Environment Variables
- `COHERE_API_KEY` (string): API key for Cohere embedding service
- `QDRANT_HOST` (string): Host URL for Qdrant Cloud instance
- `QDRANT_API_KEY` (string): API key for Qdrant Cloud
- `QDRANT_COLLECTION` (string): Name of the collection to search (default: "text_chunks")

## External Service Contracts

### Cohere Embedding Service
- **Endpoint**: Cohere's embedding API (via Python SDK)
- **Method**: Embedding generation with `input_type="search_query"`
- **Model**: `embed-english-v3.0` (or configured model)
- **Expected Response Time**: < 2 seconds for single query
- **Error Handling**: Rate limiting, service unavailability

### Qdrant Vector Database
- **Endpoint**: Configured Qdrant Cloud instance
- **Method**: Vector similarity search
- **Query Type**: Dense vector search
- **Limit**: Top 3 results
- **Expected Response Time**: < 2 seconds for search
- **Error Handling**: Connection failures, collection not found

## Performance Contract

### Response Time Requirements
- Total execution time: < 10 seconds (from spec SC-001)
- Individual service calls: < 2 seconds each
- Error handling: < 1 second

### Success Rate Requirements
- Successful retrieval: 95% of valid queries (from spec SC-002)
- Proper result formatting: 100% of successful calls

## Security Contract

### Authentication
- Cohere API: Bearer token via API key
- Qdrant Cloud: API key authentication
- Keys stored in environment variables, not hardcoded

### Data Privacy
- No user queries stored or logged
- No embedding vectors stored beyond the current request
- No search results cached inappropriately
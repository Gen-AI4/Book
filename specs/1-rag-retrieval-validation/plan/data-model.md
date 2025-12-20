# Data Model: RAG Retrieval Validation

**Feature**: RAG Retrieval Validation
**Created**: 2025-12-20
**Status**: Complete

## Entities

### Query
- **Description**: A text string representing a user search request that needs to be validated
- **Fields**:
  - `text` (string): The actual query text
- **Validation**:
  - Must not be empty or contain only whitespace
  - Length should be reasonable (e.g., 1-1000 characters)

### Embedding
- **Description**: A vector representation of the query used for similarity matching
- **Fields**:
  - `vector` (list of floats): The numerical vector representation
  - `model` (string): The embedding model used (e.g., "embed-english-v3.0")
- **Validation**:
  - Vector must have the correct dimensionality for the target model
  - Model name must be valid and supported

### SearchResult
- **Description**: An individual result from the similarity search
- **Fields**:
  - `distance` (float): The similarity distance score (lower is more similar)
  - `content` (string): The text content of the matching chunk
  - `metadata` (dict): Additional metadata from the vector database
- **Validation**:
  - Distance must be a non-negative number
  - Content must not be empty

### SearchResults
- **Description**: Container for multiple search results
- **Fields**:
  - `results` (list of SearchResult): The list of individual results
  - `query` (string): The original query that generated these results
  - `count` (int): The number of results returned
- **Validation**:
  - Must contain at most 3 results as per requirements
  - Results should be ordered by similarity (closest first)

## Relationships

### Query → Embedding
- A Query generates one Embedding through the embedding process
- This is a 1:1 relationship for the purpose of this validation

### Embedding → SearchResult
- An Embedding is used to find multiple SearchResults through similarity search
- This is a 1:many relationship

### SearchResults → SearchResult
- SearchResults contains multiple SearchResult items
- This is a 1:many composition relationship

## State Transitions

### Query Processing Flow
1. **Input**: Query is received and validated
2. **Embedding**: Query is converted to Embedding using Cohere API
3. **Search**: Embedding is used to query Qdrant for similar vectors
4. **Results**: SearchResults with top 3 SearchResult items is returned

## Validation Rules

### From Functional Requirements
- FR-001: Query must be accepted as input to the retrieve function
- FR-002: Embedding must be generated for similarity matching
- FR-003: Vector database must be queried with the embedding
- FR-004: Top 3 most relevant results must be returned
- FR-005: Distance scores and payload content must be displayed
- FR-006: Service unavailability must be handled gracefully
- FR-007: Secure authentication must be used for vector database

### Additional Validation
- Query length must be within reasonable bounds
- Results must be ordered by similarity score
- Error responses must contain appropriate messaging
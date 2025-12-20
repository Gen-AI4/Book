# Feature Tasks: Ingestion Engine Backend

**Feature**: 2-ingestion-engine
**Generated**: 2025-12-20
**Status**: Draft

## Implementation Strategy

The implementation will follow the single-file system design with specific functions as requested. The ingestion pipeline will process "Physical AI" textbook content from the deployed site, generate vector embeddings using Cohere, and store them in Qdrant Cloud with appropriate metadata.

## Dependencies

- User Story 2 (Vector Embedding Generation) depends on User Story 1 (Textbook Content Ingestion) for the basic ingestion infrastructure
- User Story 3 (Vector Storage Management) depends on User Story 1 and User Story 2 for content processing and embedding generation

## Parallel Execution Examples

- Dependencies installation (T001, T002) can run in parallel with environment setup (T003)
- Database initialization (T004, T005) can run in parallel with ingestion function implementation (T006-T011)
- Web scraping functions can be developed in parallel with chunking and embedding functions

## Phase 1: Setup

### Goal
Initialize the project structure and configure dependencies for the ingestion pipeline.

- [x] T001 Create backend directory structure
- [x] T002 [P] Create `backend/requirements.txt` with: `cohere`, `qdrant-client`, `python-dotenv`, `langchain-text-splitters`, `requests`, `beautifulsoup4`
- [x] T003 [P] Create `backend/.env` with `COHERE_API_KEY`, `QDRANT_HOST`, and `QDRANT_API_KEY`

## Phase 2: Foundational

### Goal
Set up the database schema and initialize the Qdrant collection for storing vector embeddings.

- [x] T004 Create `backend/init_db.py` with Qdrant client configuration
- [x] T005 Implement logic to check if collection `physical_ai_textbook` exists; if not, create it with `vector_size: 1024` (for Cohere `embed-english-v3.0`) and `distance: Cosine`

## Phase 3: User Story 1 - Textbook Content Ingestion (Priority: P1)

### Goal
Implement the core functionality to process "Physical AI" textbook content from the deployed site and prepare it for vector storage.

### Independent Test Criteria
- Given the ingestion system is properly configured, when I run the process on textbook content, then the content is successfully parsed and stored as vector embeddings
- Given textbook content exists in the source location, when I execute the ingestion process, then I receive a success notification indicating successful processing

- [x] T006 [P] [US1] Implement function `get_all_urls(base_url)` to retrieve all textbook page URLs from the deployed site (https://the-book-iota.vercel.app/)
- [x] T007 [P] [US1] Implement function `extract_text_from_url(url)` to extract clean text content from a specific URL, handling Docusaurus site structure
- [x] T008 [US1] Create the main ingestion script `backend/ingest.py` with basic structure
- [x] T009 [US1] Implement error handling for network issues in web scraping functions
- [x] T010 [US1] Add logging functionality to track ingestion progress and errors

## Phase 4: User Story 2 - Vector Embedding Generation (Priority: P2)

### Goal
Convert the textbook content to vector embeddings using the Cohere API for semantic search capabilities.

### Independent Test Criteria
- Given raw textbook text content, when the embedding process runs, then numerical vectors representing the semantic meaning are generated
- Given similar text content, when embeddings are compared, then they should have high similarity scores

- [x] T011 [P] [US2] Implement function `chunk_text(text, chunk_size=500, overlap=50)` to split text into manageable chunks with appropriate overlap
- [x] T012 [US2] Implement function `get_embeddings(texts)` to generate vector embeddings using Cohere API with batch processing (Note: Function renamed to match directive)
- [x] T013 [US2] Add retry logic with exponential backoff for Cohere API calls
- [x] T014 [US2] Implement batch processing to optimize API usage (up to 96 texts per request)

## Phase 5: User Story 3 - Vector Storage Management (Priority: P3)

### Goal
Store the vector embeddings with proper metadata in Qdrant for retrieval with context during searches.

### Independent Test Criteria
- Given vector embeddings with associated metadata, when they are stored, then the metadata is preserved and accessible
- Given a stored vector record, when I query for its metadata, then I can retrieve the source URL and chapter title information

- [x] T015 [US3] Implement function `save_chunk_to_qdrant(chunk, embedding, metadata)` to store vectors with metadata in Qdrant
- [x] T016 [US3] Add proper metadata handling including source URL, chapter title, and content preview
- [x] T017 [US3] Implement function `create_collection(name)` to manage Qdrant collections if needed
- [x] T018 [US3] Add verification mechanism to confirm successful storage in Qdrant

## Phase 6: Integration and Testing

### Goal
Integrate all components into a cohesive ingestion pipeline and verify its functionality.

- [x] T019 Implement the main function to coordinate the entire ingestion process
- [x] T020 Add comprehensive error handling and logging throughout the pipeline
- [x] T021 Implement checkpointing mechanism for partial failure recovery
- [x] T022 Test the complete pipeline with sample textbook content
- [x] T023 Verify vector count in Qdrant Dashboard matches expected values

## Phase 7: Polish & Cross-Cutting Concerns

### Goal
Address edge cases and add finishing touches to ensure robust operation.

- [x] T024 Handle large content files that exceed memory limits with streaming/chunked processing
- [x] T025 Add validation for embedding dimensions (must be exactly 1024 for Cohere embeddings)
- [x] T026 Implement graceful handling of malformed text files or files with special characters
- [x] T027 Add progress reporting with percentage completion during long-running ingestion
- [x] T028 Create documentation for running and configuring the ingestion pipeline
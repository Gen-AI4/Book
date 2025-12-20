# Implementation Plan: Ingestion Engine Backend

**Feature**: 2-ingestion-engine
**Created**: 2025-12-20
**Status**: Draft
**Author**: Claude

## Technical Context

This plan outlines the implementation of the data ingestion pipeline that processes "Physical AI" textbook content, generates vector embeddings, and stores them in a vector database. The implementation will follow a single-file system design with specific functions as requested.

### Architecture Overview

- **Frontend**: Docusaurus-based textbook at https://the-book-iota.vercel.app/
- **Backend**: Python-based ingestion pipeline
- **Vector Database**: Qdrant Cloud
- **Embedding Service**: Cohere API
- **Data Source**: Deployed site URLs

### Key Requirements

- Qdrant Cloud endpoint URL and API key (from .env)
- Cohere API key (from .env)
- Access to deployed textbook site at https://the-book-iota.vercel.app/

## Constitution Check

### Sim-to-Real Transfer Focus
- ✅ The ingestion engine will support educational content for Physical AI and Humanoid Robotics
- ✅ Textbook content will be properly indexed for semantic search capabilities

### Multi-Modal Learning Approach
- ✅ Integration with existing technology stack (Python, Qdrant, Cohere)
- ✅ Content will be accessible through the RAG chatbot mentioned in constitution

### Test-First for Educational Content
- ✅ Implementation will include proper error handling and validation
- ✅ Logging will be implemented to track ingestion success/failure

### Hardware-Aware Implementation
- ✅ Memory-efficient chunking strategy to handle large content files
- ✅ Batch processing to optimize API usage

### Interactive Learning Experience
- ✅ Content will be stored with proper metadata for context-aware Q&A
- ✅ Vector embeddings will enable semantic search in the textbook

### Compliance Verification
- All requirements from the constitution have been addressed in the implementation plan

## Phase 0: Research

### Research Tasks

1. **Qdrant Cloud Setup**: Research Qdrant Cloud configuration and API usage
2. **Cohere Embeddings**: Research Cohere embedding API best practices
3. **Web Scraping**: Research methods to extract text content from deployed URLs
4. **Text Chunking**: Research optimal text chunking strategies for educational content

### Implementation Decisions

- **Decision**: Use Python 3.10+ with virtual environment
- **Rationale**: Aligns with project constitution technology stack
- **Alternatives considered**: Node.js, Go - Python chosen for better ML/AI library support

- **Decision**: Use `cohere` and `qdrant-client` libraries
- **Rationale**: Direct integration with required services
- **Alternatives considered**: OpenAI embeddings, Pinecone - Cohere/Qdrant chosen per requirements

- **Decision**: Single-file implementation with specific functions
- **Rationale**: Per user requirements for simplicity and maintainability
- **Alternatives considered**: Multi-module structure - single file chosen per requirements

## Phase 1: Design & Contracts

### Data Model

#### Textbook Content Entity
- **Source URL**: String (identifier for content location)
- **Chapter Title**: String (title of the textbook section)
- **Content Text**: String (the actual text content)
- **Vector Embedding**: Array of floats (1024-dimensional vector representation)
- **Metadata**: Dictionary (additional information like section, timestamp)

### API Contracts

#### Ingestion Pipeline Functions

1. `get_all_urls(base_url)` - Retrieves all textbook page URLs from the deployed site
2. `extract_text_from_url(url)` - Extracts clean text content from a specific URL
3. `chunk_text(text, chunk_size=1000)` - Splits text into manageable chunks
4. `embed(texts)` - Generates vector embeddings for text chunks
5. `create_collection(name)` - Creates Qdrant collection for embeddings
6. `save_chunk_to_qdrant(chunk, embedding, metadata)` - Stores chunk in Qdrant
7. `main()` - Coordinates the entire ingestion process

## Phase 2: Implementation Plan

### Task 1: Environment Setup
- [ ] Create `backend/` directory
- [ ] Initialize Python virtual environment
- [ ] Create `.env` file for environment variables
- [ ] Install required dependencies

### Task 2: SDK Configuration
- [ ] Install `cohere` library
- [ ] Install `qdrant-client` library
- [ ] Install `requests` and `beautifulsoup4` for web scraping
- [ ] Install `python-dotenv` for environment management

### Task 3: Qdrant Initialization
- [ ] Configure Qdrant client with cloud credentials
- [ ] Create `textbook_embeddings` collection with proper vector dimensions
- [ ] Implement connection verification

### Task 4: Web Scraping Implementation
- [ ] Implement `get_all_urls` function to crawl the textbook site
- [ ] Implement `extract_text_from_url` function to extract clean text
- [ ] Add error handling for network issues

### Task 5: Text Processing Pipeline
- [ ] Implement `chunk_text` function with appropriate strategy
- [ ] Implement `embed` function to generate vector embeddings
- [ ] Add batch processing for efficiency

### Task 6: Storage Implementation
- [ ] Implement `create_collection` function
- [ ] Implement `save_chunk_to_qdrant` function
- [ ] Add proper metadata handling (source URL, chapter title)

### Task 7: Integration and Testing
- [ ] Implement `main` function to coordinate the pipeline
- [ ] Add comprehensive logging
- [ ] Test with sample textbook content
- [ ] Verify vector count in Qdrant Dashboard

## Risk Analysis

### High-Risk Items
- **External API Reliability**: Cohere API availability affects ingestion
- **Rate Limiting**: API rate limits may slow down ingestion process
- **Large Content Files**: Memory constraints when processing large files

### Mitigation Strategies
- Implement retry logic with exponential backoff
- Use batch processing to optimize API usage
- Implement streaming/chunked processing for large files

## Success Criteria

- [ ] Ingestion pipeline processes all textbook content without errors
- [ ] Vector embeddings are generated and stored successfully
- [ ] All content is stored with proper metadata (URL, chapter title)
- [ ] System handles edge cases gracefully (network issues, large files, etc.)
- [ ] Qdrant Dashboard shows correct vector count after execution
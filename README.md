---
title: The Book - AI Teaching Assistant Backend
emoji: 🤖
colorFrom: blue
colorTo: red
sdk: docker
app_file: app.py
pinned: false
---

# The Book - AI Teaching Assistant Backend

This is the backend service for The Book AI Teaching Assistant, a Physical AI system with RAG capabilities. This FastAPI backend serves as the "Mind" of the textbook. It uses OpenAI Chat Completions for reasoning and Qdrant for context retrieval (RAG system).

## Overview

This backend provides:
- FastAPI-based REST API
- RAG (Retrieval Augmented Generation) capabilities
- Integration with Qdrant for vector storage
- Integration with OpenAI for responses
- Integration with Cohere for embeddings

## Endpoints

- `GET /` - Health check
- `GET /health` - Health status
- `GET /docs` - API documentation
- `POST /chat` - Chat endpoint for AI interactions

## Environment Variables

The following environment variables need to be configured in your Hugging Face Space settings:

- `OPENAI_API_KEY` - Your OpenAI API key
- `QDRANT_API_KEY` - Your Qdrant API key
- `QDRANT_URL` - Your Qdrant instance URL
- `COHERE_API_KEY` - Your Cohere API key
- `QDRANT_COLLECTION_NAME` - Name of the collection to query (default: textbook_content)

## How to Use

1. The backend is automatically started when the Space loads
2. The API endpoints are available at the root URL of the Space
3. You can test the API using the `/docs` endpoint for interactive documentation

## Architecture

The system follows a service-oriented architecture:
- `main.py`: FastAPI application with endpoints
- `models.py`: Pydantic models for request/response validation
- `services/`: Business logic services
  - `context_retrieval_service.py`: Qdrant integration and context retrieval
  - `openai_service.py`: OpenAI API integration
  - `chat_service.py`: Orchestrates the RAG flow
- `config.py`: Configuration and environment variables
- `utils.py`: Utility functions
- `middleware.py`: Rate limiting and other middleware
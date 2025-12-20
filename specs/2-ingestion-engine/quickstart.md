# Quickstart: Ingestion Engine Backend

**Feature**: 2-ingestion-engine
**Created**: 2025-12-20

## Prerequisites

- Python 3.10+
- Access to Cohere API (API key)
- Access to Qdrant Cloud (endpoint URL and API key)
- Internet access to scrape content from https://the-book-iota.vercel.app/

## Setup

### 1. Clone and Navigate
```bash
# Navigate to your project directory
cd your-project-root
```

### 2. Create Backend Directory
```bash
mkdir -p backend
cd backend
```

### 3. Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install cohere qdrant-client requests beautifulsoup4 python-dotenv
```

### 5. Create Environment File
Create a `.env` file in the backend directory:
```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_HOST=your_qdrant_cloud_endpoint_here
QDRANT_API_KEY=your_qdrant_api_key_here
BASE_URL=https://the-book-iota.vercel.app/
```

## Running the Ingestion Pipeline

### 1. Prepare the ingest.py file
Create `ingest.py` with the implementation containing all required functions.

### 2. Execute the Pipeline
```bash
cd backend
python ingest.py
```

## Expected Output

- All textbook content from the deployed site will be processed
- Vector embeddings will be stored in Qdrant Cloud
- Progress and status will be logged to the console
- Final count of stored vectors will be displayed

## Verification

1. Check the Qdrant Cloud dashboard for the `textbook_embeddings` collection
2. Verify the vector count matches the expected number of content chunks
3. Confirm metadata includes proper source URLs and chapter titles
# Quickstart: Docusaurus Textbook Frontend

## Prerequisites
- Node.js 18.0 or higher
- Python 3.9 or higher
- npm package manager
- Access to Qdrant Cloud (for vector database)
- Access to Neon Postgres (for transactional data)

## Setup Instructions

### 1. Clone and Initialize the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Set up the Frontend (Docusaurus)
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Install required packages for math and diagrams
npm install remark-math rehype-katex
npm install @docusaurus/theme-mermaid

# Start development server
npm start
```

### 3. Set up the Backend (FastAPI)
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn qdrant-client openai python-dotenv

# Set up environment variables
cp .env.example .env
# Edit .env with your Qdrant and Neon credentials

# Start the backend server
uvicorn main:app --reload
```

### 4. Initialize the Knowledge Base
```bash
# From the backend directory
python ingest.py
```

### 5. Build and Deploy
```bash
# From the frontend directory
npm run build

# The built static files will be in the build/ directory
# Deploy these to GitHub Pages or your preferred static hosting
```

## Environment Variables
Create a `.env` file in the backend directory with the following variables:
```
QDRANT_URL=<your-qdrant-url>
QDRANT_API_KEY=<your-qdrant-api-key>
NEON_DATABASE_URL=<your-neon-database-url>
OPENAI_API_KEY=<your-openai-api-key>
```

## Running Tests
```bash
# Frontend tests
npm test

# Backend tests
cd backend
python -m pytest
```

## Development Workflow
1. Make changes to the documentation in `frontend/docs/`
2. Update the knowledge base by running `python backend/ingest.py`
3. Test the chatbot functionality
4. Run the build process to generate static files
5. Deploy to GitHub Pages
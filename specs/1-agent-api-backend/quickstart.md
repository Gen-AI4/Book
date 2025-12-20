# Quickstart Guide: Agent API Backend

## Prerequisites

- Python 3.9 or higher
- pip package manager
- Access to OpenAI API key
- Access to Qdrant Cloud or local Qdrant instance
- Access to Cohere API key (for embeddings)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn python-dotenv openai cohere qdrant-client pydantic
```

### 4. Environment Configuration
Create a `.env` file in the project root with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
COHERE_API_KEY=your_cohere_api_key
QDRANT_COLLECTION_NAME=textbook_content
```

## Running the Server

### 1. Start the API Server
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Access the API
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Chat Endpoint: http://localhost:8000/chat

## Making Your First Request

### Using curl:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the textbook about?",
    "history": []
  }'
```

### Using Python requests:
```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={
        "message": "What is the textbook about?",
        "history": []
    }
)
print(response.json())
```

## API Usage Examples

### Basic Chat Request
```json
{
  "message": "Explain quantum computing in simple terms",
  "history": []
}
```

### Chat with Conversation History
```json
{
  "message": "Can you elaborate on that?",
  "history": [
    {
      "role": "user",
      "content": "What is quantum computing?"
    },
    {
      "role": "assistant",
      "content": "Quantum computing uses quantum bits (qubits) that can exist in multiple states simultaneously..."
    }
  ]
}
```

### Advanced Request with Parameters
```json
{
  "message": "How does this apply to robotics?",
  "history": [],
  "context_window": 3,
  "temperature": 0.5,
  "max_tokens": 500
}
```

## Testing the API

### Run Unit Tests
```bash
python -m pytest tests/
```

### Run Integration Tests
```bash
python -m pytest tests/integration/
```

## Development Workflow

### 1. Adding New Endpoints
- Define the endpoint in `main.py`
- Create request/response models in `models.py`
- Add validation logic as needed
- Update API documentation

### 2. Modifying Business Logic
- Update services in the `services/` directory
- Ensure proper error handling
- Add or update tests for new functionality
- Update documentation as needed

### 3. Environment Variables
The following environment variables are required:

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key | Yes |
| `QDRANT_URL` | Qdrant instance URL | Yes |
| `QDRANT_API_KEY` | Qdrant API key (if using cloud) | Yes |
| `COHERE_API_KEY` | Cohere API key | Yes |
| `QDRANT_COLLECTION_NAME` | Name of the collection to query | Yes |
| `DEBUG` | Enable debug mode | No (default: False) |

## Troubleshooting

### Common Issues

1. **500 Error on Chat Request**
   - Check that all API keys are correctly configured
   - Verify Qdrant connection
   - Check OpenAI API availability

2. **Slow Response Times**
   - Verify network connectivity to external services
   - Check if embedding and LLM calls are properly cached
   - Monitor system resource usage

3. **No Context Retrieved**
   - Verify that Qdrant contains relevant data
   - Check that the collection name matches the data
   - Validate embedding generation process

### Logging
The API logs to stdout by default. For production, configure logging to write to files:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Deployment

### Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment-Specific Configuration
For production deployment, ensure:
- Proper API key management
- SSL/TLS configuration
- Rate limiting setup
- Monitoring and alerting
# Quickstart: Frontend-Backend Connection

## Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.11+
- FastAPI backend running on `http://localhost:8000`

## Setup

### 1. Start the Backend Server
```bash
cd backend
pip install -r requirements.txt
python -m src.main
```
The backend should be accessible at `http://localhost:8000`

### 2. Start the Docusaurus Frontend
```bash
cd frontend  # or root directory if Docusaurus is in root
npm install
npm run start
```
The frontend should be accessible at `http://localhost:3000`

## Development Workflow

### 1. API Client Implementation
- Create `src/services/chat-api.js` with POST function to `http://localhost:8000/chat`
- Implement error handling for connection failures

### 2. Chat Widget Integration
- Locate `src/components/ChatWidget` component
- Replace mock data with real API calls
- Connect input field to API trigger

### 3. State Management
- Use React Hooks (`useState`) to manage:
  - Chat messages array
  - Loading state (for "Typing..." indicator)
  - Error state (for connection failures)

### 4. Markdown Rendering
- Install and use a Markdown library (e.g., react-markdown)
- Ensure code blocks, bold text, and other formatting render correctly

## Testing

### Manual Testing
1. Start both servers (backend and frontend)
2. Open the chat widget in browser
3. Send a message and verify:
   - "Typing..." indicator appears
   - Response appears with proper Markdown formatting
   - Error handling works when backend is offline

### API Contract Verification
- Test the POST `/chat` endpoint with various message inputs
- Verify error responses when backend is unavailable
- Confirm session ID persistence across messages

## Common Issues

- **CORS errors**: Ensure backend allows requests from frontend origin
- **Connection failures**: Verify backend server is running on correct port
- **Markdown rendering**: Check that all formatting types display correctly
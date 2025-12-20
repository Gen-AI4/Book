import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Import the main FastAPI app
from backend.main import app

# For Hugging Face Spaces, we need to make sure the app is available globally
# The app will be run by the Hugging Face Spaces runtime
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
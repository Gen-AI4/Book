#!/usr/bin/env python
# Space entry point

import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Import the main FastAPI app
from backend.main import app

# Make the app available globally for Hugging Face Spaces
space_app = app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    print(f"Starting server on port {port}")
    uvicorn.run("app:space_app", host="0.0.0.0", port=port)
import sys
import os

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

print(f"Current working directory: {os.getcwd()}")
print(f"Backend path: {backend_path}")
print(f"Files in backend path: {os.listdir(backend_path)}")

try:
    print("Changing to backend directory...")
    os.chdir(backend_path)
    print(f"New working directory: {os.getcwd()}")

    print("Importing config first...")
    from config import settings
    print(f"Settings loaded: OpenAI model = {settings.openai_model}")

    print("Importing main app...")
    from main import app
    print("Successfully imported main app")

    print("Importing uvicorn...")
    import uvicorn
    print("Successfully imported uvicorn")

    print("Starting server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to continue...")
import sys
import os

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

try:
    print("Changing to backend directory...")
    os.chdir(backend_path)

    print("Importing main app...")
    from main import app
    print("Successfully imported main app")

    print("Importing uvicorn...")
    import uvicorn
    print("Successfully imported uvicorn")

    print("Starting server on port 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to continue...")
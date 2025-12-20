FROM python:3.10-slim

WORKDIR /app

# Install git (needed for some dependencies)
RUN apt-get update && apt-get install -y git

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend directory
COPY backend/ ./backend/

# Copy the app.py entry point
COPY app.py .

# Expose the port that Hugging Face Spaces expects (7860)
EXPOSE 7860

# Command to run the application
CMD ["python", "app.py"]
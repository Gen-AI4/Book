FROM python:3.10-slim

WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend directory
COPY backend/ ./backend/

# Copy the app.py entry point
COPY app.py .

# Expose the port that Hugging Face Spaces expects (7860)
EXPOSE 7860

# Command to run the application
CMD ["python", "app.py"]
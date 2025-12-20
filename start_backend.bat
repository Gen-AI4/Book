@echo off
cd /d D:\Book\backend
echo Running backend server...
python -c "from main import app; import uvicorn; print('Starting server on port 8000...'); uvicorn.run(app, host='0.0.0.0', port=8000, log_level='info')"
pause
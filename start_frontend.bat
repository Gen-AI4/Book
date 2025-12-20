@echo off
cd /d D:\Book\frontend
echo Installing frontend dependencies...
npm install
if %errorlevel% neq 0 (
    echo Failed to install dependencies, trying with legacy peer deps...
    npm install --legacy-peer-deps
)
echo Starting frontend server...
npx docusaurus start
pause
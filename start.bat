@echo off
echo Starting Energy Calculator Application...
echo.

REM Check if local model setup has been completed
findstr /C:"LM_MODEL_PATH=C:/path/to/your" backend\.env > nul
if not errorlevel 1 (
    echo NOTE: You haven't configured your local language model yet.
    echo The application will use template-based recommendations instead of AI.
    echo To set up the local model, run the backend\setup_model.bat script.
    echo.
    set /p SETUP_NOW="Would you like to set up the local model now? (y/n): "
    if /i "%SETUP_NOW%"=="y" (
        call backend\setup_model.bat
        echo Please restart this script after setting up your model.
        pause
        exit
    )
) else (
    echo Local language model is configured.
)

REM Start the backend server in a new window
start cmd /k "cd backend && python app.py"
echo Python backend started on http://localhost:5000

REM Wait a moment for the backend to initialize
timeout /t 3 /nobreak > nul

REM Get frontend dependencies if needed
if not exist node_modules (
    echo Installing frontend dependencies...
    npm install
)

REM Start the frontend application
echo Starting frontend server...
npm run dev

echo Both servers are now running!
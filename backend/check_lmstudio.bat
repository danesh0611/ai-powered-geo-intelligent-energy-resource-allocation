@echo off
echo Checking LM Studio API for Energy Calculator...
echo.

REM Check if LM Studio is running
powershell -Command "& { try { $response = Invoke-WebRequest -Uri 'http://localhost:1234/v1/models' -TimeoutSec 2; if ($response.StatusCode -eq 200) { Write-Host 'LM Studio API is running!' -ForegroundColor Green } } catch { Write-Host 'LM Studio API not detected. Starting LM Studio now...' -ForegroundColor Yellow; Start-Process 'LM Studio' } }"

echo.
echo ========================= INSTRUCTIONS ===============================
echo To enable the AI recommendations feature:
echo.
echo 1. Open LM Studio
echo 2. Select your preferred model (Qwen3 4B recommended)
echo 3. Click on the API tab in LM Studio
echo 4. Toggle on "Local Server" 
echo 5. Make sure it shows "Running on http://localhost:1234"
echo 6. Leave LM Studio running while using the application
echo =================================================================
echo.
echo Once LM Studio is running with API enabled, start the backend with:
echo python app.py
echo.
echo Press any key to continue...
pause > nul
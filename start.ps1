# Check if LM Studio is running
Write-Host "Checking for LM Studio API..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri 'http://localhost:1234/v1/models' -TimeoutSec 2 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ LM Studio API detected! AI recommendations will be available." -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️ LM Studio API not detected. AI recommendations will use template fallback." -ForegroundColor Yellow
    Write-Host ""
    $setupNow = Read-Host "Would you like to setup LM Studio for AI recommendations? (y/n)"
    if ($setupNow -eq "y") {
        & "$PSScriptRoot\backend\check_lmstudio.ps1"
    }
}

# Start the backend server in a new window
Write-Host "Starting Python backend..."
Start-Process powershell -ArgumentList "-Command", "cd '$PSScriptRoot\backend'; python app.py"
Write-Host "Python backend started on http://localhost:5000"

# Wait a moment for the backend to initialize
Write-Host "Waiting for backend to initialize..."
Start-Sleep -Seconds 3

# Check if node_modules exist, if not install dependencies
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing frontend dependencies..."
    npm install
}

# Start the frontend application
Write-Host "Starting frontend server..."
npm run dev

Write-Host "Both servers are now running!"
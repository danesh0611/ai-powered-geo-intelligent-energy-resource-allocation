# Check LM Studio API for Energy Calculator
Write-Host "Checking LM Studio API for Energy Calculator..." -ForegroundColor Cyan
Write-Host ""

# Check if LM Studio is running
try {
    $response = Invoke-WebRequest -Uri 'http://localhost:1234/v1/models' -TimeoutSec 2
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ LM Studio API is running!" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ LM Studio API not detected." -ForegroundColor Yellow
    Write-Host "Starting LM Studio now..." -ForegroundColor Yellow
    
    # Try to launch LM Studio - this assumes it's installed and in the path
    try {
        Start-Process "LM Studio"
    } catch {
        Write-Host "Could not start LM Studio automatically. Please start it manually." -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================= INSTRUCTIONS ===============================" -ForegroundColor Cyan
Write-Host "To enable the AI recommendations feature:"
Write-Host ""
Write-Host "1. Open LM Studio" -ForegroundColor White
Write-Host "2. Select your preferred model (Qwen3 4B recommended)" -ForegroundColor White
Write-Host "3. Click on the API tab in LM Studio" -ForegroundColor White
Write-Host "4. Toggle on 'Local Server'" -ForegroundColor White
Write-Host "5. Make sure it shows 'Running on http://localhost:1234'" -ForegroundColor White
Write-Host "6. Leave LM Studio running while using the application" -ForegroundColor White
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Once LM Studio is running with API enabled, start the backend with:" -ForegroundColor White
Write-Host "python app.py" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
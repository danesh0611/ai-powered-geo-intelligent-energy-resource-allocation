# Setup script for local language model
Write-Host "Setting up local language model for Energy Calculator..." -ForegroundColor Cyan
Write-Host ""

# Check if the models directory exists
if (-not (Test-Path "models")) {
    New-Item -ItemType Directory -Path "models" | Out-Null
    Write-Host "Created models directory for storing local language models."
}

Write-Host ""
Write-Host "========================= IMPORTANT ===============================" -ForegroundColor Yellow
Write-Host "You need to place your Qwen3 4B model in the models directory."
Write-Host "Please copy your qwen3-4b-q4_k_m.gguf file into the 'models' folder."
Write-Host ""
Write-Host "Then, update the .env file with the correct path to your model file."
Write-Host "For example: LM_MODEL_PATH=./models/qwen3-4b-q4_k_m.gguf"
Write-Host "==================================================================" -ForegroundColor Yellow
Write-Host ""

Write-Host "Instructions:" -ForegroundColor Green
Write-Host "1. If you haven't downloaded the model yet, you can find Qwen3 4B models at:"
Write-Host "   https://huggingface.co/collections/Qwen/qwen3-65656d13602cd4d029cebc41" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Once downloaded, copy the .gguf file to the 'models' directory"
Write-Host ""
Write-Host "3. Update the path in .env to point to your model file"
Write-Host ""

Write-Host "Press any key to open the models directory..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Open the models directory
Start-Process "explorer.exe" -ArgumentList "$PSScriptRoot\models"
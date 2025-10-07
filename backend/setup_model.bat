@echo off
echo Setting up local language model for Energy Calculator...
echo.

REM Check if the models directory exists
if not exist models mkdir models
echo Created models directory for storing local language models.

echo.
echo ========================= IMPORTANT ===============================
echo You need to place your Qwen3 4B model in the models directory.
echo Please copy your qwen3-4b-q4_k_m.gguf file into the 'models' folder.
echo.
echo Then, update the .env file with the correct path to your model file.
echo For example: LM_MODEL_PATH=./models/qwen3-4b-q4_k_m.gguf
echo =================================================================
echo.

echo Instructions:
echo 1. If you haven't downloaded the model yet, you can find Qwen3 4B models at:
echo    https://huggingface.co/collections/Qwen/qwen3-65656d13602cd4d029cebc41
echo.
echo 2. Once downloaded, copy the .gguf file to the 'models' directory
echo.
echo 3. Update the path in .env to point to your model file
echo.
echo Press any key to open the models directory...
pause > nul

start explorer %~dp0models
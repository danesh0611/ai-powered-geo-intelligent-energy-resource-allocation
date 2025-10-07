# Energy Calculator Backend

This is the Python backend for the Energy Calculator application. It provides APIs to calculate energy consumption and savings, with an optional integration with LM Studio to use your local AI models for generating personalized recommendations.

## Setup

1. Make sure Python 3.8+ is installed
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

### Using LM Studio for AI Recommendations

This backend can connect to LM Studio to use your local Qwen3 4B model for generating energy recommendations. Benefits:
- No external API calls or costs
- Privacy-preserving (all data stays on your machine)
- Customizable recommendations

#### Setting up LM Studio:

1. Download and install LM Studio from [lmstudio.ai](https://lmstudio.ai/) if you haven't already
2. Open LM Studio
3. Select your preferred model (Qwen3 4B recommended)
4. Click on the **API** tab in LM Studio
5. Toggle on **Local Server**
6. Make sure it shows "Running on http://localhost:1234"
7. Leave LM Studio running while using this application

If LM Studio is not running or the API server is not enabled, the backend will automatically fall back to template-based recommendations.

## API Endpoints

### Health Check
- `GET /api/health`
- Returns the status of the backend server

### Calculate Energy
- `POST /api/calculate-energy`
- Calculates energy consumption and potential savings based on input data
- Request body example:
  ```json
  {
    "homeSize": 2000,
    "monthlyBill": 150,
    "applianceUsage": {
      "refrigerator": 8,
      "washingMachine": 3,
      "dishwasher": 2
    }
  }
  ```
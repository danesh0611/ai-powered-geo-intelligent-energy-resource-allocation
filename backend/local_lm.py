import os
import requests
import json
from typing import Dict, Any

class LocalLM:
    """Wrapper for local language models using LM Studio API"""
    
    def __init__(self, api_base=None):
        """Initialize the connection to LM Studio API"""
        # Default URL for LM Studio's API - this is the standard port
        if api_base is None:
            # Use environment variable if set, otherwise use the default LM Studio port
            self.api_base = os.environ.get("LM_STUDIO_API_BASE", "http://localhost:1234/v1")
        else:
            self.api_base = api_base
            
        print(f"Using LM Studio API at: {self.api_base}")
        
        # Test the connection
        self.is_connected = False
        try:
            self.is_connected = self.test_connection()
            if self.is_connected:
                print("Successfully connected to LM Studio API")
            else:
                print("LM Studio API connection failed. Is LM Studio running with the API server enabled?")
        except Exception as e:
            print(f"Error connecting to LM Studio API: {e}")
    
    def test_connection(self):
        """Test the connection to the LM Studio API"""
        try:
            # Simple request to check if the API is responding
            response = requests.get(f"{self.api_base}/models")
            if response.status_code == 200:
                models = response.json()
                if isinstance(models, list) and len(models) > 0:
                    print(f"Available models: {', '.join([m.get('id', 'unknown') for m in models])}")
                return True
            return False
        except Exception:
            return False
    
    def generate_energy_recommendation(self, data: Dict[str, Any]) -> str:
        """Generate energy recommendations using LM Studio API"""
        # Extract relevant data
        location = data["location"]
        usage_type = data["usage_type"]
        system_type = data["system_type"]
        size = data["recommended_size_kw"]
        generation = data["estimated_generation_kwh"]
        savings = data["monthly_savings"]
        cost = data["system_cost"]
        payback = data["payback_years"]
        
        # Create a prompt for the model
        prompt = f"""You are an energy expert providing recommendations for renewable energy solutions.
        
Based on the following information:
- Location: {location}
- Usage Type: {usage_type}
- System Type: {system_type}
- System Size: {size} kW
- Monthly Generation: {generation} kWh
- Monthly Savings: ₹{savings}
- Total System Cost: ₹{cost}
- Payback Period: {payback} years

Generate a detailed paragraph recommending this renewable energy system. Include information about benefits, savings, and environmental impact.
Keep your response focused and concise (3-5 sentences only).
"""
        
        # Create the API request
        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers={"Content-Type": "application/json"},
                json={
                    "model": "local-model",  # LM Studio uses this as default name
                    "messages": [
                        {"role": "system", "content": "You are an energy expert assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 256
                },
                timeout=30  # Add a timeout in case the API is slow to respond
            )
            
            if response.status_code == 200:
                result = response.json()
                # Extract generated text from response
                if "choices" in result and len(result["choices"]) > 0:
                    message = result["choices"][0]["message"]
                    if "content" in message:
                        return message["content"].strip()
            
            # If we get here, something went wrong
            print(f"API Error: {response.status_code} - {response.text}")
            return f"Unable to generate recommendation. API returned: {response.status_code}"
        
        except Exception as e:
            print(f"Error calling LM Studio API: {e}")
            return "Unable to generate recommendation due to an error connecting to the local model."
    
    def is_available(self) -> bool:
        """Check if the API is available"""
        return self.is_connected


# Singleton pattern for API reuse
_api_instance = None

def get_model_instance(api_base=None):
    """Get or create a singleton API instance"""
    global _api_instance
    if _api_instance is None:
        try:
            _api_instance = LocalLM(api_base)
            if not _api_instance.is_available():
                print("WARNING: LM Studio API is not available.")
                print("Please make sure LM Studio is running and the API server is enabled.")
                print("Instructions:")
                print("1. Open LM Studio")
                print("2. Select your model (preferably Qwen3 4B)")
                print("3. Click 'API' tab")
                print("4. Toggle on 'Local Server'")
                print("5. Make sure it shows 'Running on http://localhost:1234'")
                _api_instance = None
        except Exception as e:
            print(f"Error initializing LM Studio API connection: {e}")
            _api_instance = None
    return _api_instance
    
    def generate_energy_recommendation(self, data: Dict[str, Any]) -> str:
        """Generate energy recommendations based on user data"""
        # Extract relevant data
        location = data["location"]
        usage_type = data["usage_type"]
        system_type = data["system_type"]
        size = data["recommended_size_kw"]
        generation = data["estimated_generation_kwh"]
        savings = data["monthly_savings"]
        cost = data["system_cost"]
        payback = data["payback_years"]
        
        # Create a prompt for the model
        prompt = f"""You are an energy expert providing recommendations for renewable energy solutions.
        
Based on the following information:
- Location: {location}
- Usage Type: {usage_type}
- System Type: {system_type}
- System Size: {size} kW
- Monthly Generation: {generation} kWh
- Monthly Savings: ₹{savings}
- Total System Cost: ₹{cost}
- Payback Period: {payback} years

Generate a detailed paragraph recommending this renewable energy system. Include information about benefits, savings, and environmental impact.
Keep your response focused and concise (3-5 sentences only).
"""

        # Generate response
        response = self.model(
            prompt,
            max_tokens=256,
            temperature=0.7,
            top_p=0.9,
            repeat_penalty=1.1,
            stop=["###", "\n\n"],
            echo=False
        )
        
        # Extract the generated text
        generated_text = response["choices"][0]["text"].strip()
        
        return generated_text
    
    def is_available(self) -> bool:
        """Check if the model is properly loaded and available"""
        try:
            # Try a simple generation to check if model works
            response = self.model(
                "Hello, are you working?",
                max_tokens=10,
                echo=False
            )
            return True
        except Exception:
            return False


# Singleton pattern for model reuse
_model_instance = None

def get_model_instance(model_path=None):
    """Get or create a singleton model instance"""
    global _model_instance
    if _model_instance is None:
        try:
            _model_instance = LocalLM(model_path)
        except Exception as e:
            print(f"Error loading model: {e}")
            _model_instance = None
    return _model_instance
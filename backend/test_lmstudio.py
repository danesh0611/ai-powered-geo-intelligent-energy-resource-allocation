"""
Test script to verify the LM Studio API connection
Run this to check if your LM Studio setup is working correctly
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import the local_lm module
try:
    from local_lm import get_model_instance
except ImportError as e:
    print(f"ERROR: Could not import local_lm module: {e}")
    print("Make sure you're running this from the backend directory.")
    sys.exit(1)

def main():
    """Test the LM Studio API connection"""
    print("Testing LM Studio API connection...")
    
    api_base = os.environ.get("LM_STUDIO_API_BASE", "http://localhost:1234/v1")
    print(f"Using API endpoint: {api_base}")
    
    # Try to connect to the API
    model = get_model_instance(api_base)
    
    if model is None:
        print("\n❌ Connection to LM Studio failed!")
        print("Please make sure LM Studio is running and the API server is enabled.")
        print("\nInstructions:")
        print("1. Open LM Studio")
        print("2. Select your model (preferably Qwen3 4B)")
        print("3. Click 'API' tab")
        print("4. Toggle on 'Local Server'")
        print("5. Make sure it shows 'Running on http://localhost:1234'")
        sys.exit(1)
    
    print("\n✅ Successfully connected to LM Studio API!")
    
    # Try generating a recommendation
    print("\nGenerating a test recommendation...")
    
    test_data = {
        "location": "Test City",
        "usage_type": "home",
        "system_type": "solar",
        "recommended_size_kw": 5.0,
        "estimated_generation_kwh": 600,
        "monthly_savings": 4500,
        "system_cost": 275000,
        "payback_years": 5.1
    }
    
    try:
        recommendation = model.generate_energy_recommendation(test_data)
        print("\nGenerated recommendation:")
        print("-" * 80)
        print(recommendation)
        print("-" * 80)
        print("\n✅ LM Studio is working correctly!")
    except Exception as e:
        print(f"\n❌ Error generating recommendation: {e}")
        print("API connection works but there was an error with the model generation.")
        sys.exit(1)

if __name__ == "__main__":
    main()
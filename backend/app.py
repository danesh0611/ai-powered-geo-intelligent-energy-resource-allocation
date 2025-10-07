from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import random
import math
from dotenv import load_dotenv
import time

# Import local LM module
try:
    from local_lm import get_model_instance
    USE_LOCAL_LM = True
except ImportError:
    print("Warning: Local LM module could not be imported. Using fallback method.")
    USE_LOCAL_LM = False

# Load environment variables
load_dotenv()

# Initialize LM Studio API connection if available
local_model = None
if USE_LOCAL_LM:
    try:
        # Get the API endpoint from environment variable or use default
        api_base = os.environ.get("LM_STUDIO_API_BASE", "http://localhost:1234/v1")
        local_model = get_model_instance(api_base)
        print(f"LM Studio API connection initialized: {local_model is not None}")
        if local_model is None:
            print("LM Studio API not available. Make sure LM Studio is running with the API server enabled.")
            USE_LOCAL_LM = False
    except Exception as e:
        print(f"Error initializing LM Studio API connection: {e}")
        USE_LOCAL_LM = False

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "healthy", "message": "Python backend is running"}), 200

@app.route('/api/recommend', methods=['POST'])
def recommend():
    """Generate renewable energy recommendations based on input data"""
    try:
        data = request.json
        
        # Extract data from the request
        location = data.get('location', 'Unknown')
        usage_type = data.get('usageType', 'home')
        monthly_consumption = data.get('monthlyConsumption', 0)
        
        # Get tariff either from direct tariff field or calculate from slabs
        tariff = data.get('tariff', 0)
        slabs = data.get('slabs', {})
        budget = data.get('budget')
        
        # If slabs are provided, calculate effective tariff
        if slabs:
            # Default values if not provided
            slab1_rate = slabs.get('slab1Rate', 4.0)
            slab2_rate = slabs.get('slab2Rate', 6.0)
            slab3_rate = slabs.get('slab3Rate', 8.0)
            slab4_rate = slabs.get('slab4Rate', 10.0)
            
            # Calculate total bill based on consumption slabs
            if monthly_consumption <= 0:
                total_bill = 0
            else:
                bill = 0
                remaining = monthly_consumption
                
                # Slab 1: 0-100 kWh
                units_in_slab1 = min(100, remaining)
                bill += units_in_slab1 * slab1_rate
                remaining -= units_in_slab1
                
                # Slab 2: 101-300 kWh
                if remaining > 0:
                    units_in_slab2 = min(200, remaining)  # 300-100=200
                    bill += units_in_slab2 * slab2_rate
                    remaining -= units_in_slab2
                
                # Slab 3: 301-500 kWh
                if remaining > 0:
                    units_in_slab3 = min(200, remaining)  # 500-300=200
                    bill += units_in_slab3 * slab3_rate
                    remaining -= units_in_slab3
                
                # Slab 4: >500 kWh
                if remaining > 0:
                    bill += remaining * slab4_rate
                
                # Calculate effective tariff (average cost per unit)
                tariff = bill / monthly_consumption if monthly_consumption > 0 else 0
                
                print(f"Calculated effective tariff from slabs: ₹{tariff:.2f}/unit")
                
        # If no valid tariff, use a reasonable default
        if not tariff or tariff <= 0:
            tariff = 8.0  # Default tariff
        
        # Determine system type based on usage type
        if usage_type == "home":
            system_type = "solar"
        elif usage_type == "factory":
            system_type = "wind"
        elif usage_type == "agriculture":
            # For agriculture, we'll recommend solar pumps and solar panels
            system_type = "solar"
        else:
            system_type = "solar"  # Default to solar
        
        # Simple calculations
        # In a real app, these would be based on location data, solar radiation maps, etc.
        
        # Calculate system size based on consumption and usage type
        if usage_type == "agriculture":
            # Agricultural systems typically need larger sizing for irrigation pumps
            # Assuming a 5HP pump requires about 3.7kW
            pump_requirement = 3.7
            # Base size on consumption but with a minimum for pump operations
            recommended_size_kw = max(round(monthly_consumption / 100, 1), pump_requirement)
        else:
            # Standard calculation for homes and factories
            recommended_size_kw = round(monthly_consumption / 100, 1)
        
        # Calculate expected generation - typically 4-5 kWh per kW of solar in India
        solar_multiplier = 4.2  # average daily sun hours
        wind_multiplier = 3.8   # average daily wind generation factor
        
        # Agricultural solar systems often have better positioning (open fields)
        if usage_type == "agriculture" and system_type == "solar":
            solar_multiplier = 4.5  # slightly higher for agricultural deployments
            
        # Use different multipliers based on system type
        multiplier = solar_multiplier if system_type == "solar" else wind_multiplier
        
        # Calculate estimated generation - adjusted by location factor
        location_factor = 0.9 + (hash(location) % 20) / 100  # Pseudo-random factor based on location
        estimated_generation_kwh = int(recommended_size_kw * multiplier * 30 * location_factor)
        
        # Calculate current monthly bill before solar
        current_bill = monthly_consumption * tariff
        
        # Calculate new consumption after solar (remaining grid usage)
        new_consumption = max(0, monthly_consumption - estimated_generation_kwh)
        
        # Calculate new bill after solar using slabs if provided
        if slabs:
            slab1_rate = slabs.get('slab1Rate', 4.0)
            slab2_rate = slabs.get('slab2Rate', 6.0)
            slab3_rate = slabs.get('slab3Rate', 8.0)
            slab4_rate = slabs.get('slab4Rate', 10.0)
            
            # Calculate new bill with reduced consumption
            if new_consumption <= 0:
                new_bill = 0
            else:
                new_bill = 0
                remaining = new_consumption
                
                # Slab 1: 0-100 kWh
                units_in_slab1 = min(100, remaining)
                new_bill += units_in_slab1 * slab1_rate
                remaining -= units_in_slab1
                
                # Slab 2: 101-300 kWh
                if remaining > 0:
                    units_in_slab2 = min(200, remaining)
                    new_bill += units_in_slab2 * slab2_rate
                    remaining -= units_in_slab2
                
                # Slab 3: 301-500 kWh
                if remaining > 0:
                    units_in_slab3 = min(200, remaining)
                    new_bill += units_in_slab3 * slab3_rate
                    remaining -= units_in_slab3
                
                # Slab 4: >500 kWh
                if remaining > 0:
                    new_bill += remaining * slab4_rate
        else:
            # Simple calculation if no slabs
            new_bill = new_consumption * tariff
            
        # Calculate monthly savings (difference between current and new bill)
        monthly_savings = int(current_bill - new_bill)
        
        # Calculate system cost with different rates based on usage type
        if usage_type == "agriculture":
            # Agricultural solar systems often have government subsidies
            # PM-KUSUM scheme provides subsidies for solar agricultural pumps
            base_cost = 45000  # Lower cost per kW due to subsidies
            subsidy_percentage = 0.30  # 30% subsidy
            
            # Calculate gross and net costs
            gross_cost = int(recommended_size_kw * base_cost)
            subsidy_amount = int(gross_cost * subsidy_percentage)
            system_cost = gross_cost - subsidy_amount
            
            # Store subsidy info in details for display
            subsidy_info = {
                "available": True,
                "percentage": subsidy_percentage * 100,
                "amount": subsidy_amount,
                "gross_cost": gross_cost
            }
        else:
            # Standard costs for homes and factories
            base_cost = 55000 if system_type == "solar" else 75000  # Cost per kW
            system_cost = int(recommended_size_kw * base_cost)
            subsidy_info = {"available": False}
        
        # Calculate payback period in years
        annual_savings = monthly_savings * 12
        payback_years = round(system_cost / annual_savings, 1) if annual_savings > 0 else 0
        
        # Calculate additional metrics
        co2_reduction = estimated_generation_kwh * 0.82 / 1000  # Tons of CO2 saved per month (0.82 kg/kWh in India)
        
        # Generate a summary based on the data
        gemini_summary = generate_summary(
            location, 
            usage_type, 
            system_type, 
            recommended_size_kw, 
            estimated_generation_kwh, 
            monthly_savings, 
            system_cost, 
            payback_years
        )
        
        # Prepare response with detailed breakdown
        response = {
            "location": location,
            "usage_type": usage_type,
            "system_type": system_type,
            "recommended_size_kw": recommended_size_kw,
            "estimated_generation_kwh": estimated_generation_kwh,
            "monthly_savings": monthly_savings,
            "system_cost": system_cost,
            "payback_years": payback_years,
            "gemini_summary": gemini_summary,
            "details": {
                "current_consumption": monthly_consumption,
                "remaining_consumption": new_consumption,
                "current_bill": round(current_bill, 2),
                "new_bill": round(new_bill, 2),
                "effective_tariff": round(tariff, 2),
                "co2_reduction": round(co2_reduction, 2),
                "slabs_used": bool(slabs),
                "subsidy_info": subsidy_info,
            }
        }
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def generate_summary(location, usage_type, system_type, size, generation, savings, cost, payback):
    """Generate a human-readable summary of the recommendation"""
    
    # Check if we should use local LM
    if USE_LOCAL_LM and local_model is not None:
        try:
            # Prepare the data for the local model
            data = {
                "location": location,
                "usage_type": usage_type,  # This will now include 'agriculture' as a possibility
                "system_type": system_type,
                "recommended_size_kw": size,
                "estimated_generation_kwh": generation,
                "monthly_savings": savings,
                "system_cost": cost,
                "payback_years": payback
            }
            
            # Get summary from local model
            start_time = time.time()
            summary = local_model.generate_energy_recommendation(data)
            elapsed = time.time() - start_time
            print(f"Generated recommendation using local LM in {elapsed:.2f} seconds")
            
            return summary
        except Exception as e:
            print(f"Error using local LM: {e}. Falling back to template-based summary.")
            # Fall back to template-based summary
            pass
    
    # Template-based summary generation as fallback
    # Collection of phrases to make the summary more natural
    intros = [
        f"Based on your {usage_type} in {location}, we recommend a {size} kW {system_type} energy system.",
        f"For your {usage_type} located in {location}, a {size} kW {system_type} system would be optimal.",
        f"Our analysis suggests that a {size} kW {system_type} system is ideal for your {usage_type} in {location}."
    ]
    
    generation_phrases = [
        f"This system will generate approximately {generation} kWh per month,",
        f"You can expect to generate around {generation} kWh monthly,",
        f"With average {location} conditions, you'll produce about {generation} kWh each month,"
    ]
    
    savings_phrases = [
        f"saving you ₹{savings:,} on your monthly electricity bill.",
        f"which translates to monthly savings of ₹{savings:,}.",
        f"reducing your electricity expenses by approximately ₹{savings:,} per month."
    ]
    
    investment_phrases = [
        f"The total investment of ₹{cost:,} would be recovered in {payback} years, making it a sound financial decision.",
        f"With a total cost of ₹{cost:,}, your investment will pay for itself in just {payback} years.",
        f"The system costs approximately ₹{cost:,} and offers a payback period of {payback} years."
    ]
    
    benefits = []
    if usage_type == "agriculture":
        if system_type == "solar":
            benefits = [
                "Solar pumps for irrigation eliminate diesel costs and reduce dependency on grid power.",
                "PM-KUSUM scheme offers substantial subsidies for agricultural solar installations.",
                "Solar-powered farming improves crop yield through consistent and reliable irrigation.",
                "Excess generation can be sold back to the grid for additional income."
            ]
        else:
            benefits = [
                "Renewable energy for agricultural operations reduces operational costs significantly.",
                "Government programs offer special incentives for farm-based renewable energy.",
                "Clean energy enhances sustainability credentials for farm products."
            ]
    elif system_type == "solar":
        benefits = [
            "This renewable energy solution will reduce your carbon footprint significantly.",
            "In addition to financial benefits, you'll contribute to environmental sustainability.",
            "Solar energy is maintenance-free and will provide clean electricity for 25+ years."
        ]
    else:  # wind
        benefits = [
            "Wind energy is particularly effective for industrial applications with high consumption.",
            "This wind system will operate day and night, complementing your energy needs.",
            "Industrial wind solutions provide consistent power with minimal maintenance."
        ]
    
    # Randomly select one phrase from each category
    intro = random.choice(intros)
    generation_phrase = random.choice(generation_phrases)
    savings_phrase = random.choice(savings_phrases)
    investment_phrase = random.choice(investment_phrases)
    benefit = random.choice(benefits)
    
    # Combine all parts into a coherent summary
    summary = f"{intro} {generation_phrase} {savings_phrase} {investment_phrase} {benefit}"
    
    return summary

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
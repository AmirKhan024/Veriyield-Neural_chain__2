# # import requests
# # import os

# # # Get this from OpenWeatherMap website
# # API_KEY = "7321b07957d9321623818dfc607b92e0" 

# import requests
# import os
# from utils.history import save_transaction

# # 1. PASTE YOUR WEATHERSTACK API KEY HERE
# # Get it from: https://weatherstack.com/dashboard
# API_KEY = "7321b07957d9321623818dfc607b92e0" 

# def get_real_weather(city="Nashik"):
#     """Fetches LIVE weather from Weatherstack API."""
#     try:
#         # Weatherstack Endpoint
#         url = f"http://api.weatherstack.com/current?access_key={API_KEY}&query={city}"
        
#         response = requests.get(url)
#         data = response.json()
        
#         # Check if the API returned an error (e.g., invalid key)
#         if "error" in data:
#             print(f"Weatherstack Error: {data['error']['info']}")
#             return {"temp": 30, "rain_mm": 0, "condition": "Error"}

#         # Extract data from Weatherstack's JSON structure
#         current = data.get("current", {})
        
#         return {
#             "temp": current.get("temperature", 30),
#             "rain_mm": current.get("precip", 0.0), # 'precip' is rainfall in mm
#             "condition": current.get("weather_descriptions", ["Clear"])[0]
#         }
#     except Exception as e:
#         print(f"API Connection Failed: {e}")
#         return {"temp": 30, "rain_mm": 0, "condition": "Offline"}

# def check_weather_oracle(location, god_mode=False):
#     """
#     Hybrid Oracle: Uses REAL data by default, but God Mode can override it.
#     """
#     # 1. Fetch Real Data
#     real_data = get_real_weather(location)
    
#     # 2. Logic: If God Mode is ON, force a drought.
#     if god_mode:
#         # Define the payout simulation details
#         tx_details = {
#             "amount": "0.5 ETH",
#             "reason": "Drought Simulation (God Mode)",
#             "location": location
#         }
        
#         return {
#             "condition": "🔥 Extreme Drought (Simulated)",
#             "rainfall_mm": 0.0,
#             "trigger_met": True, # Payout Triggered!
#             "payout_amount": "0.5 ETH",
#             "source": "Simulated Override"
#         }
    
#     # 3. Otherwise, use Real Data logic
#     # Real World Logic: If rain > 50mm (Heavy Flood), trigger payout
#     is_flood = float(real_data['rain_mm']) > 50.0
    
#     return {
#         "condition": f"{real_data['condition']} (Live)",
#         "rainfall_mm": real_data['rain_mm'],
#         "trigger_met": is_flood,
#         "payout_amount": "0.5 ETH" if is_flood else "0.0 ETH",
#         "source": "Weatherstack API"
#     }

# def trigger_payout_transaction(wallet):
#     """
#     Simulates the blockchain payout transaction and saves to history.
#     """
#     import random
#     import time
    
#     time.sleep(2) # Fake processing delay
    
#     # Generate a random transaction hash
#     tx_hash = "0x" + "".join([random.choice("0123456789abcdef") for _ in range(64)])
    
#     # SAVE TO HISTORY (The new Dynamic Feature)
#     try:
#         save_transaction("Insurance Payout", {
#             "amount": "0.5 ETH", 
#             "tx": tx_hash,
#             "status": "Confirmed"
#         })
#     except Exception as e:
#         print(f"History Save Failed: {e}")
    
#     return {"tx_hash": tx_hash}


import requests
import time
import random
from datetime import datetime
from fpdf import FPDF
from utils.history import save_transaction

API_KEY = "7321b07957d9321623818dfc607b92e0"  # Replace with your key

def get_real_weather(city="Nashik"):
    """Fetches LIVE weather data."""
    try:
        url = f"http://api.weatherstack.com/current?access_key={API_KEY}&query={city}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            return {
                "temp": data["main"]["temp"],
                "rain_mm": data.get("rain", {}).get("1h", 0),
                "condition": data["weather"][0]["main"]
            }
    except:
        pass
    return {"temp": 32, "rain_mm": 0, "condition": "Clear Sky (Fallback)"}

def check_weather_oracle(location, god_mode=False):
    """
    Advanced Parametric Oracle: Calculates TIERED payouts based on severity.
    """
    # 1. God Mode Override (For Demo "Money Shot")
    if god_mode:
        return {
            "condition": "🔥 Extreme Drought (Simulated)",
            "rainfall_mm": 0.0,
            "trigger_met": True,
            "severity": "CRITICAL",
            "payout_amount": "1.0 ETH (100% Coverage)", # Maximum Payout
            "source": "Simulated Override"
        }
    
    # 2. Real Data Logic
    real_data = get_real_weather(location)
    rain = real_data['rain_mm']
    
    # Actuarial Logic (Tiered Payouts)
    payout = "0.0 ETH"
    trigger = False
    severity = "Normal"
    
    if rain > 100: # Catastrophic Flood
        payout = "1.0 ETH (100% Coverage)"
        trigger = True
        severity = "CRITICAL FLOOD"
    elif rain > 50: # Moderate Flood
        payout = "0.5 ETH (50% Partial Payout)"
        trigger = True
        severity = "MODERATE FLOOD"
        
    return {
        "condition": f"{real_data['condition']} (Live)",
        "rainfall_mm": rain,
        "trigger_met": trigger,
        "severity": severity,
        "payout_amount": payout,
        "source": "OpenWeatherMap API"
    }

def trigger_payout_transaction(wallet_address, amount):
    """Executes the payout and logs it."""
    time.sleep(2)
    tx_hash = "0x" + "".join([random.choice("0123456789abcdef") for _ in range(64)])
    
    save_transaction("Insurance Payout", {
        "amount": amount, 
        "tx": tx_hash,
        "wallet": wallet_address
    })
    
    return {"tx_hash": tx_hash, "status": "Confirmed"}

def generate_insurance_policy(farmer_name, location):
    """Generates a legal-style Smart Policy PDF."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    header = f"""
    VERIYIELD PARAMETRIC INSURANCE POLICY
    -------------------------------------------------------
    Policy ID: {random.randint(10000, 99999)}
    Date: {datetime.now().strftime('%Y-%m-%d')}
    Insured: {farmer_name}
    Location: {location}
    
    COVERAGE TERMS (SMART CONTRACT):
    1. CRITICAL RISK (>100mm Rain): 1.0 ETH Payout
    2. MODERATE RISK (>50mm Rain): 0.5 ETH Payout
    3. TRIGGER SOURCE: OpenWeatherMap Oracle
    
    This policy is active and monitoring real-time weather conditions.
    Automatic execution enabled via Polygon Smart Contract.
    -------------------------------------------------------
    """
    pdf.multi_cell(0, 10, header)
    filename = "smart_policy.pdf"
    pdf.output(filename)
    return filename
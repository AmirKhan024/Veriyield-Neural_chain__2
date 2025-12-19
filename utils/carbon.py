import random
import time

def calculate_green_score(inputs):
    """
    Calculates Regenerative Score based on Cool Farm Tool principles.
    Base Score: 100
    """
    score = 100
    details = []
    
    # Logic: Add points for sustainable practices
    if inputs.get('tillage') == 'No-Till':
        score += 20
        details.append("✅ +20: No-Till Soil Conservation")
    
    if inputs.get('irrigation') == 'Drip':
        score += 15
        details.append("✅ +15: Water Conservation (Drip)")
        
    if inputs.get('fertilizer') == 'Organic':
        score += 15
        details.append("✅ +15: Chemical-Free Input")
        
    if inputs.get('cover_crop'):
        score += 10
        details.append("✅ +10: Cover Cropping")

    return {
        "total_score": score,
        "breakdown": details,
        "eligible_tokens": int(score * 0.5) # Example: 150 score = 75 AgriTokens
    }

def mint_carbon_tokens(address, amount):
    """
    SIMULATION: Generates a fake transaction hash.
    Does NOT connect to real blockchain.
    """
    time.sleep(1.5) # Fake network delay
    
    # Generate a random hex string that looks exactly like a Polygon hash
    mock_hash = "0x" + "".join([random.choice("0123456789abcdef") for _ in range(64)])
    
    return {
        "tx_hash": mock_hash,
        "amount": amount,
        "status": "Minted"
    }
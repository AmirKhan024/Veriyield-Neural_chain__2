"""
Blockchain Integration Module
Handles real interaction with Polygon Amoy Testnet (with Mock Fallback)
"""

import os
import json
import hashlib
import time
from datetime import datetime
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- MINIMAL ABI (The Interface to talk to the Contract) ---
# We assume a simple contract function: storeCropData(string memory _data)
SIMPLE_ABI = [
    {
        "inputs": [{"internalType": "string", "name": "_data", "type": "string"}],
        "name": "storeCropData",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

class BlockchainManager:
    """Manages blockchain interactions for crop verification"""
    
    def __init__(self):
        """Initialize Web3 connection"""
        # Polygon Amoy Testnet RPC
        self.rpc_url = os.getenv("POLYGON_RPC_URL", "https://rpc-amoy.polygon.technology/")
        self.private_key = os.getenv("WALLET_PRIVATE_KEY")
        self.contract_address = os.getenv("CONTRACT_ADDRESS")
        
        try:
            self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
            self.is_connected = self.w3.is_connected()
            if self.is_connected:
                print("✅ Connected to Polygon Amoy")
            else:
                print("⚠️ Blockchain Disconnected - Switching to Mock Mode")
        except:
            self.is_connected = False

    def create_crop_record(self, crop_data):
        """
        Create a blockchain record for crop analysis.
        Attempts REAL transaction first; falls back to MOCK if keys are missing.
        """
        # 1. Check if we have everything needed for a REAL transaction
        if self.is_connected and self.private_key and self.contract_address:
            try:
                return self._send_real_transaction(crop_data)
            except Exception as e:
                print(f"❌ Real Transaction Failed ({e}). Using Mock.")
                return self._mock_transaction(crop_data)
        
        # 2. Otherwise, use Mock
        else:
            return self._mock_transaction(crop_data)

    def _send_real_transaction(self, crop_data):
        """Writes data to the Polygon Blockchain"""
        account = self.w3.eth.account.from_key(self.private_key)
        
        # Initialize Contract
        contract = self.w3.eth.contract(address=self.contract_address, abi=SIMPLE_ABI)
        
        # Prepare Data string (JSON)
        data_string = json.dumps(crop_data)
        
        # Build Transaction
        tx = contract.functions.storeCropData(data_string).build_transaction({
            'from': account.address,
            'nonce': self.w3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        # Sign & Send
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        # Wait for receipt (Optional - for speed we might just return hash)
        print(f"🚀 Transaction Sent! Hash: {self.w3.to_hex(tx_hash)}")
        
        return {
            "success": True,
            "transaction_hash": self.w3.to_hex(tx_hash),
            "network": "Polygon Amoy (Real)",
            "timestamp": datetime.now().isoformat(),
            "crop_data": crop_data,
            "explorer_link": f"https://amoy.polygonscan.com/tx/{self.w3.to_hex(tx_hash)}"
        }

    def _mock_transaction(self, crop_data):
        """Create mock blockchain transaction for demo"""
        # Create a deterministic hash based on crop data to look real
        data_string = json.dumps(crop_data, sort_keys=True)
        tx_hash = hashlib.sha256(data_string.encode()).hexdigest()
        
        return {
            "success": True,
            "transaction_hash": f"0x{tx_hash}",
            "network": "Polygon Amoy Testnet (Simulated)",
            "timestamp": datetime.now().isoformat(),
            "crop_data": crop_data,
            "explorer_link": "#"
        }

# Initialize global instance
blockchain_manager = BlockchainManager()
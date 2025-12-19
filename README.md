# 🌾 VeriYield Neural-Chain Protocol
> **The Autonomous "Farm-to-Finance" Operating System.**
> *Built for the ML Mumbai GenAI Hackathon 2025 | AgriTech Track*

![Status](https://img.shields.io/badge/Status-Hackathon_MVP-success?style=for-the-badge&logo=git)
![AI](https://img.shields.io/badge/AI-Llama_4_Vision_%7C_LangGraph-blueviolet?style=for-the-badge)
![Stack](https://img.shields.io/badge/Stack-Streamlit_%7C_Python-FF4B4B?style=for-the-badge)
![DeFi](https://img.shields.io/badge/DeFi-Polygon_Amoy_%7C_Parametric-blue?style=for-the-badge)

---

## 📂 1. Project Structure
VeriYield is built on a modular, micro-service architecture powered by Python. Here is how the codebase is organized:

```text
VeriYield-Neural-Chain/
├── 📄 app.py                   # MAIN ENTRY POINT: The Streamlit Dashboard & UI Logic
├── 📄 requirements.txt         # Dependency list (LangGraph, Groq, Streamlit, etc.)
├── 📄 .env                     # Configuration (API Keys for Groq, OpenWeatherMap)
├── 📄 veriyield_db.json        # Local Database (Persists Wallet & Transaction History)
│
└── 📁 utils/                   # THE BRAIN (Backend Modules)
    ├── 📄 __init__.py          # Package initializer
    ├── 📄 vision.py            # VISION ENGINE: Llama-4-Scout integration for FCI Grading
    ├── 📄 market_agent.py      # COMMERCE ENGINE: "Raju Bhai" LangGraph Negotiator
    ├── 📄 rag.py               # RESEARCH ENGINE: Web-Search Agent (DuckDuckGo + Llama-3)
    ├── 📄 insurance.py         # DEFI ENGINE: Parametric Weather Oracle & Smart Policies
    ├── 📄 carbon.py            # REFI ENGINE: Sustainability Logic & Visual Proof Verification
    ├── 📄 history.py           # STORAGE: Handles transaction logging and persistence
    └── 📄 blockchain.py        # LEDGER: Simulates Polygon Amoy interactions


VeriYield
VeriYield Neural-Chain is a decentralized protocol designed to bridge the gap between Physical Agriculture and Digital Finance.

While current agricultural apps are passive—merely displaying data—VeriYield is Agentic. It uses autonomous AI agents to execute complex financial and logistical tasks that usually require human intermediaries.

🚩 The Core Problem
The agricultural sector currently suffers from systemic inefficiencies:

Information Asymmetry: Farmers often don't know the real market price, allowing middlemen to exploit the gap.

Subjective Grading: Crop quality is often visually guessed, leading to unfair rejections and pricing.

Slow Insurance: Insurance claims can take months to process after a disaster, leaving farmers vulnerable.

🚀 The VeriYield Solution
VeriYield deploys a Multi-Agent System to automate and secure the supply chain:

AI Vision Agents: Scientifically prove crop quality based on FCI Standards, removing subjective bias.

Research Agents: Perform live web searches to identify real-time market prices, ensuring fair value.

Negotiation Agents: Autonomously haggle with buyers to secure the best possible deals for farmers.

Smart Contracts: Execute instant insurance payouts based on verifiable weather triggers.



graph TD
    User[👨‍🌾 Farmer] -->|1. ZK Login| Identity[🔐 Identity Layer]
    Identity -->|Fetch Land Record| AgriStack[📍 AgriStack Simulation]
    
    User -->|2. Upload Photo| Vision[📸 Llama-4 Vision Engine]
    Vision -->|JSON: FCI Grade| Brain{🧠 Central Intelligence}
    
    Brain -->|Trigger| RAG[🕵️ Research Agent]
    RAG -->|Web Search| Duck[🌐 DuckDuckGo]
    Duck -->|Live Prices| RAG
    
    Brain -->|Grade + Price| Raju[🤝 'Raju Bhai' Negotiator]
    Raju -->|Final Deal| User
    
    Brain -->|Visual Proof| Carbon[🌍 Sustainability Auditor]
    Carbon -->|Verify No-Till| Mint[🪙 Mint Carbon Credits]
    
    Oracle[☔ Weather Oracle] -->|3. Monitor Rain| Insurance[🛡️ Parametric Contract]
    Insurance -->|Trigger >50mm| Payout[💰 Wallet Transfer]



🔍 Step-by-Step Execution Flow
Phase 1: The Trust Layer (Identity)
Input: User clicks "Connect Identity."

Process: The app simulates a Zero-Knowledge Proof (ZKP) via Anon Aadhaar to verify the user is a resident of Maharashtra without revealing their ID number.

AgriStack Integration: Simultaneously, the system fetches mock land records (Survey No. 24/A) to prove the user actually owns farmland.

Phase 2: The Perception Layer (Vision)
Input: User uploads a photo of a diseased or healthy crop.

Engine: utils/vision.py uses Llama-4-Scout.

Output: It generates a strict JSON containing the FCI Grade (Grade A/B), visual defects, and a "Search Term" (e.g., "Early Blight Tomato Fungicide 2025").

Phase 3: The Intelligence Layer (LangGraph RAG)
Trigger: The JSON from Phase 2 is passed to utils/rag.py.

Agent Workflow:

Researcher Node: Takes the "Search Term" and crawls the live web (DuckDuckGo) for real-time market prices in Nashik and new treatment protocols.

Analyst Node: Synthesizes this raw data into a professional advisory report.

Phase 4: The Commerce Layer (Negotiation)
Persona: "Raju Bhai" (Senior Commission Agent).

Engine: utils/market_agent.py uses LangGraph.

Logic: The agent doesn't guess prices. It looks at the Live Market Data found in Phase 3. If the web says ₹20/kg, Raju Bhai uses that as a baseline to negotiate, while using "Hinglish" trade lingo to build rapport.

Phase 5: The DeFi Layer (Insurance & Carbon)
Insurance: utils/insurance.py hits the OpenWeatherMap API. If rainfall exceeds specific thresholds (e.g., 50mm for Moderate, 100mm for Critical), a Smart Contract automatically executes a payout to the farmer's wallet.

Sustainability: utils/carbon.py asks for "Visual Proof" of eco-friendly farming (e.g., a photo of drip irrigation). The AI analyzes this photo to verify the claim before minting ERC-20 Carbon Credit tokens.

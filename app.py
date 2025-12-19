import streamlit as st
import time
import pandas as pd
import numpy as np
from datetime import datetime
import io
import random

# --- CUSTOM MODULE IMPORTS ---
from utils.vision import analyze_crop_disease
from utils.insurance import check_weather_oracle, trigger_payout_transaction,generate_insurance_policy

from utils.carbon import calculate_green_score, mint_carbon_tokens
from utils.history import load_history, save_transaction
from utils.rag import agent_chain
from utils.market_agent import broker_agent
# Try to import Qrcode (Fail gracefully if not installed)
try:
    import qrcode
except ImportError:
    qrcode = None



from fpdf import FPDF




def generate_quality_pdf(result):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="VeriYield - FCI Quality Certificate", ln=1, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Grade: {result.get('fci_grade', 'N/A')}", ln=1)
    pdf.cell(200, 10, txt=f"Defects: {', '.join(result.get('visual_defects', []))}", ln=1)
    pdf.cell(200, 10, txt=f"Confidence: {result.get('confidence', 'N/A')}", ln=1)
    pdf.cell(200, 10, txt=f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1)
    
    # Save to a temporary file
    filename = "quality_certificate.pdf"
    pdf.output(filename)
    return filename

# --- CONFIGURATION ---
st.set_page_config(layout="wide", page_title="VeriYield Protocol", page_icon="🌾")

# --- SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'crop_data' not in st.session_state: st.session_state.crop_data = None
if 'last_analysis' not in st.session_state: st.session_state.last_analysis = None
if 'user_input' not in st.session_state: st.session_state.user_input = ""

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .verified-badge { 
        background-color: #E3F2FD; color: #1565C0; padding: 4px 12px; 
        border-radius: 20px; font-size: 0.8rem; border: 1px solid #90CAF9; 
        display: inline-block; margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: GOD MODE ---
with st.sidebar:
    st.title("⚙️ Protocol Admin")
    st.info("Simulating Polygon Amoy Network")
    god_mode = st.toggle("⚡ God Mode (Force Drought)", value=False)
    st.caption("Toggle to trigger Insurance Payout demo.")
    st.divider()
    st.caption("VeriYield Neural-Chain v2.0")
    st.divider()
    st.markdown("### 🎒 Farmer Wallet")

    
    history = load_history()

    # Calculate Balance dynamically
    balance = 0
    for h in history:
        if "ETH" in str(h['details']):
            balance += 0.5 # Simple logic for demo

    st.metric("Wallet Balance", f"{balance} ETH")

    with st.expander("📜 Transaction History"):
        for h in reversed(history[-5:]): # Show last 5
            st.caption(f"{h['timestamp']} - {h['type']}")
            st.code(h['details'].get('tx', 'N/A')[:10] + "...", language="text")

# --- LOGIN LAYER: ZK-IDENTITY ---
# --- LOGIN LAYER: ZK-IDENTITY & AGRISTACK ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'> VeriYield Protocol</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Decentralized Agricultural Risk & Commerce Layer</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.info("Authenticating via Anon Aadhaar (ZK-Proof)...")
        
        # The Button
        if st.button("Connect Identity (Zero-Knowledge)", type="primary", use_container_width=True):
            with st.spinner("Generating Cryptographic Proof..."):
                time.sleep(1.5) # Fake ZK generation delay
                st.success("✅ Proof Verified: Resident of Maharashtra (Valid Aadhaar)")
                time.sleep(0.5)
                
                # --- NEW: AGRISTACK LAND FETCH (The Missing Feature) ---
                with st.status("Fetching AgriStack Land Records...", expanded=True):
                    time.sleep(0.8)
                    st.write(" Locating Survey No. 24/A (Nashik)...")
                    time.sleep(0.5)
                    st.write(" Verifying Land Polygon Geometry...")
                    time.sleep(0.5)
                    st.write(" Linking Identity to Farmland Registry...")
                    time.sleep(0.5)
                
                # Save Mock Land Data for the Map later
                st.session_state.land_coords = {
                    'lat': [19.9975], 
                    'lon': [73.7898]
                }
                
                st.session_state.logged_in = True
                st.rerun()

else:
    # --- MAIN APPLICATION ---
    st.markdown("## 🌾 VeriYield Dashboard")
    
    # The 5 Pillars of the Protocol
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Vision & Grading", 
        "Supply Chain & Trust",
        "Insurance (DeFi)", 
        "Market Negotiator",
        "Sustainability"
    ])

    # --- TAB 1: VISION & FCI GRADING ---
    with tab1:
        st.subheader("FCI-Standard Quality Assayer")
        col_img, col_metrics = st.columns([1, 1])
        
        with col_img:
            img = st.file_uploader("Upload Crop Image", type=['jpg', 'png', 'jpeg'])
            if img:
                st.image(img, caption="Field Capture", use_column_width=True)
        
        with col_metrics:
            if img and st.button("Analyze Quality", type="primary"):
                with st.spinner("Running Llama-Vision Assayer..."):
                    result = analyze_crop_disease(img)
                    st.session_state.crop_data = result
                    st.session_state.last_analysis = result # For Tab 2 compatibility
                    
                    # Display Results
                    st.markdown(f"### Grade: {result.get('fci_grade', 'N/A')}")
                    
                    m1, m2 = st.columns(2)
                    m1.metric("Est. Size", result.get('estimated_size_mm', 'N/A'))
                    m2.metric("Confidence", result.get('confidence', 'N/A'))
                    
                    st.write("**Visual Defects:**")
                    st.write(", ".join(result.get('visual_defects', ['None'])))
                    
                    st.info(f"**Explanation:** {result.get('explanation', 'Analysis complete.')}")
                    st.divider()
                    st.subheader("🧠 Multi-Modal Research Agent")
                    
                    with st.status("🕵️ Agent is searching the web...", expanded=True) as status:
                        st.write(f"🔍 Searching: '{result.get('search_term', 'Crop disease treatment')}'")
                        st.write("🌐 Browsing: agmarknet.gov.in, amazon.in, krishijagran.com...")
                        
                        # CALL THE LANGGRAPH AGENT
                        advisory = agent_chain.generate_detailed_advisory(
                            disease_data=result,
                            weather_context="Live", # Agent fetches this automatically now
                            market_context="Live"
                        )
                        status.update(label="✅ Research Complete!", state="complete", expanded=False)
                    
                    # Display the Agent's Report
                    st.markdown(advisory)
                    
                    if result.get('fci_grade') == 'Grade A':
                        st.balloons()
                        pdf_file = generate_quality_pdf(result)
                        with open(pdf_file, "rb") as f:
                            st.download_button(
                                label="📄 Download FCI Quality Certificate",
                                data=f,
                                file_name="VeriYield_Certificate.pdf",
                                mime="application/pdf"
                            )


    # --- TAB 2: SUPPLY CHAIN (SIMULATED BLOCKCHAIN) ---
    with tab2:
        st.subheader("🚛 AI Logistics & Blockchain Passport")
        
        # 1. Map Logic (Nashik -> Mumbai)
        map_data = pd.DataFrame({
            'lat': [19.9975, 19.0330], 
            'lon': [73.7898, 73.0297],
            'type': ['Farm (Origin)', 'Market (Destination)']
        })
        
        col_map, col_stats = st.columns([2, 1])
        with col_map:
            st.map(map_data, zoom=7, use_container_width=True)
        with col_stats:
            st.success("✅ Route Optimized")
            st.metric("Distance", "167 km")
            st.metric("Est. Time", "3 hrs 42 mins")
            st.caption("AI avoided traffic on NH-160")
            
        st.divider()

        # 2. Blockchain Logic
        st.markdown("### ⛓️ Immutable Quality Record")
        
        if not st.session_state.last_analysis:
            st.warning("⚠️ Please analyze a crop in Tab 1 first.")
        else:
            result = st.session_state.last_analysis
            col_a, col_b = st.columns([1, 1])
            
            with col_a:
                st.info("📦 **Asset to Tokenize:**")
                st.json(result)
            
            with col_b:
                st.write("### 🚀 Commit to Polygon")
                if st.button("🔗 Mint Quality Token (Polygon Amoy)", type="primary"):
                    
                    with st.spinner("Encrypting Data & Mining Block..."):
                        # --- SAFE SIMULATION LOGIC ---
                        # Try to use the blockchain manager, but fallback to local sim if it fails
                        try:
                            from utils.blockchain import blockchain_manager
                            tx_receipt = blockchain_manager.create_crop_record(result)
                        except Exception:
                            # Local Simulation Fallback (Safe Mode)
                            time.sleep(2)
                            fake_hash = "0x" + "".join([random.choice("0123456789abcdef") for _ in range(64)])
                            tx_receipt = {
                                "success": True,
                                "transaction_hash": fake_hash,
                                "network": "Polygon Amoy Testnet (Simulated)",
                                "timestamp": datetime.now().isoformat(),
                                "explorer_link": "https://amoy.polygonscan.com/tx/" + fake_hash
                            }
                        
                    if tx_receipt['success']:
                        st.balloons()
                        st.success("✅ Transaction Confirmed!")
                        
                        # --- QR CODE PASSPORT VISUALIZATION ---
                        st.markdown("---")
                        st.markdown("### 🎫 Digital Product Passport")
                        
                        c1, c2, c3 = st.columns([1, 2, 1])
                        
                        # QR Code
                        with c1:
                            if qrcode:
                                qr = qrcode.make(tx_receipt['explorer_link'])
                                img_byte_arr = io.BytesIO()
                                qr.save(img_byte_arr, format='PNG')
                                st.image(img_byte_arr.getvalue(), caption="Scan to Verify", width=120)
                            else:
                                st.warning("Install 'qrcode' library")

                        # Certificate Details
                        with c2:
                            st.markdown(f"**Network:** `{tx_receipt['network']}`")
                            st.markdown(f"**Block Time:** `{tx_receipt['timestamp']}`")
                            st.markdown(f"[🔎 View on PolygonScan]({tx_receipt['explorer_link']})")
                            
                        # Badge
                        with c3:
                            st.markdown("""
                            <div style="text-align: center; border: 2px solid #4CAF50; border-radius: 10px; padding: 10px; background: #E8F5E9;">
                                <h3 style="color: #4CAF50; margin:0;">VERIFIED</h3>
                                <small>VeriYield Audit</small>
                            </div>
                            """, unsafe_allow_html=True)
                            
                        st.caption("Transaction Hash")
                        st.code(tx_receipt['transaction_hash'], language="text")

    # --- TAB 3: PARAMETRIC INSURANCE ---
    # --- TAB 3: PARAMETRIC INSURANCE (Advanced) ---
    with tab3:
        st.subheader("☔ Parametric Insurance Oracle")
        st.caption("Smart Contract auto-claims based on Weather Oracle data.")
        
        # 1. Policy Download Section (New!)
        with st.expander("📄 Active Smart Policy Details", expanded=False):
            st.info("Policy #8492 active for Nashik Region.")
            from utils.insurance import generate_insurance_policy
            if st.button("Download Signed Policy Document"):
                pdf_path = generate_insurance_policy("Ramesh Patil", "Nashik")
                with open(pdf_path, "rb") as f:
                    st.download_button("Download PDF", f, "VeriYield_Policy.pdf", "application/pdf")

        st.divider()

        # 2. Oracle Monitor
        status = check_weather_oracle("Nashik", god_mode)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Live Rainfall", f"{status['rainfall_mm']} mm")
            # Show Severity Badge
            if status['severity'] == "Normal":
                st.success(f"Condition: {status['condition']}")
            else:
                st.error(f"⚠️ Condition: {status['severity']}")
        
        with col_b:
            if status['trigger_met']:
                st.error("🚨 PARAMETRIC TRIGGER ACTIVATED")
                st.markdown(f"**Payout Tier:** {status['payout_amount']}")
                
                if st.button("Execute Smart Contract Payout"):
                    with st.spinner("Verifying Oracle Data & Transferring Funds..."):
                        # Pass the calculated amount to the transaction
                        tx = trigger_payout_transaction("0xUserWallet", status['payout_amount'])
                        st.success(f"💰 Funds Transferred: {status['payout_amount']}")
                        st.code(tx['tx_hash'], language="text")
            else:
                st.success("✅ Risk Threshold Not Breached.")
                st.caption("System monitoring for >50mm Rainfall.")
    # --- TAB 4: MARKET NEGOTIATOR ---
   # --- TAB 4: MARKET NEGOTIATOR (The "Raju Bhai" Agent) ---
    with tab4:
        st.subheader("🤝 e-NAM Smart-Mandi (Live)")
        
        if not st.session_state.crop_data:
            st.warning("⚠️ Please analyze a crop in Tab 1 first.")
        else:
            c1, c2 = st.columns([1, 4])
            with c1: st.image("https://cdn-icons-png.flaticon.com/512/4529/4529995.png", width=80)
            with c2: 
                st.markdown(f"**Agent:** {broker_agent.name} (Senior Broker)")
                st.caption("📍 Location: Nashik Mandi | 🟢 Status: Online")
            
            st.divider()
            chat_container = st.container(height=400)
            
            # Display History
            with chat_container:
                if not st.session_state.chat_history:
                    crop = st.session_state.crop_data.get('crop_type', 'Crop')
                    greeting = f"Ram Ram Sir ji! I see you have some {crop}. Market is busy today. What is your expected rate (Bhaav)?"
                    st.session_state.chat_history.append({"role": "assistant", "content": greeting})
                
                for msg in st.session_state.chat_history:
                    avatar = "👳" if msg['role'] == "assistant" else "👨‍🌾"
                    st.chat_message(msg['role'], avatar=avatar).write(msg["content"])

            # Chips
            st.markdown("### 🗣️ Quick Actions")
            cols = st.columns(4)
            if cols[0].button("📈 Market Trend?"): st.session_state.user_input = "What is the market trend?"
            if cols[1].button("🚚 Arrivals?"): st.session_state.user_input = "How many trucks arrived today?"
            if cols[2].button("💰 Best Price?"): st.session_state.user_input = "Give me your best final rate."
            if cols[3].button("🛑 Should I hold?"): st.session_state.user_input = "Should I sell now or wait?"

            # Input
            prompt = st.chat_input("Message Raju Bhai...")
            if prompt: st.session_state.user_input = prompt

            if st.session_state.user_input:
                user_msg = st.session_state.user_input
                st.session_state.user_input = "" # Clear input
                
                # Show User Message
                st.session_state.chat_history.append({"role": "user", "content": user_msg})
                with chat_container: st.chat_message("user", avatar="👨‍🌾").write(user_msg)
                
                # Show AI Response
                with st.spinner(f"{broker_agent.name} is checking rates..."):
                    response = broker_agent.chat_with_broker(st.session_state.chat_history, st.session_state.crop_data, user_msg)
                
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                with chat_container: st.chat_message("assistant", avatar="👳").write(response)
                st.rerun()
    # --- TAB 5: SUSTAINABILITY ---
    # --- TAB 5: SUSTAINABILITY (Fixed Logic) ---
    # --- TAB 5: SUSTAINABILITY (With AI "Proof of Green") ---
    with tab5:
        st.subheader("🌍 Regenerative Farming Audit (AI-Verified)")
        
        # Import the new function
        from utils.vision import verify_sustainable_practice

        with st.form("carbon_audit"):
            st.info("📝 Self-Reporting Protocol")
            c1, c2 = st.columns(2)
            with c1:
                tillage = st.selectbox("Tillage Method", ["Conventional", "No-Till (+20 pts)"])
                irrigation = st.selectbox("Irrigation Type", ["Flood", "Drip (+15 pts)", "Sprinkler"])
            with c2:
                fertilizer = st.selectbox("Fertilizer", ["Synthetic", "Organic (+15 pts)"])
                cover_crop = st.checkbox("Used Cover Crops? (+10 pts)")
            
            st.divider()
            st.info("📸 Proof of Work (Required for High Scores)")
            audit_img = st.file_uploader("Upload Field Photo for AI Verification", type=['jpg', 'png'])
            
            submitted = st.form_submit_button("Run AI Audit & Calculate Score")
            
        if submitted:
            # 1. Base Calculation
            inputs = {
                "tillage": "No-Till" if "No-Till" in tillage else "Conventional",
                "irrigation": "Drip" if "Drip" in irrigation else "Flood",
                "fertilizer": "Organic" if "Organic" in fertilizer else "Synthetic",
                "cover_crop": cover_crop
            }
            base_result = calculate_green_score(inputs)
            final_score = base_result['total_score']
            
            # 2. AI Verification Layer (The "Advanced" Upgrade)
            verification_bonus = False
            if audit_img:
                with st.spinner("🤖 AI Auditor is inspecting the field..."):
                    # We verify the highest value claim (e.g., No-Till or Drip)
                    claim_to_check = inputs['tillage'] if inputs['tillage'] == 'No-Till' else inputs['irrigation']
                    audit_result = verify_sustainable_practice(audit_img, claim_to_check)
                    
                    if audit_result.get('verified'):
                        st.success(f"✅ AI Verified: {claim_to_check}")
                        st.caption(f"Evidence: {audit_result.get('evidence')}")
                        final_score += 20 # BONUS for Verified Proof
                        verification_bonus = True
                    else:
                        st.error(f"❌ AI Rejection: Could not verify {claim_to_check}")
                        st.caption(f"Reason: {audit_result.get('evidence')}")
            
            # 3. Save to Session State
            st.session_state.carbon_result = {
                "score": final_score,
                "tokens": int(final_score * 0.5),
                "breakdown": base_result['breakdown']
            }
            if verification_bonus:
                st.session_state.carbon_result['breakdown'].append("🌟 +20: AI Visual Proof Bonus")

        # 4. Results & Minting
        if 'carbon_result' in st.session_state:
            res = st.session_state.carbon_result
            
            st.metric("VeriYield Green Score", f"{res['score']}/170")
            for item in res['breakdown']: st.caption(item)
                
            if res['score'] > 100:
                st.success(f"🎉 Eligible for {res['tokens']} AgriTokens!")
                if st.button("Mint Carbon Credits (ERC-20)"):
                    with st.spinner("Minting on Polygon..."):
                        tx = mint_carbon_tokens("0xUser", res['tokens'])
                        st.balloons()
                        st.success(f"Minted {res['tokens']} Tokens!")
                        st.code(tx['tx_hash'], language="text")
            else:
                st.warning("Score too low. Upload photo proof to boost score!")
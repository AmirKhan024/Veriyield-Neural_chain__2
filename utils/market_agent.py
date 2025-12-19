import os
from typing import TypedDict, List
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# --- 1. SETUP & CONFIGURATION ---
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize Fast Llama Model (The Brain)
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7 
)

# Initialize Search Tool (The Eyes)
search_tool = DuckDuckGoSearchRun()

# --- 2. DEFINE AGENT STATE ---
class AgentState(TypedDict):
    """
    The Memory of our Agent.
    - messages: The chat history.
    - crop_name: What we are selling.
    - crop_grade: The quality (A/B).
    - market_intel: The REAL prices found on the web.
    """
    messages: List[str] 
    crop_name: str
    crop_grade: str
    market_intel: str

# --- 3. DEFINE NODES (The Actions) ---

def market_research_node(state: AgentState):
    """
    Step 1: Research.
    If we don't have market data yet, search the web for REAL prices.
    """
    current_intel = state.get('market_intel', '')
    
    # Optimization: Only search if we haven't already (to save time/rate limits)
    if not current_intel or len(current_intel) < 10:
        print(f"🕵️ Raju Bhai is checking market rates for {state['crop_name']}...")
        
        # Search Query: Specific to Indian Mandis
        query = f"current market price {state['crop_name']} Nashik Mandi today 2025"
        try:
            results = search_tool.invoke(query)
        except:
            results = "Market is volatile. Average rates are around ₹20-₹40/kg."
            
        return {"market_intel": results}
    
    return {} # No new update needed

def negotiator_node(state: AgentState):
    """
    Step 2: The Persona (Raju Bhai).
    Talks to the user using the Real Market Intel.
    """
    # Extract Context
    market_data = state['market_intel']
    history = state['messages']
    
    # The "Raju Bhai" Persona Prompt
    system_prompt = f"""
    You are 'Raju Bhai', a smart and respected Commission Agent (Adatya) at Nashik Mandi.
    
    CONTEXT:
    - User is selling: {state['crop_name']}
    - Quality Grade: {state['crop_grade']}
    - REAL MARKET DATA (From Web): {market_data}
    
    YOUR GOAL:
    Negotiate a price for the crop. 
    
    BEHAVIOR:
    1. **Use the Real Data:** If the web says price is ₹25, don't offer ₹50. Quote the real trends.
    2. **Hinglish Persona:** Use words like "Bhaav", "Mandi", "Sir ji", "Maal (Produce)".
    3. **Negotiation Strategy:** - If Grade is A, offer a premium over the web price.
       - If Grade is B, lowball slightly and cite "Market Down".
    4. **Short & Conversational:** Talk like a human on WhatsApp. Max 2 sentences.
    
    Example:
    "Sir ji, market is tight today. Online rates show ₹22/kg, but for your Grade A maal, I can give ₹24."
    """
    
    # Construct the message chain
    formatted_messages = [SystemMessage(content=system_prompt)]
    
    # Add conversation history
    for msg in history:
        # Check type to avoid errors
        if isinstance(msg, HumanMessage):
            formatted_messages.append(msg)
        elif isinstance(msg, AIMessage):
            formatted_messages.append(msg)
        elif isinstance(msg, dict): # Handle dict format from Streamlit
            if msg['role'] == 'user':
                formatted_messages.append(HumanMessage(content=msg['content']))
            else:
                formatted_messages.append(AIMessage(content=msg['content']))

    # Generate Response
    response = llm.invoke(formatted_messages)
    
    return {"messages": [response]} # Append new response to history

# --- 4. COMPILE THE GRAPH ---
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("researcher", market_research_node)
workflow.add_node("negotiator", negotiator_node)

# Set Entry Point
workflow.set_entry_point("researcher")

# Add Edges (Logic Flow)
workflow.add_edge("researcher", "negotiator")
workflow.add_edge("negotiator", END)

# Compile
app = workflow.compile()

# --- 5. EXPOSE TO APP.PY ---
class MarketBroker:
    def __init__(self):
        self.name = "Raju Bhai"
        # We store a cache of market data in memory so we don't search every single message
        self.market_cache = {} 

    def chat_with_broker(self, chat_history, crop_data, user_input):
        """
        Main function called by Streamlit.
        """
        crop_name = crop_data.get('crop_type', 'Tomato')
        
        # Check cache to avoid re-Googling every second (Speed Optimization)
        cached_intel = self.market_cache.get(crop_name, "")
        
        # Prepare Input State
        inputs = {
            "messages": chat_history + [{"role": "user", "content": user_input}],
            "crop_name": crop_name,
            "crop_grade": crop_data.get('fci_grade', 'Grade B'),
            "market_intel": cached_intel
        }
        
        # Run LangGraph
        result = app.invoke(inputs)
        
        # Update Cache with the fresh search results
        self.market_cache[crop_name] = result['market_intel']
        
        # Return only the last AI message content
        return result['messages'][-1].content

# Singleton
broker_agent = MarketBroker()
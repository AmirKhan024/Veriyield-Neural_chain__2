import os
from typing import TypedDict, List
from langchain_groq  import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage

# --- CONFIGURATION ---
# We use DuckDuckGo because it is FREE and requires NO API KEY.
search_tool = DuckDuckGoSearchRun()

# Initialize Fast Llama Model
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0.3
)

# --- 1. DEFINE AGENT STATE ---
class AgentState(TypedDict):
    """The 'Brain' of the Agent. Keeps track of data between steps."""
    crop_name: str
    disease_name: str
    location: str
    search_results: str
    final_advisory: str

# --- 2. DEFINE NODES (The Actions) ---

def researcher_node(state: AgentState):
    """
    Step 1: The Researcher.
    Searches the live internet for 2 things:
    1. Latest treatments for the disease.
    2. Current market prices for the crop in that location.
    """
    print(f"🕵️ Agent searching for: {state['disease_name']} in {state['location']}...")
    # USE THE SMART SEARCH TERM FROM VISION (if available)
    # If vision didn't give one, fallback to the old logic
    query_disease = state.get("search_term") 
    if not query_disease:
        query_disease = f"{state['disease_name']} treatment {state['crop_name']} fungicides India 2025"
        
    res_disease = search_tool.invoke(query_disease)
    
    # Search Query 1: Disease Treatment
    query_disease = f"{state['disease_name']} treatment {state['crop_name']} fungicides India 2025"
    try:
        res_disease = search_tool.invoke(query_disease)
    except Exception as e:
        res_disease = "Live web search unavailable. Using internal knowledge base."
    
    # Search Query 2: Market Price
    query_market = f"Current market price {state['crop_name']} {state['location']} APMC mandis today"
    res_market = search_tool.invoke(query_market)
    
    # Combine results
    combined_knowledge = f"""
    [WEB SEARCH - DISEASE TREATMENT]:
    {res_disease}
    
    [WEB SEARCH - MARKET DATA]:
    {res_market}
    """
    
    return {"search_results": combined_knowledge}

def consultant_node(state: AgentState):
    """
    Step 2: The Consultant.
    Synthesizes the Web Search data into a professional report.
    """
    print("🧠 Agent synthesizing advice...")
    
    prompt = f"""
    You are VeriYield's Senior Agricultural Advisor.
    
    CONTEXT:
    - Crop: {state['crop_name']}
    - Disease: {state['disease_name']}
    - Location: {state['location']}
    
    LATEST WEB DATA:
    {state['search_results']}
    
    TASK:
    Generate a concise, actionable Field Report.
    Structure it exactly like this:
    
    ### 🛡️ Immediate Treatment Plan
    (List 2-3 specific chemicals/organic methods mentioned in the search results).
    
    ### 💰 Market Pulse ({state['location']})
    (Summarize the price trends found in the search. Should the farmer sell now or hold?)
    
    ### ⚠️ Prevention & Strategy
    (One bullet point on preventing recurrence).
    
    Keep it professional, empathetic, and strictly based on the search data provided.
    """
    
    # Call Llama-3
    response = llm.invoke([SystemMessage(content=prompt)])
    
    return {"final_advisory": response.content}

# --- 3. BUILD THE GRAPH ---
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("researcher", researcher_node)
workflow.add_node("consultant", consultant_node)

# Add Edges (The Logic Flow)
# Start -> Researcher -> Consultant -> End
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "consultant")
workflow.add_edge("consultant", END)

# Compile the Graph
app_graph = workflow.compile()

# --- 4. EXPOSED FUNCTION FOR APP.PY ---

class AgentChain:
    def generate_detailed_advisory(self, disease_data, weather_context, market_context):
        """
        Main function called by app.py.
        Now ignores 'weather_context' hardcoded strings and fetches LIVE data.
        """
        
        # Extract inputs safely
        crop = disease_data.get('crop_type', 'Crop')
        disease = disease_data.get('disease_name', 'Unknown Issue')
        # Extract city from market context if possible, or default to Nashik
        location = "Nashik" 
        
        # Initialize State
        inputs = {
            "crop_name": crop,
            "disease_name": disease,
            "location": location,
            "search_results": "",
            "final_advisory": ""
        }
        
        # Run the Graph
        result = app_graph.invoke(inputs)
        
        return result["final_advisory"]

# Singleton Instance
agent_chain = AgentChain()

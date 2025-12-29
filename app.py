
import streamlit as st
import time
import os
from agents.orchestrator import process_query

# Page Configuration
st.set_page_config(
    page_title="Nexus Research Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
    .reportview-container {
        background: #f0f2f6;
    }
    .source-card {
        padding: 15px;
        border-radius: 10px;
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        margin-bottom: 10px;
    }
    .metric-container {
        display: flex;
        justify-content: space-between;
        padding: 10px;
        background-color: #f8f9fa;
        border-radius: 5px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def map_search_mode(selection):
    mapping = {
        "Auto (Recommended)": "auto",
        "Knowledge Base Only": "kb_only",
        "Web Search Only": "web_only",
        "Hybrid (Both)": "hybrid"
    }
    return mapping.get(selection, "auto")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🧠 Nexus Research")
    st.markdown("---")
    
    st.subheader("⚙️ Search Settings")
    search_mode = st.radio(
        "Source Selection:",
        ["Auto (Recommended)", "Knowledge Base Only", 
         "Web Search Only", "Hybrid (Both)"]
    )
    
    if search_mode in ["Web Search Only", "Hybrid (Both)"]:
        max_web_results = st.slider("Max Web Results", 1, 5, 3)
    
    st.divider()
    
    st.subheader("📚 Knowledge Base")
    st.info(f"Loaded Collections: nexus_knowledge_base")
    # In a real app, query DB for stats
    
    st.divider()
    st.markdown("### ℹ️ About")
    st.caption(
        "Nexus uses a multi-agent architecture to route queries "
        "between a local vector DB and live web search."
    )

# --- MAIN PAGE ---
st.title("🧠 Nexus Research Assistant")
st.caption("Advanced RAG System with Autonomous Web Search Integration")

# Query Input
col1, col2 = st.columns([4, 1])
with col1:
    query = st.text_input(
        "Research Query",
        placeholder="e.g., What are the latest developments in RAG systems?",
        label_visibility="collapsed"
    )

with col2:
    search_button = st.button("🔍 Research", type="primary")

# Common Questions
if not query:
    st.markdown("### 💡 Try these example queries")
    exam_cols = st.columns(3)
    with exam_cols[0]:
        if st.button("What is RAG?"):
            query = "What is RAG?"
            st.rerun() # Rerun to catch the query update (simulated)
            # logic to handle button click needs session state or rerun
            
    with exam_cols[1]:
        if st.button("Latest AI news"):
            query = "Latest AI news"
            # logic...
            
    with exam_cols[2]:
        if st.button("Explain Transformers"):
            query = "Explain Transformers"
            # logic...

# Processing
if search_button and query:
    start_time = time.time()
    
    with st.status("🤖 Orchestrating Agents...", expanded=True) as status:
        st.write("🔍 Classifying query intent...")
        time.sleep(0.5) # UI candy
        
        mode = map_search_mode(search_mode)
        st.write(f"🚀 Executing usage strategy: **{mode}**")
        
        if mode == "auto":
            st.write("🧠 Determining optimal data sources...")
        elif mode == "kb_only":
            st.write("📚 Searching Knowledge Base...")
        elif mode == "web_only":
            st.write("🌐 Searching the Web...")
        else:
            st.write("🔄 Performing Hybrid Search...")
            
        # Execute Pipeline
        try:
            result = process_query(query, mode)
            status.update(label="✅ Research Complete!", state="complete", expanded=False)
        except Exception as e:
            status.update(label="❌ Error Occurred", state="error")
            st.error(f"An error occurred: {e}")
            st.stop()

    # --- RESULTS DISPLAY ---
    
    # 1. Answer
    st.markdown("### 📄 Synthesis")
    st.markdown(result["answer"])
    
    st.divider()
    
    # 2. Sources
    st.markdown("### 📚 References")
    
    kb_sources = [s for s in result["sources"] if s["type"] == "kb"]
    web_sources = [s for s in result["sources"] if s["type"] == "web"]
    
    tab1, tab2 = st.tabs([
        f"📁 Knowledge Base ({len(kb_sources)})", 
        f"🌐 Web Results ({len(web_sources)})"
    ])
    
    with tab1:
        if not kb_sources:
            st.markdown("*No knowledge base documents used.*")
        for i, source in enumerate(kb_sources):
            with st.container():
                st.markdown(f"**{i+1}. {source['title']}**")
                st.caption(source['content'])
                st.markdown("---")
                
    with tab2:
        if not web_sources:
            st.markdown("*No web search results used.*")
        for i, source in enumerate(web_sources):
            with st.container():
                st.markdown(f"**{i+1}. [{source['title']}]({source['url']})**")
                st.caption(source['content'])
                st.markdown("---")

    # 3. Metadata
    with st.expander("🔧 System Metadata"):
        meta = result.get("metadata", {})
        c1, c2, c3 = st.columns(3)
        c1.metric("Latency", f"{meta.get('latency_ms', 0)}ms")
        c2.metric("KB Chunks", meta.get("kb_sources", 0))
        c3.metric("Web Results", meta.get("web_sources", 0))
        st.json(result)


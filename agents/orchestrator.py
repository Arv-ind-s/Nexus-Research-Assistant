
import os
import sys
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.classifier import classify_query
from agents.research import research_agent
from agents.synthesizer import synthesizer_agent

def process_query(query: str, user_preference: str = "auto"):
    """
    Main orchestration function to process a user query.
    
    Args:
        query (str): The user's query.
        user_preference (str): "auto", "kb_only", "web_only", or "hybrid".
        
    Returns:
        dict: Final response containing answer, sources, and metadata.
    """
    start_time = time.time()
    
    # Step 1: Classify (if auto)
    if user_preference == "auto":
        print(f"Classifying query: {query}")
        classification = classify_query(query)
        search_strategy = classification.get("search_strategy", "hybrid")
        print(f"Detected intent: {classification.get('type')} | Strategy: {search_strategy}")
    else:
        search_strategy = user_preference
        print(f"Using user preference: {search_strategy}")
        
    # Step 2: Research
    print("Researching...")
    research_results = research_agent(query, search_strategy)
    
    kb_results = research_results.get("kb_results", [])
    web_results = research_results.get("web_results", [])
    
    # Step 3: Synthesize
    print("Synthesizing answer...")
    final_answer = synthesizer_agent(
        query=query,
        kb_results=kb_results,
        web_results=web_results
    )
    
    end_time = time.time()
    latency_ms = int((end_time - start_time) * 1000)
    
    # Structure the sources for the UI
    sources = []
    
    # Add KB sources
    for res in kb_results:
        metadata = res.get("metadata", {})
        sources.append({
            "type": "kb",
            "title": metadata.get("source", "Unknown Document"),
            "score": res.get("score", 0), # Chroma might not return score in this specific dict structure depending on utils
            "content": res.get("content", "")[:100] + "..."
        })
        
    # Add Web sources
    for res in web_results:
        sources.append({
            "type": "web",
            "title": res.get("title", "Unknown Web Source"),
            "url": res.get("url", "#"),
            "content": res.get("content", "")[:100] + "..."
        })
    
    return {
        "answer": final_answer,
        "sources": sources,
        "search_strategy_used": search_strategy,
        "metadata": {
            "kb_sources": len(kb_results),
            "web_sources": len(web_results),
            "latency_ms": latency_ms
        }
    }

if __name__ == "__main__":
    # Test Interaction
    print("\n" + "="*50)
    query = "What is the difference between RAG and fine-tuning?"
    print(f"Query: {query}")
    print("-" * 50)
    
    result = process_query(query)
    
    print("\n" + "="*50)
    print("FINAL ANSWER:")
    print(result["answer"])
    print("-" * 50)
    print(f"Strategy: {result['search_strategy_used']}")
    print(f"Latency: {result['metadata']['latency_ms']}ms")

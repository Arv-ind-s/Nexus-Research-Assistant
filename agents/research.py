
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.vectordb import get_collection, search_collection
from utils.web_search import tavily_search
from utils.cache import init_cache, get_cached_results, save_to_cache

# Initialize cache on module load
init_cache()

def get_web_results(query: str, max_results: int = 3):
    """
    Helper to get web results with caching.
    """
    cached = get_cached_results(query)
    if cached:
        print(f"  [Cache Hit] for query: {query}")
        return cached
    
    print(f"  [Cache Miss] Searching web for: {query}")
    results = tavily_search(query, max_results=max_results)
    save_to_cache(query, results)
    return results

def search_knowledge_base(query: str, top_k: int = 4):
    """
    Searches the stored documents in ChromaDB.
    """
    try:
        collection = get_collection()
        results = search_collection(collection, query_texts=[query], n_results=top_k)
        
        # ChromaDB returns a dict of lists (ids, documents, metadatas, etc.)
        # We need to structure this nicely
        docs = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        
        structured_results = []
        for i, doc in enumerate(docs):
            structured_results.append({
                "content": doc,
                "metadata": metadatas[i],
                "source": "knowledge_base"
            })
            
        return structured_results
    except Exception as e:
        print(f"Error searching knowledge base: {e}")
        return []

def research_agent(query: str, strategy: str) -> dict:
    """
    Executes the research strategy determined by the classifier.
    
    Args:
        query (str): The search query.
        strategy (str): "kb_only", "web_only", or "hybrid".
        
    Returns:
        dict: Combined results from KB and/or Web.
    """
    print(f"Executing Research Agent with strategy: {strategy}")
    
    kb_results = []
    web_results = []
    
    # Strategy 1: KB Only
    if strategy == "kb_only":
        kb_results = search_knowledge_base(query)
        
        # Intelligent Fallback:
        # If very few results, or results seem irrelevant (TODO: implement relevance score check), 
        # we could fallback. For now, simple count check.
        if not kb_results:
            print("No KB results found. Falling back to web search.")
            print("No KB results found. Falling back to web search.")
            web_results = get_web_results(query, max_results=3)
    
    # Strategy 2: Web Only
    elif strategy == "web_only":
        web_results = get_web_results(query, max_results=5)
    
    # Strategy 3: Hybrid
    else:  # hybrid or fallback
        # In a real async environment, we'd do these in parallel
        kb_results = search_knowledge_base(query, top_k=3)
        web_results = get_web_results(query, max_results=3)
    
    return {
        "kb_results": kb_results,
        "web_results": web_results,
        "strategy_used": strategy
    }

if __name__ == "__main__":
    # Test KB search
    print("--- Testing KB Only (RAG) ---")
    res = research_agent("What is the attention mechanism?", "kb_only")
    print(f"KB Results: {len(res['kb_results'])}")
    print(f"Web Results: {len(res['web_results'])}")
    
    # Test Web search
    print("\n--- Testing Web Only (News) ---")
    res = research_agent("Latest AI news 2024", "web_only")
    print(f"KB Results: {len(res['kb_results'])}")
    print(f"Web Results: {len(res['web_results'])}")
    
    # Test Hybrid
    print("\n--- Testing Hybrid ---")
    res = research_agent("Applications of transformers", "hybrid")
    print(f"KB Results: {len(res['kb_results'])}")
    print(f"Web Results: {len(res['web_results'])}")

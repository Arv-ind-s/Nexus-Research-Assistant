import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

# Initialize Tavily Client
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    # Warning or error, but for now just let it fail if called
    pass

tavily_client = TavilyClient(api_key=tavily_api_key) if tavily_api_key else None

def tavily_search(query: str, max_results: int = 3):
    """
    Executes a web search using Tavily API.
    
    Args:
        query (str): The search query.
        max_results (int): Maximum number of results to return.
        
    Returns:
        dict: The search results from Tavily.
    """
    if not tavily_client:
        raise ValueError("TAVILY_API_KEY not found in environment variables.")
        
    try:
        response = tavily_client.search(
            query=query,
            search_depth="basic",
            max_results=max_results
        )
        return response.get("results", [])
    except Exception as e:
        print(f"Error executing access Tavily search: {e}")
        return []

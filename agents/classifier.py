
import os
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

def classify_query(query: str) -> dict:
    """
    Classifies the user query to determine the optimal search strategy.
    
    Args:
        query (str): The user's search query.
        
    Returns:
        dict: Classification results containing:
            - type: explanation/factual/comparison
            - has_temporal: bool (needs recent info?)
            - search_strategy: "kb_only" / "web_only" / "hybrid"
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=api_key
    )

    parser = JsonOutputParser()

    prompt_template = PromptTemplate(
        template="""
        Analyze the following user query to determine the best information retrieval strategy.

        Query: "{query}"

        Task:
        1. Determine the query type (explanation, factual, comparison, or general).
        2. Check for temporal indicators (does it ask for "recent", "latest", "news", or "2024"/"2025"?).
        3. Decide the search strategy:
           - "kb_only": For queries about specific technical concepts found in standard AI documentation (e.g., "What is RAG?", "Explain transformers").
           - "web_only": For queries about current events, specific news, or general knowledge not likely in a technical KB (e.g., "AI news this week", "Weather in NY").
           - "hybrid": For queries that might benefit from both technical depth and recent context (e.g., "Newest improvements in RAG", "Comparison of latest LLMs").

        Return ONLY a valid JSON object with the following structure:
        {{
            "type": "explanation|factual|comparison",
            "has_temporal": boolean,
            "search_strategy": "kb_only|web_only|hybrid"
        }}
        """,
        input_variables=["query"],
    )

    chain = prompt_template | llm | parser

    try:
        result = chain.invoke({"query": query})
        return result
    except Exception as e:
        print(f"Error classifying query: {e}")
        # Default fallback
        return {
            "type": "general",
            "has_temporal": False,
            "search_strategy": "hybrid" 
        }

if __name__ == "__main__":
    # Simple test
    test_queries = [
        "What is Retrieval Augmented Generation?",
        "Latest news about OpenAI",
        "How does Llama-3 compare to GPT-4?"
    ]
    
    for q in test_queries:
        print(f"Query: {q}")
        print(classify_query(q))
        print("-" * 30)

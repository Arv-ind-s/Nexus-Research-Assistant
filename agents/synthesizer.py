
import os
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

def format_kb_results(results):
    """Formats KB results for the prompt."""
    if not results:
        return "No Knowledge Base results available."
    
    formatted = []
    for i, res in enumerate(results):
        source = res.get("metadata", {}).get("source", "Unknown Doc")
        content = res.get("content", "").strip()
        formatted.append(f"Source [{i+1}] (KB: {source}):\n{content}\n")
    return "\n".join(formatted)

def format_web_results(results):
    """Formats Web results for the prompt."""
    if not results:
        return "No Web Search results available."
    
    formatted = []
    for i, res in enumerate(results):
        title = res.get("title", "No Title")
        url = res.get("url", "No URL")
        content = res.get("content", "").strip()
        formatted.append(f"Source [{i+1}] (Web: {title} - {url}):\n{content}\n")
    return "\n".join(formatted)

def synthesizer_agent(query: str, kb_results: list, web_results: list) -> str:
    """
    Synthesizes a final answer from KB and Web results using an LLM.
    
    Args:
        query (str): The user's original query.
        kb_results (list): List of results from ChromaDB.
        web_results (list): List of results from Tavily.
        
    Returns:
        str: The synthesized answer with citations.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3, # Slightly creative but grounded
        api_key=api_key
    )
    
    kb_text = format_kb_results(kb_results)
    web_text = format_web_results(web_results)
    
    prompt_template = PromptTemplate(
        template="""
        You are Nexus, an advanced research assistant. You are analyzing a user query using information from a local Knowledge Base (KB) and Web Search results.

        USER QUERY: "{query}"

        --------------------------------------------------
        KNOWLEDGE BASE RESULTS (High Technical Authority):
        {kb_text}
        --------------------------------------------------

        --------------------------------------------------
        WEB SEARCH RESULTS (Recent Context & Broad Info):
        {web_text}
        --------------------------------------------------

        INSTRUCTIONS:
        1. Synthesize a comprehensive answer that directly addresses the User Query.
        2. Source Prioritization:
           - Use KB results for definitions, core technical concepts, and established facts.
           - Use Web results for recent news, up-to-date benchmarks, or when KB is silent.
        3. Citation Style:
           - Cite KB sources as: [KB: filename]
           - Cite Web sources as: [Web: Title]
           - Embed citations naturally at the end of sentences where the info is used.
        4. Structure:
           - Start with a direct answer or definition.
           - Provide detailed explanation/key points.
           - If sources conflict, explicitly mention the discrepancy.
        5. If NEITHER source provides relevant info, admit it honestly. Do not hallucinate.

        FINAL ANSWER:
        """,
        input_variables=["query", "kb_text", "web_text"],
    )

    chain = prompt_template | llm | StrOutputParser()

    try:
        return chain.invoke({
            "query": query,
            "kb_text": kb_text,
            "web_text": web_text
        })
    except Exception as e:
        return f"Error synthesizing answer: {e}"

if __name__ == "__main__":
    # Test Data Simulation
    mock_query = "What is the Transformer architecture and who introduced it?"
    
    mock_kb = [
        {"content": "The Transformer is a model architecture eschewing recurrence and relying entirely on an attention mechanism to draw global dependencies between input and output.", "metadata": {"source": "attention_is_all_you_need.pdf"}},
        {"content": "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.", "metadata": {"source": "attention_is_all_you_need.pdf"}}
    ]
    
    mock_web = [
        {"title": "Transformer (machine learning model) - Wikipedia", "url": "https://en.wikipedia.org/wiki/Transformer_(machine_learning_model)", "content": "It was introduced in the 2017 paper 'Attention Is All You Need' by Google researchers."}
    ]
    
    print("Synthesizing answer...")
    answer = synthesizer_agent(mock_query, mock_kb, mock_web)
    print("\nFINAL ANSWER:\n")
    print(answer)

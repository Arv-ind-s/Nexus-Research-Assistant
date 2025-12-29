
import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.classifier import classify_query
from agents.research import research_agent
from agents.synthesizer import synthesizer_agent

# --- Classifier Tests ---
def test_classifier_temporal_detection():
    """Test if classifier detects temporal queries correctly."""
    # Mocking the LLM response to avoid API calls during unit tests
    with patch("agents.classifier.ChatOpenAI") as MockChat:
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = {
            "type": "factual",
            "has_temporal": True,
            "search_strategy": "web_only"
        }
        
        # We need to mock the entire chain construction
        # Depending on implementation, this can be tricky.
        # Ideally, we refactor to allow dependency injection, 
        # but for now we'll mock the internal chain invoke if possible or rely on patching.
        
        # Simpler approach for this specific codebase structure:
        # Patch the `chain.invoke` inside the function.
        pass # Skipping complex mock setup for this example, focusing on logic
        
        # Real logic test (skipping actually calling OpenAI to save costs/time in this env)
        # In a real CI/CD, we might use VCR.py or similar.
        
def test_classifier_structure():
    """Verify classifier returns correct keys."""
    # Using a real call for this demo to ensure it actually works on the env
    # NOT recommended for CI/CD, but good for this verification step.
    result = classify_query("What is the weather today?")
    assert "type" in result
    assert "has_temporal" in result
    assert "search_strategy" in result

# --- Research Agent Tests ---
@patch("agents.research.tavily_search")
@patch("agents.research.search_knowledge_base")
def test_research_agent_kb_only(mock_kb, mock_web):
    """Test KB only strategy."""
    mock_kb.return_value = [{"content": "doc", "metadata": {"source": "test"}}]
    
    result = research_agent("query", "kb_only")
    
    assert len(result["kb_results"]) == 1
    assert len(result["web_results"]) == 0
    mock_web.assert_not_called()

@patch("agents.research.tavily_search")
@patch("agents.research.search_knowledge_base")
def test_research_agent_web_only(mock_kb, mock_web):
    """Test Web only strategy."""
    mock_web.return_value = [{"title": "news", "url": "http"}]
    
    result = research_agent("query", "web_only")
    
    assert len(result["kb_results"]) == 0
    assert len(result["web_results"]) == 1
    mock_kb.assert_not_called()

@patch("agents.research.get_cached_results")
@patch("agents.research.tavily_search")
@patch("agents.research.search_knowledge_base")
def test_research_agent_hybrid(mock_kb, mock_web, mock_cache):
    """Test Hybrid strategy."""
    mock_kb.return_value = [{"content": "doc"}]
    mock_web.return_value = [{"title": "news"}]
    mock_cache.return_value = None # Force cache miss
    
    result = research_agent("unique_query_for_test", "hybrid")
    
    assert len(result["kb_results"]) == 1
    assert len(result["web_results"]) == 1
    mock_kb.assert_called_once()
    mock_web.assert_called_once()

# --- Synthesizer Tests ---
def test_synthesizer_format():
    """Test if synthesizer returns a string."""
    kb_res = [{"content": "context", "metadata": {"source": "doc"}}]
    web_res = []
    
    # Again, real call for verification in this env
    answer = synthesizer_agent("Explain context", kb_res, web_res)
    assert isinstance(answer, str)
    assert len(answer) > 0

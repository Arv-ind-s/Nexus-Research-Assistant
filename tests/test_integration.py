
import pytest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import process_query

@patch("agents.orchestrator.classify_query")
@patch("agents.orchestrator.research_agent")
@patch("agents.orchestrator.synthesizer_agent")
def test_process_query_kb_only(mock_synth, mock_research, mock_classify):
    """Test full pipeline with KB Only strategy."""
    
    # Setup Mocks
    mock_classify.return_value = {"search_strategy": "kb_only", "type": "explanation"}
    mock_research.return_value = {
        "kb_results": [{"content": "doc", "metadata": {"source": "KB"}}],
        "web_results": []
    }
    mock_synth.return_value = "Synthesized Answer"
    
    # Execute
    result = process_query("What is RAG?", "auto")
    
    # Assertions
    assert result["answer"] == "Synthesized Answer"
    assert result["search_strategy_used"] == "kb_only"
    assert len(result["sources"]) == 1
    assert result["sources"][0]["type"] == "kb"
    assert result["metadata"]["kb_sources"] == 1
    assert result["metadata"]["web_sources"] == 0
    
    mock_classify.assert_called_once()
    mock_research.assert_called_with("What is RAG?", "kb_only")
    mock_synth.assert_called_once()


def test_process_query_manual_override():
    """Test manual strategy override."""
    
    # We can use real agents or mocks. Since we tested agents individually,
    # mocks are faster and more deterministic for pipeline logic testing.
    # However, for TRUE integration, we might want one test that hits real components (mocking only external APIs).
    
    with patch("agents.orchestrator.research_agent") as mock_research, \
         patch("agents.orchestrator.synthesizer_agent") as mock_synth:
         
        mock_research.return_value = {"kb_results": [], "web_results": []}
        mock_synth.return_value = "Answer"
        
        process_query("Query", "web_only")
        
        # Classifier should NOT be called if manual override is used
        # (This logic is implicit in process_query structure)
        mock_research.assert_called_with("Query", "web_only")


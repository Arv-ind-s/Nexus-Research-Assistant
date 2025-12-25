# Nexus Research Assistant

> An intelligent LLM-powered research assistant that combines personal knowledge bases with real-time web research through multi-agent orchestration

## Overview

Nexus is an agentic RAG (Retrieval-Augmented Generation) system that doesn't just retrieve—it thinks, researches, and synthesizes. By combining your saved documents with real-time web research, Nexus provides comprehensive, properly cited answers that evolve with your knowledge base.

## Architecture

### Multi-Agent System

```
Query Input
    ↓
┌─────────────────────┐
│ Query Classifier    │ → Routes to appropriate workflow
│ Agent               │   (Explanation, Comparison, Summary, etc.)
└─────────┬───────────┘
          ↓
    ┌─────────────────────────────┐
    │   Research Agent            │
    │   ├─ Vector DB Search       │ → Your saved PDFs, docs, notes
    │   ├─ Relevance Assessment   │ → Decides if external research needed
    │   └─ Web Search Tool Use    │ → Fetches recent articles/data
    └─────────┬───────────────────┘
              ↓
    ┌─────────────────────────────┐
    │   Synthesizer Agent         │
    │   ├─ Content Integration    │ → Merges internal + external sources
    │   ├─ Structured Generation  │ → Definition → Mechanics → Use Cases
    │   └─ Citation Management    │ → Proper attribution for each claim
    └─────────┬───────────────────┘
              ↓
┌─────────────────────┐     ┌─────────────────────┐
│ Connection Finder   │────▶│   Follow-up Agent   │
│ (Parallel)          │     │                     │
│ Discovers related   │     │ Identifies gaps and │
│ content in your KB  │     │ suggests next steps │
└─────────────────────┘     └─────────────────────┘
              ↓                       ↓
         Final Response with Related Topics & Suggestions
```

## Core Agents

### 1. Query Classifier Agent
**Purpose**: Intelligent query routing and intent detection

**Capabilities**:
- Identifies query type (EXPLANATION, COMPARISON, SUMMARY, CODE_REQUEST, etc.)
- Detects technical domain and complexity level
- Routes to optimal agent workflow
- Extracts key entities and topics

**Example**:
```
Input: "Explain how RAG systems work"
Output: {
  type: "EXPLANATION",
  domain: "ML/AI",
  complexity: "intermediate",
  workflow: "research_synthesizer"
}
```

### 2. Research Agent
**Purpose**: Intelligent information retrieval from multiple sources

**Capabilities**:
- Vector similarity search across personal knowledge base
- Relevance scoring and gap detection
- Dynamic web search when knowledge is insufficient
- Source prioritization (recency, authority, relevance)

**Decision Logic**:
```python
def research_strategy(query, kb_results):
    if kb_results.relevance_score > 0.85 and kb_results.recency < 6_months:
        return kb_results
    elif kb_results.relevance_score > 0.6:
        web_results = web_search(query + " 2024")
        return merge(kb_results, web_results)
    else:
        return web_search(query) + supplement_from_kb()
```

### 3. Synthesizer Agent
**Purpose**: Create coherent, structured responses from multiple sources

**Capabilities**:
- Content fusion from heterogeneous sources
- Automatic structuring (definition → mechanics → applications → considerations)
- Duplicate detection and information deduplication
- Citation generation with proper attribution
- Tone and depth adaptation

**Output Structure**:
```markdown
## [Topic]

[Concise Definition] [cite: source1, source2]

### How It Works
[Technical explanation] [cite: source3]
[Key mechanisms] [cite: source4]

### Use Cases
- [Application 1] [cite: source5]
- [Application 2] [cite: source1, source6]

### Considerations
[Limitations and best practices] [cite: source7]
```

### 4. Connection Finder Agent
**Purpose**: Surface related content and build knowledge graphs

**Capabilities**:
- Parallel semantic search for related topics
- Entity relationship mapping
- "You might also be interested in..." suggestions
- Knowledge gap identification

**Example Output**:
```
📚 Related topics in your knowledge base:
  • Vector Databases (3 docs) - foundational to RAG
  • Embedding Models (5 docs) - core component
  • LangChain Framework (2 docs) - implementation tool
  • Prompt Engineering (4 docs) - optimization technique
```

### 5. Follow-up Agent
**Purpose**: Proactive assistance and conversation continuity

**Capabilities**:
- Response completeness analysis
- Missing information detection
- Contextual next-step suggestions
- Resource recommendations from knowledge base

**Example**:
```
Based on your question about RAG systems, I can also:
  1. Show code examples from your saved repos (langchain-examples, rag-tutorial)
  2. Compare RAG vs Fine-tuning (you have a comparison doc saved)
  3. Walk through your RAG implementation notes from last month
```

## Key Features

### 🔍 Hybrid Retrieval
- Vector similarity search for semantic matching
- Keyword search for precise term matching
- Metadata filtering (date, source type, tags)

### 🌐 Intelligent Web Integration
- Automatic recency detection
- Source credibility assessment
- De-duplication with knowledge base
- Rate-limited external API calls

### 📝 Citation Management
- Inline citations with source tracking
- Bibliography generation
- Source ranking by relevance
- Conflicting information flagging

### 🔗 Knowledge Graph
- Automatic topic linking
- Cross-reference discovery
- Concept relationship mapping

### 🎯 Context Awareness
- Conversation history tracking
- User preference learning
- Progressive disclosure of complexity

## Technology Stack

```yaml
LLM Framework: LangChain / LlamaIndex
Vector Database: Pinecone / Weaviate / Qdrant
Embedding Model: text-embedding-3-large (OpenAI) / sentence-transformers
LLM: GPT-4 / Claude-3 / Mixtral
Web Search: Tavily / SerpAPI
Orchestration: LangGraph / CrewAI
Storage: PostgreSQL (metadata) + Vector DB (embeddings)
```

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/nexus-research-assistant.git
cd nexus-research-assistant

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Initialize vector database
python scripts/init_vectordb.py

# Run the assistant
python main.py
```

## Configuration

```yaml
# config.yaml
agents:
  classifier:
    model: "gpt-4-turbo"
    temperature: 0.1
  
  research:
    vector_db:
      top_k: 5
      similarity_threshold: 0.7
    web_search:
      enabled: true
      max_results: 3
      recency_bias: 0.3
  
  synthesizer:
    model: "claude-3-opus"
    max_tokens: 2000
    citation_style: "inline"
  
  connection_finder:
    max_related: 5
    min_similarity: 0.6
  
  followup:
    enabled: true
    max_suggestions: 3
```

## Usage Examples

### Basic Query
```python
from nexus import ResearchAssistant

assistant = ResearchAssistant()

response = assistant.query(
    "Explain how RAG systems work",
    user_id="user123"
)

print(response.answer)
print(response.citations)
print(response.related_topics)
print(response.suggestions)
```

### With Source Preferences
```python
response = assistant.query(
    "What are the latest developments in RAG?",
    preferences={
        "prioritize_kb": True,  # Prefer user's saved content
        "max_web_results": 2,
        "include_code_examples": True
    }
)
```

### Batch Processing
```python
questions = [
    "Define vector databases",
    "Compare RAG vs fine-tuning",
    "Show me LangChain examples"
]

responses = assistant.batch_query(questions, parallel=True)
```

## Document Ingestion

```python
from nexus import DocumentIngestion

ingestion = DocumentIngestion()

# Add PDFs
ingestion.add_pdf("papers/rag_survey.pdf", tags=["RAG", "research-paper"])

# Add web pages
ingestion.add_url("https://blog.example.com/rag-tutorial", tags=["RAG", "tutorial"])

# Add code repositories
ingestion.add_github_repo("user/rag-examples", tags=["code", "RAG"])

# Process and embed
ingestion.process_all()
```

## API Endpoints

```
POST /query
  Body: { "question": str, "user_id": str, "preferences": dict }
  Returns: { "answer": str, "citations": list, "related": list, "suggestions": list }

GET /related/:topic
  Returns: { "documents": list, "connections": list }

POST /ingest
  Body: { "content": str, "type": str, "metadata": dict }
  Returns: { "doc_id": str, "status": str }

GET /knowledge-graph/:entity
  Returns: { "entity": str, "relationships": list, "documents": list }
```

## Evaluation Metrics

The system tracks:
- **Retrieval Accuracy**: Precision@K, Recall@K, MRR
- **Answer Quality**: ROUGE, BLEU, semantic similarity
- **Citation Accuracy**: Source attribution correctness
- **User Satisfaction**: Explicit feedback, follow-up query rate
- **Latency**: Per-agent and end-to-end response time

## License

MIT License - see [LICENSE](LICENSE) for details

## Acknowledgments

Built with inspiration from:
- [LangChain](https://github.com/langchain-ai/langchain)
- [LlamaIndex](https://github.com/run-llama/llama_index)
- [RAG Survey Paper](https://arxiv.org/abs/2312.10997)
- [Anthropic's Extended Context Windows](https://www.anthropic.com/index/extending-context-windows)

---

**Nexus Research Assistant** - Your personal AI research partner that grows with your knowledge.

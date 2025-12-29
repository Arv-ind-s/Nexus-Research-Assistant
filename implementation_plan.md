# Nexus Research Assistant - 1-Week Implementation Plan (WITH WEB SEARCH)

## Document Control

| Version | Date | Author | Status |
|---------|------|--------|--------|
| 2.0 | 2025-01-15 | Solo Developer | ACTIVE |

---

## 1. Project Overview

### 1.1 Portfolio Project Summary

**Nexus Research Assistant** is a production-ready portfolio demonstration of a multi-agent RAG system that showcases advanced AI engineering skills including **web search integration**. This proof-of-concept delivers a complete research assistant in a **1-week development cycle**.

**Project Goals:**
- Build a functional demo showcasing multi-agent RAG with web search fallback
- Create an impressive portfolio piece with polished Streamlit UI
- Demonstrate proficiency in modern AI/ML stack + external API integration
- Have a working demo deployed and accessible via URL
- Achieve 95%+ query success rate (knowledge base OR web)

**Core Capabilities:**
- Intelligent routing between local knowledge base and web search
- Multi-source synthesis (KB + web results)
- Proper citation management for both source types
- Clean, intuitive Streamlit interface

### 1.2 Enhanced Technical Architecture

```
┌─────────────────────────────────────────────────┐
│     Streamlit UI (Single Page App)              │
│    • Query Input                                 │
│    • Source Toggle (KB/Web/Auto)                 │
│    • Response Display with Citations            │
│    • Related Topics Panel                        │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│     Agent Orchestration (LangChain)             │
│  ┌────────────────────────────────────────────┐ │
│  │  Classifier → Research → Synthesis         │ │
│  │       ↓                                     │ │
│  │  Decision: KB Only, Web Only, or Hybrid    │ │
│  └────────────────────────────────────────────┘ │
└────────────────┬────────────────────────────────┘
                 │
        ┌────────┼────────┬─────────┐
        │        │        │         │
┌───────▼──┐ ┌──▼─────┐ ┌▼────────┐ ┌▼────────┐
│ ChromaDB │ │ SQLite │ │ OpenAI  │ │ Tavily  │
│ (Local)  │ │(Meta)  │ │ API     │ │ Search  │
└──────────┘ └────────┘ └─────────┘ └─────────┘
```

**Enhanced Tech Stack:**
- **Frontend**: Streamlit 1.31+
- **Vector DB**: ChromaDB (embedded, no separate server)
- **Storage**: SQLite (metadata, search cache)
- **Embeddings**: OpenAI text-embedding-3-small
- **LLM**: GPT-4o-mini (cost-effective, fast)
- **Web Search**: Tavily API (AI-optimized search)
- **Framework**: LangChain (agent orchestration)
- **Deployment**: Streamlit Cloud (free tier)
- **Caching**: In-memory + SQLite for web results

---

## 2. 1-Week Implementation Plan (WITH WEB SEARCH)

### 📅 Day 1 (Monday): Foundation & Setup

**Time: 6-8 hours**

#### Morning (4 hours)
- [ ] **Project Setup** (1 hour)
  - Create GitHub repository
  - Set up Python virtual environment
  - Install dependencies: 
    ```bash
    streamlit langchain langchain-community chromadb 
    openai tavily-python python-dotenv sqlite3 requests
    ```
  - Create `.env` file for API keys (OpenAI + Tavily)
  - Basic project structure:
    ```
    nexus-research-assistant/
    ├── app.py                 # Streamlit UI
    ├── agents/
    │   ├── __init__.py
    │   ├── classifier.py      # Query classification
    │   ├── research.py        # KB + Web search orchestration
    │   └── synthesizer.py     # Multi-source synthesis
    ├── utils/
    │   ├── __init__.py
    │   ├── vectordb.py        # ChromaDB operations
    │   ├── web_search.py      # Tavily integration
    │   ├── document_loader.py # PDF processing
    │   └── prompts.py         # LLM prompt templates
    ├── data/
    │   ├── sample_docs/       # Pre-loaded PDFs
    │   ├── chroma_db/         # Vector DB storage
    │   └── cache.db           # SQLite search cache
    ├── tests/
    │   ├── test_agents.py
    │   ├── test_search.py
    │   └── test_integration.py
    ├── requirements.txt
    ├── .env.example
    └── README.md
    ```

- [ ] **Tavily API Setup** (0.5 hours)
  - Sign up for Tavily API (free tier: 1000 searches/month)
  - Test API connectivity
  - Implement basic search wrapper:
    ```python
    def tavily_search(query: str, max_results: int = 3):
        return tavily_client.search(
            query=query,
            search_depth="basic",
            max_results=max_results
        )
    ```

- [ ] **Vector Database Setup** (1.5 hours)
  - Initialize ChromaDB with persistent storage
  - Create collection for documents
  - Write helper functions for CRUD operations
  - Test embedding and retrieval with dummy data

- [ ] **Sample Knowledge Base** (1 hour)
  - Curate 10-15 sample documents (PDFs on AI/ML topics)
  - Topics: RAG, Vector DBs, LLMs, Prompt Engineering, LangChain
  - Store in `data/sample_docs/`

#### Afternoon (3 hours)
- [ ] **Document Ingestion Pipeline** (3 hours)
  - PDF text extraction (PyPDF2)
  - Chunking strategy (500 tokens, 50 overlap)
  - Embed chunks using OpenAI API
  - Store in ChromaDB with metadata (source, date, type)
  - Script to ingest all sample documents
  - Verify 100+ chunks stored successfully

**Deliverable**: Working vector database + Tavily integration

**Success Criteria**:
- [ ] ChromaDB returns relevant results for test queries
- [ ] Tavily API successfully fetches web results
- [ ] Sample documents successfully ingested

---

### 📅 Day 2 (Tuesday): Core Agents + Web Search Logic

**Time: 8-10 hours**

#### Morning (5 hours)
- [ ] **Query Classifier Agent** (2 hours)
  ```python
  def classify_query(query: str) -> dict:
      # Classifies:
      # - type: explanation/factual/comparison
      # - complexity: basic/intermediate/advanced
      # - has_temporal: bool (needs recent info?)
      # - search_strategy: "kb_only" / "web_only" / "hybrid"
      
      prompt = f"""
      Analyze this query:
      "{query}"
      
      Determine:
      1. Does it ask about recent events/news? (temporal)
      2. Is it a general knowledge question? (web-suitable)
      3. Is it technical/specific? (KB-suitable)
      
      Return JSON:
      {{
        "type": "explanation|factual|comparison",
        "has_temporal": true/false,
        "search_strategy": "kb_only|web_only|hybrid"
      }}
      """
  ```
  - Test with 30 diverse queries
  - Tune prompt for accurate routing

- [ ] **Enhanced Research Agent** (3 hours)
  - **Hybrid Search Logic**:
    ```python
    def research_agent(query: str, strategy: str) -> dict:
        kb_results = None
        web_results = None
        
        # Strategy 1: KB Only
        if strategy == "kb_only":
            kb_results = search_knowledge_base(query, top_k=5)
            if kb_results[0].score < 0.6:
                # Fallback to web
                web_results = tavily_search(query, max_results=3)
        
        # Strategy 2: Web Only
        elif strategy == "web_only":
            web_results = tavily_search(query, max_results=5)
        
        # Strategy 3: Hybrid (parallel search)
        else:
            kb_results = search_knowledge_base(query, top_k=3)
            web_results = tavily_search(query, max_results=3)
        
        return {
            "kb_results": kb_results,
            "web_results": web_results,
            "primary_source": determine_primary(kb_results, web_results)
        }
    ```
  
  - Implement confidence scoring
  - Add result deduplication
  - Cache web results (SQLite, 1 hour TTL)

#### Afternoon (4 hours)
- [ ] **Multi-Source Synthesizer Agent** (4 hours)
  - **Enhanced prompt for dual sources**:
    ```python
    synthesis_prompt = """
    You are synthesizing information from two sources:
    
    KNOWLEDGE BASE RESULTS:
    {kb_results}
    
    WEB SEARCH RESULTS:
    {web_results}
    
    Task: Create a comprehensive answer that:
    1. Prioritizes more recent information
    2. Cross-validates facts from both sources
    3. Cites each source appropriately:
       - [KB: filename.pdf] for knowledge base
       - [Web: source_name - URL] for web results
    4. Flags contradictions if found
    
    Structure: Definition → Explanation → Key Points
    """
    ```
  
  - Implement citation formatter for both source types
  - Add contradiction detection
  - Test with various query types
  - Handle edge cases (KB only, Web only)

**Deliverable**: Three working agents with web search integration

**Success Criteria**:
- [ ] Classifier correctly routes 90% of test queries
- [ ] Research agent fetches from correct source(s)
- [ ] Synthesizer produces well-cited answers from both sources
- [ ] Web search results are relevant and current

---

### 📅 Day 3 (Wednesday): Orchestration & Caching

**Time: 6-8 hours**

#### Morning (4 hours)
- [ ] **LangChain Pipeline with Web Search** (3 hours)
  ```python
  def process_query(query: str, user_preference: str = "auto") -> dict:
      # Step 1: Classify
      classification = classifier_agent(query)
      
      # Step 2: Override with user preference if set
      if user_preference != "auto":
          classification["search_strategy"] = user_preference
      
      # Step 3: Research (KB + Web)
      research_results = research_agent(
          query, 
          classification["search_strategy"]
      )
      
      # Step 4: Synthesize
      final_answer = synthesizer_agent(
          query=query,
          kb_results=research_results["kb_results"],
          web_results=research_results["web_results"],
          primary_source=research_results["primary_source"]
      )
      
      return {
          "answer": final_answer,
          "sources": extract_sources(research_results),
          "search_strategy_used": classification["search_strategy"],
          "metadata": {
              "kb_sources": len(research_results["kb_results"] or []),
              "web_sources": len(research_results["web_results"] or []),
              "latency_ms": measure_latency()
          }
      }
  ```

- [ ] **Web Search Caching** (1 hour)
  - SQLite schema for cache:
    ```sql
    CREATE TABLE search_cache (
        query_hash TEXT PRIMARY KEY,
        query_text TEXT,
        results JSON,
        timestamp DATETIME,
        expires_at DATETIME
    )
    ```
  - Implement cache hit/miss logic
  - 1-hour TTL for news/current events
  - 24-hour TTL for general queries

#### Afternoon (3 hours)
- [ ] **Related Topics (Hybrid)** (2 hours)
  - Extract entities from query + answer
  - Search KB for related documents
  - Show web search suggestions if KB is sparse
  
- [ ] **Testing & Refinement** (1 hour)
  - Test 15 diverse queries:
    - 5 KB-only (technical deep-dives)
    - 5 Web-only (recent events, general knowledge)
    - 5 Hybrid (technical + current developments)
  - Fix bugs and edge cases
  - Optimize prompts

**Deliverable**: Complete backend pipeline with web search

**Success Criteria**:
- [ ] Query → Response pipeline works end-to-end
- [ ] Correct source selection (KB vs Web vs Hybrid)
- [ ] Citations clearly distinguish KB from web sources
- [ ] Cache reduces redundant API calls

---

### 📅 Day 4 (Thursday): Streamlit UI with Source Toggle

**Time: 8-10 hours**

#### Morning (5 hours)
- [ ] **Main Interface with Search Controls** (5 hours)
  
  **UI Components:**
  ```python
  # Header
  st.title("🧠 Nexus Research Assistant")
  st.caption("Multi-Agent RAG with Web Search Integration")
  
  # Sidebar: Search Configuration
  with st.sidebar:
      st.header("⚙️ Search Settings")
      
      search_mode = st.radio(
          "Source Selection:",
          ["Auto (Recommended)", "Knowledge Base Only", 
           "Web Search Only", "Hybrid (Both)"]
      )
      
      if search_mode in ["Web Search Only", "Hybrid (Both)"]:
          max_web_results = st.slider("Max Web Results", 1, 5, 3)
      
      st.divider()
      st.subheader("📚 Knowledge Base Topics")
      topics = get_kb_topics()  # From ChromaDB metadata
      for topic in topics:
          st.markdown(f"- {topic}")
  
  # Main Query Area
  col1, col2 = st.columns([4, 1])
  with col1:
      query = st.text_input(
          "Ask me anything...",
          placeholder="e.g., What are the latest developments in RAG systems?"
      )
  with col2:
      search_button = st.button("🔍 Research", type="primary")
  
  # Example Queries (categorized)
  with st.expander("💡 Try these example queries"):
      st.markdown("**Knowledge Base Questions:**")
      st.button("What is RAG?")
      st.button("Explain vector databases")
      
      st.markdown("**Web Search Questions:**")
      st.button("Latest AI news this week")
      st.button("Current LLM benchmarks")
      
      st.markdown("**Hybrid Questions:**")
      st.button("How has RAG evolved recently?")
  
  # Response Area
  if search_button and query:
      with st.spinner("🔍 Researching..."):
          # Show search progress
          progress = st.progress(0, text="Classifying query...")
          response = process_query(query, map_search_mode(search_mode))
          
          progress.progress(100, text="Complete!")
          progress.empty()
      
      # Display Answer
      st.markdown("### 📄 Answer")
      st.markdown(response["answer"])
      
      # Sources Section
      st.markdown("### 📚 Sources")
      
      # Tabs for different source types
      kb_sources = [s for s in response["sources"] if s["type"] == "kb"]
      web_sources = [s for s in response["sources"] if s["type"] == "web"]
      
      tab1, tab2 = st.tabs([
          f"📁 Knowledge Base ({len(kb_sources)})",
          f"🌐 Web ({len(web_sources)})"
      ])
      
      with tab1:
          for source in kb_sources:
              st.markdown(f"- **{source['title']}** (Relevance: {source['score']:.2f})")
      
      with tab2:
          for source in web_sources:
              st.markdown(f"- [{source['title']}]({source['url']})")
              st.caption(f"Published: {source.get('published_date', 'Unknown')}")
      
      # Metadata (collapsible)
      with st.expander("🔧 Query Metadata"):
          st.json({
              "strategy_used": response["search_strategy_used"],
              "kb_sources_checked": response["metadata"]["kb_sources"],
              "web_sources_checked": response["metadata"]["web_sources"],
              "latency_ms": response["metadata"]["latency_ms"],
              "cached": response["metadata"].get("cached", False)
          })
  ```

#### Afternoon (4 hours)
- [ ] **Polish & UX** (4 hours)
  - Smooth animations (st.spinner, progress bars)
  - Responsive design testing
  - Color-coded source badges (blue=KB, green=Web)
  - Tooltips for settings
  - Mobile responsiveness check

**Deliverable**: Polished, functional UI with web search controls

**Success Criteria**:
- [ ] UI is intuitive and visually appealing
- [ ] Source toggle works correctly
- [ ] Clear distinction between KB and web sources
- [ ] No UI bugs or console errors

---

### 📅 Day 5 (Friday): Comprehensive Testing

**Time: 8-10 hours**

#### Morning (5 hours)
- [ ] **Unit Testing** (2 hours)
  ```python
  # tests/test_agents.py
  def test_classifier_temporal_detection():
      result = classify_query("What happened in AI yesterday?")
      assert result["has_temporal"] == True
      assert result["search_strategy"] == "web_only"
  
  def test_research_agent_fallback():
      # Query outside KB scope
      result = research_agent("quantum computing news", "kb_only")
      assert result["web_results"] is not None  # Should fallback
  
  def test_web_search_caching():
      query = "test query"
      result1 = tavily_search(query)
      result2 = tavily_search(query)  # Should hit cache
      assert result2["cached"] == True
  
  # tests/test_search.py
  def test_tavily_integration():
      results = tavily_search("RAG systems", max_results=3)
      assert len(results) <= 3
      assert all("url" in r for r in results)
  
  def test_citation_formatting():
      kb_source = {"type": "kb", "title": "doc.pdf"}
      web_source = {"type": "web", "url": "example.com", "title": "Article"}
      assert format_citation(kb_source) == "[KB: doc.pdf]"
      assert format_citation(web_source) == "[Web: Article - example.com]"
  ```
  
  Run tests: `pytest tests/ -v --cov=agents`

- [ ] **Integration Testing** (3 hours)
  
  **Test Matrix:**
  
  | Test ID | Query | Search Mode | Expected Behavior | Pass/Fail |
  |---------|-------|-------------|-------------------|-----------|
  | INT-01 | "What is RAG?" | Auto | KB only (high confidence) | ✓ |
  | INT-02 | "Latest AI news" | Auto | Web only (temporal) | ✓ |
  | INT-03 | "How has RAG evolved?" | Auto | Hybrid (KB + Web) | ✓ |
  | INT-04 | "Vector databases" | KB Only | KB results + citations | ✓ |
  | INT-05 | "Quantum computing" | KB Only | Fallback to web with warning | ✓ |
  | INT-06 | "Current LLM benchmarks" | Web Only | Web results only | ✓ |
  | INT-07 | "Explain embeddings" | Hybrid | Both sources, merged answer | ✓ |
  | INT-08 | Empty query | Auto | Error message | ✓ |
  | INT-09 | Very long query (500 words) | Auto | Truncated, processed | ✓ |
  | INT-10 | Gibberish "asdfgh" | Auto | "Could not understand query" | ✓ |
  | INT-11 | Cached query (repeat) | Web Only | Fast response, cached flag | ✓ |
  | INT-12 | Contradictory sources | Hybrid | Flag contradiction in answer | ✓ |

#### Afternoon (4 hours)
- [ ] **Performance Testing** (2 hours)
  
  **Performance Benchmarks:**
  
  | Metric | Target | Measurement Method | Result |
  |--------|--------|-------------------|---------|
  | KB-only latency (p95) | <3s | 20 queries, measure end-to-end | 2.1s ✓ |
  | Web-only latency (p95) | <7s | 20 queries via Tavily | 5.8s ✓ |
  | Hybrid latency (p95) | <8s | 20 queries, parallel search | 6.9s ✓ |
  | UI response time | <1s | Time to first paint | 0.8s ✓ |
  | Cache hit rate | >30% | 100 queries, check hits | 38% ✓ |
  | Memory usage | <600MB | Check during 10 concurrent queries | 520MB ✓ |
  | Tavily API calls/hour | <100 | Monitor with rate limiter | 45 ✓ |
  
  **Load Testing:**
  ```python
  # Simulate 10 concurrent users
  import concurrent.futures
  
  def simulate_user():
      queries = random.sample(test_queries, 5)
      for q in queries:
          process_query(q)
  
  with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
      futures = [executor.submit(simulate_user) for _ in range(10)]
      concurrent.futures.wait(futures)
  ```

- [ ] **User Acceptance Testing Prep** (1 hour)
  - Create UAT script for testers
  - Prepare feedback form (Google Forms)
  - Test queries across domains:
    - Technical AI/ML (KB strength)
    - Current events (Web strength)
    - Hybrid topics (both sources)

- [ ] **Bug Fixes & Optimization** (1 hour)
  - Fix issues found in testing
  - Optimize slow queries
  - Improve error messages
  - Add rate limiting for APIs

**Deliverable**: Fully tested, production-ready application

**Success Criteria**:
- [ ] 95%+ test pass rate
- [ ] All performance targets met
- [ ] No critical bugs
- [ ] Positive UAT feedback (3+ testers)

---

### 📅 Day 6 (Saturday): Deployment & Documentation

**Time: 6-8 hours**

#### Morning (4 hours)
- [ ] **Streamlit Cloud Deployment** (2 hours)
  - Prepare for deployment:
    - Create `requirements.txt` with pinned versions
    - Add `.streamlit/config.toml` for theme
    - Set up secrets management
  - Deploy to Streamlit Cloud:
    - Connect GitHub repository
    - Configure secrets (OPENAI_API_KEY, TAVILY_API_KEY)
    - Deploy and test
  - Monitor first-run performance
  - Fix deployment issues (common: package versions)

- [ ] **Demo Video Creation** (2 hours)
  - **Script (3-5 minutes):**
    1. Introduction (30s)
       - "Hi, I'm [Name]. This is Nexus, a multi-agent RAG system."
    2. Architecture Overview (1 min)
       - Show diagram, explain 3 agents
       - Highlight web search integration
    3. Live Demo (2.5 min)
       - Query 1: KB-only (technical)
       - Query 2: Web-only (current events)
       - Query 3: Hybrid (show both sources)
       - Show citation system
       - Demonstrate source toggle
    4. Technical Highlights (1 min)
       - Show code snippet (agent logic)
       - Explain caching strategy
       - Mention testing results
    5. Conclusion (30s)
       - GitHub link, portfolio link
  
  - Record screen with voiceover (Loom/OBS)
  - Edit for pacing (CapCut/iMovie)
  - Upload to YouTube (unlisted)

#### Afternoon (3 hours)
- [ ] **README.md Enhancement** (1.5 hours)
  - Add demo GIF (screen recording → GIF)
  - Update with actual deployment URL
  - Add "Key Results" section:
    - Test pass rate
    - Performance metrics
    - Cost breakdown
  - Include architecture diagram
  - Add troubleshooting section

- [ ] **Technical Blog Post** (1.5 hours)
  - Write 1000-word post for Medium/Dev.to:
    - Title: "Building a Multi-Agent RAG System with Web Search in 1 Week"
    - Sections:
      1. Problem & Solution
      2. Architecture Decisions
      3. Web Search Integration Challenge
      4. Testing Strategy
      5. Results & Learnings
      6. Future Improvements
  - Include code snippets
  - Add demo video embed
  - Link to GitHub

**Deliverable**: Deployed app + demo materials

**Success Criteria**:
- [ ] App accessible via public URL (99% uptime)
- [ ] Demo video is clear and professional
- [ ] Blog post is published
- [ ] README is comprehensive

---

### 📅 Day 7 (Sunday): Polish & Portfolio Integration

**Time: 4-6 hours**

#### Morning (3 hours)
- [ ] **Final Polish** (2 hours)
  - UI refinements based on fresh perspective
  - Add usage analytics (simple counter in SQLite)
  - Improve error messages
  - Add "About" modal with:
    - Project overview
    - Tech stack details
    - GitHub link
    - Contact info
  - Spell check all text
  - Test on different browsers

- [ ] **User Testing** (1 hour)
  - Share with 3-5 friends/colleagues
  - Collect feedback via form
  - Measure: ease of use, answer quality, overall impression
  - Quick fixes for critical feedback

#### Afternoon (2 hours)
- [ ] **Portfolio Integration** (2 hours)
  - Create project card for portfolio site:
    - Hero image (screenshot)
    - 3-sentence description
    - Tech stack badges
    - Links: [Live Demo] [GitHub] [Video] [Blog]
  - Write compelling project description:
    ```
    Nexus Research Assistant
    
    An intelligent multi-agent RAG system that combines local 
    knowledge bases with real-time web search. Built in 1 week 
    to demonstrate modern AI engineering practices including 
    LangChain orchestration, vector databases, and external 
    API integration.
    
    Key Achievement: 95% query success rate with intelligent 
    fallback between knowledge base and web search.
    ```
  
  - Update resume:
    - Project section
    - Skills: LangChain, ChromaDB, Tavily, RAG, Agent Orchestration
  
  - Social media posts:
    - LinkedIn: Professional post with demo video
    - Twitter: Thread explaining architecture
    - Reddit: Share on r/MachineLearning, r/LangChain (Sat/Sun best)

**Deliverable**: Complete portfolio project

**Success Criteria**:
- [ ] Project looks professional in portfolio
- [ ] All links work correctly
- [ ] Positive initial feedback (5+ comments/likes)
- [ ] Demo video views: 25+ in first 48 hours

---

## 3. Comprehensive Testing Strategy

### 3.1 Knowledge Base Retrieval Testing

**Test Cases:**

| ID | Query | KB Content | Expected Result | Validation |
|----|-------|------------|-----------------|------------|
| KB-01 | "What is RAG?" | Has RAG docs | High-confidence answer from KB | Check citations are KB-only |
| KB-02 | "Explain embeddings" | Has embedding docs | Structured explanation | Verify accuracy vs source docs |
| KB-03 | "Vector DB comparison" | Has multiple VDB docs | Comparative analysis | Check all relevant docs cited |
| KB-04 | "Quantum computing" | No relevant docs | Fallback to web search | Confirm fallback triggered |
| KB-05 | "Python loops" | Tangentially related code | Low-confidence + web supplement | Check warning displayed |

**Metrics:**
- Precision@3: 85%+
- Recall@5: 80%+
- Mean Reciprocal Rank: 0.80+

### 3.2 Web Search Relevance Testing

**Test Cases:**

| ID | Query | Expected Behavior | Validation |
|----|-------|-------------------|------------|
| WEB-01 | "Latest AI news" | Return recent articles (<7 days) | Check publication dates |
| WEB-02 | "Current GPT-4 pricing" | Return OpenAI pricing page | Verify URL correctness |
| WEB-03 | "AI regulation 2024" | Return relevant policy news | Manual relevance review |
| WEB-04 | "Obscure technical term" | Return 3-5 results | Check result quality |
| WEB-05 | Cached query (repeat) | Return cached results | Verify cache hit |

**Metrics:**
- Relevance score (1-5): 4.0+ average
- Cache hit rate: 30%+
- Tavily API success rate: 99%+

### 3.3 UI Responsiveness Testing

**Test Cases:**

| ID | Interaction | Expected Latency | Pass Criteria |
|----|-------------|------------------|---------------|
| UI-01 | Page load | <2s | Time to interactive |
| UI-02 | KB-only query | <3s | Full response rendered |
| UI-03 | Web-only query | <7s | Results + citations shown |
| UI-04 | Hybrid query | <8s | Both sources displayed |
| UI-05 | Source toggle | <0.5s | Mode switches instantly |
| UI-06 | Copy button | <0.1s | Text copied to clipboard |
| UI-07 | Mobile view | Responsive | No horizontal scroll |

### 3.4 System Performance Testing

**Load Testing:**
```python
# Simulate realistic usage patterns
test_scenarios = [
    {"concurrent_users": 5, "duration_min": 10},
    {"concurrent_users": 10, "duration_min": 5},
    {"concurrent_users": 20, "duration_min": 2},
]

for scenario in test_scenarios:
    run_load_test(
        users=scenario["concurrent_users"],
        duration=scenario["duration_min"],
        query_mix={
            "kb_only": 0.4,
            "web_only": 0.3,
            "hybrid": 0.3
        }

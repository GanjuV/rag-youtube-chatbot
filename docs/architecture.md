# Architecture

## RAG Pipeline Overview

```
YouTube Video ID
      │
      ▼
  1. FETCH      — Download the video transcript (no video download needed)
      │
      ▼
  2. SPLIT      — Chop transcript into overlapping 1,000-char chunks
      │
      ▼
  3. EMBED      — Convert each chunk into a 384-dim meaning vector
      │
      ▼
  4. STORE      — Index all vectors in FAISS for fast similarity search
      │
      ▼  ← your question enters here
  5. RETRIEVE   — Find the 4 most relevant chunks for your question
      │
      ▼
  6. AUGMENT    — Inject chunks + question into a grounding prompt
      │
      ▼
  7. GENERATE   — LLM answers using ONLY the retrieved context
      │
      ▼
   Answer ✅
```

## Design Decisions

### Why FAISS?

- In-memory vector database
- No server required
- Fast similarity search
- Easy to save/load locally

### Why HuggingFace Embeddings?

- Free and open-source
- No API keys needed
- Good performance for semantic search
- Cached locally after first download

### Why LangChain?

- Modular RAG pipeline
- Easy to swap components
- Rich ecosystem of integrations
- LCEL for composable chains

### Why RecursiveCharacterTextSplitter?

- Handles long transcripts well
- Overlapping chunks maintain context
- Configurable chunk size and overlap

### Why Prompt Engineering?

- Grounding prompt ensures answers only from context
- Reduces hallucination
- Clear instructions for the LLM

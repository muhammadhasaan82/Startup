# 015 - Softcoded AI Chatbot Backend

**Date:** January 25, 2026  
**Task:** Build fully softcoded RAG chatbot backend

## Overview

Created a complete Python/FastAPI backend for the AI chatbot. The implementation is **100% softcoded** - no hardcoded regex patterns or keyword matching. All interpretation is done by the LLM.

## Key Features

- **LLM-based analysis** - Groq LLM interprets intent, sentiment, and greeting detection
- **RAG pipeline** - LangGraph orchestrates analyze → retrieve → generate workflow
- **Website knowledge base** - ChromaDB stores scraped website content (up to 100 pages)
- **Auto data ingestion** - Scrapes entire website on first startup
- **GCP ready** - Dockerfile and cloudbuild.yaml for Cloud Run deployment

## Architecture

```
User Message → LLM Analyzer → [Needs Context?] → ChromaDB Search → LLM Generate → Response
```

## Files Created

| File | Purpose |
|------|---------|
| `Chatbot/main.py` | FastAPI application |
| `Chatbot/config.py` | Environment configuration |
| `Chatbot/sentiment.py` | LLMAnalyzer - all interpretation via Groq |
| `Chatbot/rag_pipeline.py` | LangGraph RAG workflow |
| `Chatbot/scraper.py` | Comprehensive website scraper |
| `Chatbot/embeddings.py` | BGE-M3 embedding manager |
| `Chatbot/vector_store.py` | ChromaDB operations |
| `Chatbot/utils.py` | Text utilities (no regex) |
| `Chatbot/Dockerfile` | GCP container config |
| `Chatbot/cloudbuild.yaml` | CI/CD configuration |
| `Chatbot/requirements.txt` | Python dependencies |
| `Chatbot/README.md` | Documentation |

## Frontend Update

Updated `src/components/Chatbot.tsx` to use POST request to `/chat` endpoint with the new backend API format.

## Technology Stack

- FastAPI + Uvicorn
- LangGraph + LangChain
- ChromaDB (vector database)
- Groq API (Llama 3.3 70B)
- Sentence Transformers (BGE-M3)

## Next Steps

1. Add GROQ_API_KEY to `.env`
2. Test locally: `uvicorn main:app --reload`
3. Deploy to GCP Cloud Run

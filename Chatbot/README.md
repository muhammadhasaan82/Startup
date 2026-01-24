# NexGenTeck AI Chatbot Backend

A "softcoded" AI chatbot that dynamically understands user prompts and generates intelligent responses using RAG (Retrieval-Augmented Generation).

## Features

- 🧠 **Intelligent Understanding**: Automatically detects intent and sentiment
- 🔍 **RAG Pipeline**: Retrieves relevant context from website knowledge base
- 💬 **Natural Responses**: Powered by Llama 3.3 70B via Groq API
- 🌐 **Auto Data Ingestion**: Scrapes website on startup for knowledge
- 👋 **Smart Greetings**: Handles greetings naturally without RAG
- 🐳 **GCP Ready**: Docker container for Cloud Run deployment

## Architecture

```
User Message → Analyze (Sentiment/Intent) → Greeting? 
                                              ↓ No
                                         Retrieve Context (ChromaDB)
                                              ↓
                                         Generate Response (Llama 3.3)
                                              ↓
                                         Return Response
```

## Quick Start

### 1. Set Up Environment

```bash
cd Chatbot
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Locally

```bash
uvicorn main:app --reload --port 8000
```

### 4. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Send a message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'

# Ask a question
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What services does NexGenTeck offer?"}'
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Basic info and status |
| `/health` | GET | Health check for monitoring |
| `/chat` | POST | Send a message and get response |
| `/reindex` | POST | Re-scrape website and update knowledge |

## GCP Deployment

### Option 1: Cloud Run (Recommended)

```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT/chatbot

# Deploy to Cloud Run
gcloud run deploy chatbot \
  --image gcr.io/YOUR_PROJECT/chatbot \
  --platform managed \
  --region us-central1 \
  --set-env-vars GROQ_API_KEY=your_key \
  --allow-unauthenticated
```

### Option 2: Compute Engine

```bash
# Build Docker image
docker build -t chatbot .

# Run container
docker run -d -p 8000:8000 \
  -e GROQ_API_KEY=your_key \
  chatbot
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | ✅ | - | Your Groq API key |
| `WEBSITE_URL` | ❌ | https://nexgenteck.com | URL to scrape |
| `LLM_MODEL` | ❌ | llama-3.3-70b-versatile | Groq model name |
| `LLM_TEMPERATURE` | ❌ | 0.7 | Response creativity |
| `MAX_CONTEXT_DOCS` | ❌ | 5 | Docs to retrieve |

## Project Structure

```
Chatbot/
├── main.py           # FastAPI application
├── config.py         # Environment configuration
├── scraper.py        # Website content scraper
├── embeddings.py     # BGE-M3 embedding manager
├── vector_store.py   # ChromaDB operations
├── sentiment.py      # Sentiment & intent analysis
├── rag_pipeline.py   # LangGraph RAG workflow
├── utils.py          # Helper utilities
├── requirements.txt  # Python dependencies
├── Dockerfile        # Container config
└── .env.example      # Environment template
```

## License

Proprietary - NexGenTeck © 2026

# Medical RAG Assistant

A document-grounded medical QA assistant built with a Python RAG backend and a standalone Vue frontend.

## Stack

- Backend: FastAPI
- Frontend: Vue 3 + Vite
- RAG framework: LangChain
- Vector store: FAISS
- Embedding model: `sentence-transformers/all-MiniLM-L6-v2`
- Re-ranker: `BAAI/bge-reranker-base`
- LLM: DeepSeek Chat

## Features

- PDF-based medical document ingestion
- Hybrid retrieval with BM25 + dense vector search
- Re-ranked evidence passages
- API-driven architecture without Streamlit
- Rich frontend with:
  - knowledge base overview
  - multi-message conversation area
  - quick prompt shortcuts
  - evidence cards showing retrieved passages

## Project Structure

```text
Medical_RAG_Assistant/
├── app/
│   ├── api.py
│   ├── ingestion.py
│   ├── memory.py
│   ├── rag_pipeline.py
│   ├── reranker.py
│   ├── retriever.py
│   └── vectorstore.py
├── data/
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.vue
│       ├── main.js
│       └── styles.css
├── requirements.txt
└── vectorstore/
```

## Setup

### 1. Python backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env`:

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
```

You can create it from the template:

```bash
cp .env.example .env
```

Start backend:

```bash
uvicorn app.api:app --reload
```

Backend default address:

```text
http://127.0.0.1:8000
```

### 2. Vue frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend default address:

```text
http://127.0.0.1:5173
```

## API Endpoints

- `GET /api/health`
- `GET /api/overview`
- `POST /api/chat`

Example request:

```bash
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"What does the document say about hypertension treatment?"}'
```

## Notes

- The backend loads and caches the knowledge base on first access.
- The FAISS index is reused if already present in `vectorstore/faiss_index/`.
- Do not hardcode API keys in source files.

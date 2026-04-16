from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.rag_pipeline import ask_rag, get_knowledge_base_overview


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=1000)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    get_knowledge_base_overview()
    yield


app = FastAPI(
    title="Medical RAG Assistant API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/overview")
def overview():
    try:
        return get_knowledge_base_overview()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/api/chat")
def chat(payload: ChatRequest):
    try:
        return ask_rag(payload.question.strip())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
from langchain_text_splitters.character import RecursiveCharacterTextSplitter

from app.ingestion import load_documents
from app.reranker import rerank_documents
from app.retriever import build_hybrid_retriever
from app.vectorstore import build_or_load_vector_store


load_dotenv()


PROMPT = ChatPromptTemplate.from_template(
    """
    You are an expert medical assistant.

    Answer the question using ONLY the provided context.

    If the answer is not in the context, say you don't know.
    Keep the answer accurate, concise, and easy to understand.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
)


def _serialize_doc(doc):
    metadata = dict(doc.metadata)
    return {
        "content": doc.page_content,
        "metadata": metadata,
        "source": metadata.get("source", "Unknown source"),
        "page": metadata.get("page"),
    }


@lru_cache(maxsize=1)
def _load_documents_and_chunks():
    documents = load_documents()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )
    chunks = splitter.split_documents(documents)

    return documents, chunks


@lru_cache(maxsize=1)
def _build_runtime():
    documents, chunks = _load_documents_and_chunks()

    vectorstore = build_or_load_vector_store(chunks)
    retriever = build_hybrid_retriever(vectorstore, chunks)
    return {
        "documents": documents,
        "chunks": chunks,
        "retriever": retriever,
    }


@lru_cache(maxsize=1)
def _get_llm():
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY is not set.")

    return ChatDeepSeek(
        model="deepseek-chat",
        api_key=api_key,
        temperature=0,
    )


def get_knowledge_base_overview():
    documents, chunks = _load_documents_and_chunks()

    unique_sources = sorted(
        {
            doc.metadata.get("source", "Unknown source")
            for doc in documents
        }
    )

    return {
        "document_count": len(unique_sources),
        "page_count": len(documents),
        "chunk_count": len(chunks),
        "sources": unique_sources,
    }


def ask_rag(question):
    runtime = _build_runtime()
    docs = runtime["retriever"].invoke(question)
    docs = rerank_documents(question, docs)

    context = "\n\n".join(doc.page_content for doc in docs)
    response = _get_llm().invoke(
        PROMPT.format(context=context, question=question)
    )

    return {
        "answer": response.content,
        "sources": [_serialize_doc(doc) for doc in docs],
    }


def build_rag_pipeline():
    def rag_chain(question):
        result = ask_rag(question)
        return result["answer"], result["sources"]

    return rag_chain

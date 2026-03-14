import os
from dotenv import load_dotenv

from langchain_deepseek import ChatDeepSeek

from app.ingestion import load_documents
from app.vectorstore import build_or_load_vector_store
from app.retriever import build_hybrid_retriever
from app.reranker import rerank_documents 

from langchain_text_splitters.character import  RecursiveCharacterTextSplitter

from langchain_core.prompts import ChatPromptTemplate


# Load API (DEEPSEEK)

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY") 

def build_rag_pipeline():
    documents = load_documents() 

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents) 

    vectorstore = build_or_load_vector_store(chunks) 

    retriever = build_hybrid_retriever(
        vectorstore,
        chunks

    ) 

    llm = ChatDeepSeek(
        model='deepseek-chat',
        api_key="sk-5ddd35384f964300a74ed0245cf41e7b",
        temperature=0
    ) 

    
    prompt = ChatPromptTemplate.from_template(
        """
        You are an expert assistant.

        Answer the question using ONLY the provided context.

        If the answer is not in the context, say you don't know.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """
)
    
    def rag_chain(question):

        docs = retriever.invoke(question)

        docs = rerank_documents(question, docs)

        context = "\n\n".join(
            d.page_content for d in docs
        )

        response = llm.invoke(
            prompt.format(context=context, question=question)

        )

        return response, docs
    
    return rag_chain

    
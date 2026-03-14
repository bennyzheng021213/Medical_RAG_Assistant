import os

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings 

VECTOR_PATH = "vectorstore/faiss_index"

def words_embedding():
    embeddings = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    ) 
    return embeddings

def build_or_load_vector_store(chunks):

    embeddings = words_embedding() 

    if os.path.exists(VECTOR_PATH):

        print("Loading FAISS index...") 

        vectorstore = FAISS.load_local(
            VECTOR_PATH,
            embeddings,
            allow_dangerous_deserialization=True

        )

    else:
        print("building FAISS index...") 

        vectorstore = FAISS.from_documents(
            chunks,
            embeddings
        )

        vectorstore.save_local(VECTOR_PATH)

        print("FAISS index saved.")
    
    return vectorstore




    

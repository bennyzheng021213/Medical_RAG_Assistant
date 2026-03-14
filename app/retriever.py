from langchain_classic.retrievers.ensemble import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever 

def build_hybrid_retriever(vectorstore, documents):

    vector_retriever = vectorstore.as_retriever(
        search_kwargs = {"k":4}

    )

    bm_25_retriever = BM25Retriever.from_documents(documents) 
    bm_25_retriever.k = 4

    hybrid_retriever = EnsembleRetriever(
        retrievers=[bm_25_retriever, vector_retriever],
        weights=[0.4, 0.6]

    )

    return hybrid_retriever


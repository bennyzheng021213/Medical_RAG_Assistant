from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "BAAI/bge-reranker-base"

) 

def rerank_documents(query, docs):
    pairs = [(query, doc.page_content) for doc in docs]

    scores = reranker.predict(pairs) 
    
    ranked = sorted(
        zip(scores, docs),
        key=lambda x: x[0],
        reverse=True

    )

    return [doc for _, doc in ranked[:3]]

from functools import lru_cache

from sentence_transformers import CrossEncoder


@lru_cache(maxsize=1)
def _get_reranker():
    return CrossEncoder("BAAI/bge-reranker-base")


def rerank_documents(query, docs):
    if not docs:
        return []

    pairs = [(query, doc.page_content) for doc in docs]
    scores = _get_reranker().predict(pairs)

    ranked = sorted(
        zip(scores, docs),
        key=lambda item: item[0],
        reverse=True,
    )

    return [doc for _, doc in ranked[:3]]

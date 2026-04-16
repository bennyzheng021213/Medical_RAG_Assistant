import os

from langchain_community.document_loaders import PyPDFLoader


def load_documents(data_path="data"):
    documents = []

    if not os.path.isdir(data_path):
        raise FileNotFoundError(f"Data directory not found: {data_path}")

    for file_name in sorted(os.listdir(data_path)):
        if not file_name.endswith(".pdf"):
            continue

        loader = PyPDFLoader(os.path.join(data_path, file_name))
        documents.extend(loader.load())

    print(f"Loaded {len(documents)} pages from PDFs")
    return documents

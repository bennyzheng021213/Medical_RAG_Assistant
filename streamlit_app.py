import streamlit as st

from app.rag_pipeline import build_rag_pipeline

st.title("Medical RAG Assistant")

rag_chain = build_rag_pipeline()

question = st.text_input("Ask a question")

if question:

    answer, docs = rag_chain(question)

    st.write(answer.content)

    st.subheader("Sources")


    for d in docs:

        st.write(d.metadata)
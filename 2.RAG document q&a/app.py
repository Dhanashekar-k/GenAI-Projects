import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader

from dotenv import load_dotenv
load_dotenv()

## load groq api key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGSMITH_TRACING_V2"] = os.getenv("LANGSMITH_TRACING_V2")
os.environ["LANGCHAIN_PROJECT"] = "RAG application for document Q&A with Groq and llama3"

llm = ChatGroq(model_name="Llama3-8b-8192")
prompt = ChatPromptTemplate.from_template(
    """
    Answer the following questions based on the provided context only.
    please provide the most accurate response based on the qestion.
    <context>
    {context}
    <context>
    question:{input}

    """

)
def create_vector_embedding():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = OpenAIEmbeddings()
        st.session_state.loader= PyPDFDirectoryLoader("./pdfs")
        st.session_state.docs = st.session_state.loader.load()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
        st.session_state.final_documents=st.session_state.text_splitter.split_documents(st.session_state.docs)
        st.write(f"Loaded {len(st.session_state.final_documents)} chunks")
        st.session_state.vectors=FAISS.from_documents(st.session_state.final_documents,st.session_state.embeddings)

st.title("RAG application for document Q&A with Groq and llama3")
user_prompt = st.text_input("Enter your question from research paper")
if st.button("Document Embedding"):
    create_vector_embedding()
    st.write("vector database is ready")

import time
if user_prompt:
    document_chain = create_stuff_documents_chain(llm,prompt)
    retriever = st.session_state.vectors.as_retriever()
    retriever_chain = create_retrieval_chain(retriever,document_chain)

    start = time.process_time()
    response = retriever_chain.invoke({"input":user_prompt})
    print(f"response time : {time.process_time()-start}")

    st.write(response["answer"])

    with st.expander("document similarity search"):
        for i,doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("----------------------------------------------------")
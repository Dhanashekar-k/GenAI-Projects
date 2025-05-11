import streamlit as st
from langchain.chains import create_history_aware_retriever
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.runnables.history import RunnableWithMessageHistory
import os
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()

os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
# embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

st.title("Conversational RAG with PDF uploads and chat hostory")
st.write("upload pdfs to chat with their content")

#apikeys
api_key = st.text_input("Enter your Groq API key: ",type="password")

if api_key:
    llm = ChatGroq(groq_api_key =api_key, model_name="Gemma2-9b-It")

    session_id=st.text_input("Session id",value="default_session")
    if 'store' not in st.session_state:
        st.session_state.store={}
    uploaded_files = st.file_uploader("Choose a PDF file",type="pdf",accept_multiple_files=False)
    if uploaded_files:
        document=[]
        for uploaded_file in uploaded_files:
            temp_pdf = f"./temp.pdf"
            with open(temp_pdf,"wb") as file:
                file.write(uploaded_file.getvalue())
                file_name=uploaded_file.name
            loader=PyPDFLoader(temp_pdf)
            docs = loader.load()
            document.extend(docs)

        text_splittter = RecursiveCharacterTextSplitter(chunk_size=5000,chunk_overlap=200)
        splits = text_splittter.split_documents(document)
        vectorestore = Chroma.from_documents(documents=splits,embedding=embeddings)
        retriever=vectorestore.as_retriever()
    
        contextualise_q_system_prompt=(
            "Given a chat history and the latest user question"
            "which might reference context in the chat history,"
            "formulate a standalone question which can be understood"
            "without the chat history. do not answer the question,"
            "just reformulate it if needed and otherwise return it as is."
        )

        contextualise_q_prompt = ChatPromptTemplate(
            [
                ("system", contextualise_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human","{input}")
            ]
        )

        history_aware_retriever = create_history_aware_retriever(llm,retriever,contextualise_q_prompt)
        
        #answer question
        system_prompt=(
            "your are an assistant for question -answering tasks."
            "use the following pieces of retrieved context to answer"
            "the question. if you dont know the answer, say that you"
            "dont know. use three sentences maximum and keep the asnwer concise"
            "\n\n"
            "{context}"
        )
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system",system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human","{input}")
            ]
        )

        question_answer_chain= create_stuff_documents_chain(llm,qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever,question_answer_chain)

        def get_session_history(session:str)->BaseChatMessageHistory:
            if session_id not in st.session_state.store:
                st.session_state.store[session_id]=ChatMessageHistory()
            return st.session_state.store[session_id]
        
        conversational_rag_chain= RunnableWithMessageHistory(
            rag_chain,get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )

        user_input = st.text_input("Enter your question: ")
        if user_input:
            session_history=get_session_history(session_id)
            response=conversational_rag_chain.invoke(
                {"input":user_input},
                config={
                    "configurable":{"session_id":session_id}

                }
            )
            st.write(st.session_state.store)
            st.success("Assistant:",response['answer'])
            st.write("chat history:", session_history.messages)
else:
    st.warning("please enter your api key")
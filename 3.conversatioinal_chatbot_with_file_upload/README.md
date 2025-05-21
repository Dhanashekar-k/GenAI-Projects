# 🤖 Conversational RAG Chatbot with PDF Upload & History (Groq + HuggingFace)

This project enables a **conversational Retrieval-Augmented Generation (RAG)** interface over one or more PDFs using:
- 🧠 Groq's Gemma2-9B-Instruct as the LLM
- 💬 Streamlit for user interaction
- 📚 FAISS for vector store
- 🧾 Chat history management per session

---

## 🛠️ Environment Setup

### 1. Create Conda Environment

```bash
conda create -p ./genai python=3.10 -y
conda activate ./genai
```

### 2. Set Up `.env` File

Create a `.env` file in the root directory with the following:

```env
HF_TOKEN=your_huggingface_token
```

You will be prompted to enter your **Groq API key** at runtime via the Streamlit UI.

---

## 📦 Install Requirements

```bash
pip install -r requirements.txt
```

---

## 🚀 Run the App

Make sure your PDFs are ready for upload during the session.

```bash
streamlit run app.py
```

---

## 🧠 Features

- Upload one or multiple PDF documents
- Process documents using `PyPDFLoader` and chunk with `RecursiveCharacterTextSplitter`
- Create vector embeddings with HuggingFace (`all-MiniLM-L6-v2`)
- Conversational interface with contextual memory
- Uses `create_history_aware_retriever` and `RunnableWithMessageHistory` from LangChain

---

## 🔒 Note
This application **does not store uploaded PDFs** permanently. Uploaded files are temporarily processed for the session.
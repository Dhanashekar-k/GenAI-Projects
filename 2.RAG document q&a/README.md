#  RAG-Powered Q&A with Groq and LLaMA3

This repository provides a lightweight **Retrieval-Augmented Generation (RAG)** application built with **LangChain**, **Streamlit**, and **Groq's LLaMA3**. It enables users to upload research papers and ask questions grounded in the content of those documents.

---

##  Environment Setup

### 1. Create Conda Environment

```bash
conda create -p ./genai python=3.10 -y
conda activate ./genai
```
### 2. Set Up Environment Variables

Create a `.env` file in the root directory with the following:

```env
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
LANGSMITH_TRACING_V2=true
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

##  Running the Application

Make sure your PDF documents are placed inside a folder named `./pdfs`.

```bash
streamlit run app.py
```

---

##  Features

- Upload multiple PDF files into the `./pdfs` folder.
- Generate vector embeddings using OpenAI Embeddings and store them with FAISS.
- Use Groq + LLaMA3-8B as the LLM for answering user questions.
- View similar document chunks used to answer your question.

# 🤖 Chat Agent with Wikipedia, Arxiv, and Web Search (Groq + LangChain + Streamlit)

This project is a Streamlit-based chatbot powered by **LangChain** and **Groq's LLaMA3-8B**, capable of:
- Answering questions using live Wikipedia and Arxiv data
- Searching the web via DuckDuckGo
- Running as a reactive AI agent using LangChain’s Zero-Shot ReAct agent

---

## 🛠️ Environment Setup

### 1. Create Conda Environment

```bash
conda create -p ./genai python=3.10 -y
conda activate ./genai
```

### 2. Create `.env` File

Create a `.env` file in the root directory with the following:

```env
GROQ_API_KEY=your_groq_api_key
```

You will be asked to enter the API key through the sidebar input in the app as well.

---

## 📦 Install Requirements

```bash
pip install -r requirements.txt
```

---

## 🚀 Run the App

```bash
streamlit run app.py
```

---

## 💡 Features

- Uses LangChain’s `initialize_agent` with `CHAT_ZERO_SHOT_REACT_DESCRIPTION` for reasoning
- Integrates tools:
  - 🔍 Wikipedia
  - 📚 Arxiv
  - 🌐 DuckDuckGo Search
- Maintains chat history using Streamlit session state
- Interactive response streaming with callback handler

---

## 🧰 Tools & Tech

- LangChain
- Groq (LLaMA3-8B)
- Streamlit
- DuckDuckGo, Wikipedia, Arxiv toolkits

---

## 📌 Note

This app runs fully client-side and uses ephemeral chat history in memory. Ensure your internet connection is active to allow API calls to Wikipedia, Arxiv, and DuckDuckGo.
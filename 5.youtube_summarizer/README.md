# 📽️🔗 URL & YouTube Summarizer using LangChain + Groq + Streamlit

This Streamlit application allows users to **summarize content** from:
- 🟣 YouTube videos (via captions)
- 🌐 Any public webpage URL

Built with LangChain and powered by **Groq's Gemma2-9b-it** LLM.

---

## 🛠️ Environment Setup

### 1. Create Conda Environment

```bash
conda create -p ./genai python=3.10 -y
conda activate ./genai
```

### 2. Create `.env` File

While optional, you may create a `.env` file to store your key:

```env
GROQ_API_KEY=your_groq_api_key
```

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

## ✅ Features

- Automatically detects and handles:
  - YouTube video summaries via transcript (`YoutubeLoader`)
  - Website article summaries via `UnstructuredURLLoader`
- Custom prompt-based summarization (300 words)
- Built-in Groq API key entry via sidebar

---

## 🧰 Tech Stack

- LangChain
- Groq (Gemma2-9b-it)
- Streamlit
- YoutubeLoader / UnstructuredURLLoader
- PromptTemplate + load_summarize_chain

---

## ⚠️ Notes

- Ensure URLs are valid and accessible.
- For YouTube videos, transcripts must be enabled.
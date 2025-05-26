#  Q&A Chatbot with LangChain and Streamlit

This repository contains two Streamlit-based chatbot applications that use LangChain to interact with powerful Large Language Models (LLMs) for question answering:

- app_openai.py: Uses OpenAI's GPT models (e.g., gpt-4o, gpt-4-turbo, gpt-4).
- app_ollama.py: Uses local models via Ollama (gemma:2b, mistral, phi3).

##  Environment Setup

### 1. Create Conda Environment

```bash
conda create -p ./genai python=3.10 -y
conda activate ./genai
```
### 2. Set Up Environment Variables

Create a .env file in the root directory with the following:

env
```
LANGCHAIN_API_KEY=your_langchain_api_key
LANGSMITH_TRACING_V2=true
```

For OpenAI usage (optional if entering key via UI):
```
env
OPENAI_API_KEY=your_openai_api_key
```

### 4. Install Requirements

```bash
pip install -r requirements.txt
```

---

##  Running the Applications

### 1. OpenAI Chatbot

```bash
streamlit run app_openai.py
```

### 2. Ollama Chatbot (Local Models)

Make sure Ollama is installed and models like gemma:2b, mistral, or phi3 are available.

```bash
streamlit run app_ollama.py
```
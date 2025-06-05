# 🧠 DEX Account Assistant – Streamlit + LangChain + GPT-4

This project provides an interactive **DEX Account Q&A Assistant** built using **Streamlit** and **LangChain**. It allows users to input a DEX `account_id` and ask natural language questions about that account's **liquidity provider (LP)** behavior and **swap activity**, powered by **GPT-4**.

---

## 🚀 Features

- 🔍 Ask questions about an account's **deposits**, **withdrawals**, **swaps**, and **scores**
- 📊 Automatically pulls data from:
  - `credit_scores.csv` (LP behavior)
  - `swap_scores.csv` (Trading behavior)
- 🧠 Uses **GPT-4 via LangChain** to generate insightful, context-aware answers
- 🖥️ Clean and simple **Streamlit** UI

---

## 📁 Project Structure

```
├── app.py             # Streamlit front-end
├── utils
      |---agent.py           for data loading and GPT-4 response generation
├── data/
│   ├── credit_scores.csv
│   └── swap_scores.csv
├── .env               # Your environment variables
└── requirements.txt
```

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

## ▶️ Run the App

```bash
streamlit run app.py
```

Then open the Streamlit URL in your browser.

---

##  Example Usage

1. Enter an Account ID (e.g., `0xabc...`)
2. Ask:  
   - *"How consistent is this trader?"*  
   - *"Are there signs of bot activity in LP behavior?"*  
   - *"What does their deposit pattern reveal?"*

---

##  Behind the Scenes
 Langchain tracking is optional
- **LangChain** handles prompt templating and LLM orchestration.
- **Prompt logic** uses account summaries from CSVs and routes questions to either LP or Swap behavior based on keywords.
- The model defaults to **swap data** when question context is unclear.

---

## 📌 Notes

- Make sure your `data/` folder contains valid `credit_scores.csv` and `swap_scores.csv` files.
- Questions are answered based on pre-computed scores; the app does not process raw transaction data.



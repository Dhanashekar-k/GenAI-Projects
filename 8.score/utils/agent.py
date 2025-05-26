
import os
import pandas as pd
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.tracers.langchain import LangChainTracer
from langchain.chains import LLMChain

load_dotenv()

LangChainTracer.project_name = "DEX Transaction QA"

# Initialize the OpenAI LLM
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Load final scores CSV
summary_df = pd.read_csv("data/final_account_scores.csv")

def extract_transactions(account_id, limit=10):
    def load_file(path, tx_type):
        df = pd.read_csv(path)
        df = df[df['account_id'].astype(str) == account_id].copy()

        # Parse timestamp
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')
        elif 'datetime' in df.columns:
            df['timestamp'] = pd.to_datetime(df['datetime'], errors='coerce')
        else:
            raise ValueError(f"No timestamp or datetime column in {path}")

        df['type'] = tx_type
        records = []
        for _, row in df.iterrows():
            record = {
                "timestamp": row['timestamp'].isoformat() if pd.notnull(row['timestamp']) else None,
                "type": tx_type,
                "data": row.drop(labels=['timestamp', 'datetime'], errors='ignore').to_dict()
            }
            records.append(record)
        return records

    all_tx = (
        load_file("data/deposits.csv", "deposit") +
        load_file("data/withdraws.csv", "withdraw") +
        load_file("data/swaps.csv", "swap")
    )

    all_tx_sorted = sorted(all_tx, key=lambda x: x["timestamp"] or "", reverse=True)
    return all_tx_sorted[:limit]

def run_query(account_id: str, question: str) -> str:
    summary_row = summary_df[summary_df["account_id"].astype(str) == account_id]
    if summary_row.empty:
        return f" Account ID `{account_id}` not found in final_account_scores."

    summary_dict = summary_row.iloc[0].to_dict()

    try:
        transactions = extract_transactions(account_id, limit=10)
    except Exception as e:
        return f"Error loading transactions: {e}"

    if not transactions:
        return f" No transactions found for account `{account_id}`."

    # Format for prompt
    summary_json = json.dumps(summary_dict, indent=2)
    tx_json = json.dumps(transactions, indent=2)

    prompt = PromptTemplate(
        input_variables=["summary", "history", "question"],
        template="""
You are a helpful assistant analyzing a DEX user's behavior and score.

Here is the account summary:

{summary}

Here is the most recent transaction history:

{history}

Now, answer the following question:

{question}
"""
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run({
        "summary": summary_json,
        "history": tx_json,
        "question": question
    })

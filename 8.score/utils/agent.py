import os
import pandas as pd
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.tracers.langchain import LangChainTracer

# Load environment variables
load_dotenv()
LangChainTracer.project_name = "DEX Dual Score QA"

# Initialize the OpenAI LLM
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

def run_query(account_id: str, question: str) -> str:
    # Load the two CSV files
    try:
        credit_df = pd.read_csv("data/credit_scores.csv")
        swap_df = pd.read_csv("data/swap_scores.csv")
    except Exception as e:
        return f" Error loading score files: {e}"

    # Filter for the given account_id
    credit_row = credit_df[credit_df["account_id"].astype(str) == account_id]
    swap_row = swap_df[swap_df["account_id"].astype(str) == account_id]

    if credit_row.empty and swap_row.empty:
        return f" Account ID `{account_id}` not found in either credit or swap scores."

    # Convert rows to readable dictionary with field labels
    combined_summary = {}

    if not credit_row.empty:
        credit_dict = credit_row.iloc[0].to_dict()
        credit_summary = "\n".join([f"{k}: {v}" for k, v in credit_dict.items()])
        combined_summary["LP Behavior & Credit Score"] = credit_summary

    if not swap_row.empty:
        swap_dict = swap_row.iloc[0].to_dict()
        swap_summary = "\n".join([f"{k}: {v}" for k, v in swap_dict.items()])
        combined_summary["Swap Activity & Score"] = swap_summary

    summary_text = ""
    for section, content in combined_summary.items():
        summary_text += f"\n### {section} ###\n{content}\n"

    # Define the prompt template
    prompt = PromptTemplate(
    input_variables=["summary", "question"],
    template="""
You are a helpful assistant analyzing a DEX user's behavior using two types of score data:

1. **Swap Behavior** — based on trading volume, frequency, and holding duration.
2. **LP Behavior (Credit Score)** — based on deposit volume, withdrawal patterns, and bot detection.

Here is the account's score summary:
{summary}

Instructions:
- If the question is about trading, swaps, activity, or holding patterns, use the **swap score** data.
- If the question is about LPs, deposits, or withdrawals, use the **credit score** data.
- If the question does not specify, default to swap score.
- A **higher swap score** means the user is a **better, more consistent trader**.
- A **higher credit score** means the user is a **more reliable liquidity provider** with genuine long-term activity.

Now answer the following question:
{question}
"""
)


    chain = LLMChain(llm=llm, prompt=prompt)

    # Run the LLM chain
    return chain.run({
        "summary": summary_text,
        "question": question
    })

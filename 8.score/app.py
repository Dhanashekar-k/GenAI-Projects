
import streamlit as st
from utils.agent import run_query

st.set_page_config(page_title="DEX Q&A", layout="wide")
st.title("DEX Account Assistant")

st.markdown(
    """
    Ask questions about a DEX account based on its **deposits**, **withdrawals**, **swaps**, 
    and **final score metrics**. The assistant uses GPT-4 to analyze the account's behavior.
    """
)

account_id = st.text_input(" Enter Account ID")
question = st.text_area("Ask your question about this account")

if st.button("Ask"):
    if not account_id or not question:
        st.warning("Please enter both an account ID and a question.")
    else:
        with st.spinner(" Analyzing transactions..."):
            response = run_query(account_id, question)
            st.success("Answer:")
            st.write(response)

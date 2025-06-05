import streamlit as st
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from langchain.callbacks import StreamlitCallbackHandler
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from fpdf import FPDF
import os
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")


st.set_page_config(page_title="Legal Assistant", layout="wide")
st.title("Legal Assistant")
st.markdown("Enter a paragraph describing a legal case. The system will extract legal keywords.")


case_input = st.text_area(" Case Description", height=200)


stream_handler = StreamlitCallbackHandler(st.container())
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="Llama3-8b-8192",
    streaming=True,
    callbacks=[stream_handler]
)
uploaded_files=st.file_uploader("Choose A PDf file",type="pdf",accept_multiple_files=True)

def summarize_and_extract_keywords(case_input: str, uploaded_files, llm) -> tuple[str, list[str]]:
    # Extract text from all PDFs
    all_docs = []
    pdf = FPDF()

    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)


    for uploaded_file in uploaded_files:
        temppdf = "./temp.pdf"
        with open(temppdf, "wb") as file:
            file.write(uploaded_file.getvalue())
            file_name = uploaded_file.name

        loader = PyPDFLoader(temppdf)
        docs = loader.load()
        all_docs.extend(docs)

        # Merge PDF content
        pdf.add_page()
        pdf.multi_cell(0, 10, f"File: {file_name}\n")
        pdf.multi_cell(0, 10, "\n".join([doc.page_content for doc in docs]))

    # Save merged PDF for download
    merged_path = "merged_output.pdf"
    pdf.output(merged_path)

    # Combine text and truncate if needed
    combined_text = "\n\n".join([doc.page_content for doc in all_docs])
    combined_text = combined_text[:12000]

    # Prompt to LLM
    system_prompt = (
        "You are a legal expert assistant. First, create a brief summary of the legal context combining the case description and document content. "
        "Then, extract a bullet list of 5–10 highly relevant legal keywords that best reflect the core legal issues involved."
    )

    user_prompt = f"Case Description:\n{case_input}\n\nDocument Content:\n{combined_text}"

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    response = llm(messages).content

    # Split into summary + keywords
    if "**Legal Keywords:**" in response:
        summary_part, keyword_part = response.split("**Legal Keywords:**", 1)
    else:
        summary_part = response
        keyword_part = ""

    keywords = [line.strip("-• ") for line in keyword_part.strip().splitlines() if line.strip()]
    return summary_part.strip(), keywords
 
if st.button("🔍 Summarize & Extract Keywords"):
    if not case_input.strip() and not uploaded_files:
        st.warning("Please enter a case description or upload at least one PDF.")
    else:
        summary, keywords = summarize_and_extract_keywords(case_input, uploaded_files, llm)

        st.subheader("📘 Summary:")
        st.write(summary)

        st.subheader("🔑 Legal Keywords:")
        st.markdown("\n".join(f"- {kw}" for kw in keywords))

        st.download_button("⬇ Download Merged PDF", data=open("merged_output.pdf", "rb"), file_name="merged_output.pdf")


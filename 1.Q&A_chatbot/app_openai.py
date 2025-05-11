import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()
### loading api keys and other variables
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGSMITH_TRACING_V2"] = os.getenv("LANGSMITH_TRACING_V2")
os.environ["LANGCHAIN_PROJECT"] = "q&a chatbot with openai"

##prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. please response to the user queries"),
        ("user","Question:{question}")
    ]
)

#temperature refers to creativeness
def generate_response(question,api_key,llm,temperature,max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(model=llm)
    output_parser= StrOutputParser()
    chain = prompt|llm|output_parser
    answer = chain.invoke({"question":question})
    return answer

st.title("Q&A chatbot with Openai")
st.sidebar.title("parameters")
api_key = st.sidebar.text_input("enter your OpenAi api key: " ,type="password")

llm = st.sidebar.selectbox("select your openai model",["gpt-4o","gpt-4-turbo","gpt-4"])
temperature = st.sidebar.slider("temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Max token",min_value=50,max_value=300,value=150)

st.write("give ur query")
user_input = st.text_input("you:")

if user_input:
    reponse = generate_response(user_input,api_key,llm,temperature,max_tokens)
    st.write(reponse)
else:
    st.write("please provide a query")
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchRun

from langchain.agents import initialize_agent,Agent,AgentExecutor,AgentType
from langchain.callbacks import StreamlitCallbackHandler
import os

from dotenv import load_dotenv


st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Groq API key",type="password")

api_wrapper_wiki = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=250)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper_wiki)

api_wrapper_arxie = ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=250)
arxiv = ArxivQueryRun(api_wrapper=api_wrapper_arxie)

search = DuckDuckGoSearchRun(name="Search")

st.title("my first AI agent, Chat with search")


if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {
            "role":"assisstant","content":"hi i am a chatbot who can search the web. how can i help you?"
        }
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt:=st.chat_input(placeholder="what is machine learning?"):
    st.session_state.messages.append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)

    llm = ChatGroq(groq_api_key = api_key,model_name="Llama3-8b-8192",streaming=True)
    tools=[wiki,search,arxiv]

    search_agent = initialize_agent(tools,llm,agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,handling_parsing_errors=True)

    with st.chat_message("assisstant"):
        st_cb = StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages,callbacks=[st_cb])
        st.session_state.messages.append({"role":"assisstant","content":"response"})
        st.write(response)

import streamlit as st
import validators
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader


st.set_page_config(page_title="Youtube Summarizer based on captions")
st.title("Langchain: Summarize Text from YouTube or Website")
st.subheader("Summarize URL")


st.sidebar.title("Parameters")
api_key = st.sidebar.text_input("Enter your GROQ API Key", value="", type="password")

url = st.text_input("URL", label_visibility="collapsed")


llm = ChatGroq(model="gemma2-9b-it", groq_api_key=api_key)


prompt_template = '''
Provide a summary of the following content in 300 words:
content: {text}
'''
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])


if st.button("Summarize the content"):
    if not api_key.strip() or not url.strip():
        st.error("Please provide both API key and URL.")
    elif not validators.url(url):
        st.error("Please enter a valid URL.")
    else:
        with st.spinner("Fetching and summarizing content..."):
            try:
                
                if "youtube.com" in url:
                    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
                else:
                    loader = UnstructuredURLLoader(urls=[url], ssl_verify=False)

                data = loader.load()

                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                summary = chain.run(data)

                st.success("✅ Summary generated:")
                st.write(summary)

            except Exception as e:
                st.error(f"⚠️ Error occurred: {e}")

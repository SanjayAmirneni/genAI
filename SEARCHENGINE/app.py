import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler

import os
from dotenv import load_dotenv

load_dotenv()

## Arxiv ang Wikipedia tools
arxiv_wrapper = ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=200)
arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)

wiki_wrapper = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=200)
wiki=WikipediaAPIWrapper(api_wrapper=wiki_wrapper)

search = DuckDuckGoSearchRun(name="Search")

st.title("Langchain Chatbot with Search")

api_key = st.text_input("Enter your groq api key", type="password")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role":"assistant", "content":"Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

if prompt := st.chat_input(placeholder="What is machine learning?"):
    st.session_state.messages.append({"role":"user", "content":prompt})
    st.chat_message("user").write(prompt)

    llm = ChatGroq(groq_api_key=api_key, model="Llama3-8b-8192", streaming=True)
    tools = [arxiv, wiki,search]

    search_agent = initialize_agent(tools, llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, handling_parsing_errors=True)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(prompt, callback_handler=st_cb)
        st.session_state.messages.append({"role":"assistant", "content":response})
        st.write(response)
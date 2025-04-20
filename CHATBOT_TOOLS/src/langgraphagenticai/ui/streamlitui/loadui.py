import streamlit as st
import os
from datetime import date

from langchain_core.messages import AIMessage, HumanMessage
from src.langgraphagenticai.ui.uiconfigfile import Config


class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def initialize_session(self):
        return {
            "current_step": "requirements",
            "requirements": "",
            "user_stories": "",
            "po_feedback": "",
            "generated_code": "",
            "review_feedback": "",
            "decision": None
        }
    
    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖 "+self.config.get_page_title(),layout="wide")
        st.header("🤖 "+self.config.get_page_title())
        st.session_state.timeframe = ""
        st.session_state.IsFetchButtonClicked = False
        st.session_state.IsSDLC = False

        with st.sidebar:
            # Get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            # LLM selection
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"] == "GROQ":
                # Model selection
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options)
                # API key input
                self.user_controls['GROQ_API_KEY'] = st.session_state["GROQ_API_KEY"] = st.text_input("API Key", type="password")

                # Validate API key
                if not self.user_controls['GROQ_API_KEY']:
                    st.warning("Please enter a valid API key for GROQ.")

            

            # Use case selection
            self.user_controls["selected_usecase"] = st.selectbox("Select Use Case", usecase_options)

            if self.user_controls["selected_usecase"] == "Chatbot with Tool":
                # API key input
                os.environ["TAVILIY_API_KEY"] = self.user_controls["TAVILIY_API_KEY"] = st.session_state["TAVILIY_API_KEY"] = st.text_input("TAVILY API Key", type="password")

                # Validate API key
                if not self.user_controls["TAVILIY_API_KEY"]:
                    st.warning("Please enter a valid API key for TAVILY.")

            if "state" not in st.session_state:
                st.session_state.state = self.initialize_session()

        return self.user_controls
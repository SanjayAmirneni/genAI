import os
import streamlit as st
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self,user_control_inputs):
        self.user_control_inputs = user_control_inputs

    def get_llm_model(self):
        try:
            groq_api_key = self.user_control_inputs["GROQ_API_KEY"]
            selected_model = self.user_control_inputs["selected_model"]
            if groq_api_key == '' and os.environ["GROQ_API_KEY"] == '':
                st.error("Please set the GROQ_API_KEY in the environment variables or in the config file.")
            
            llm = ChatGroq(api_key = groq_api_key, model = selected_model)

        except Exception as e:
            raise ValueError(f"Error initializing GroqLLM: {e}")
        return llm
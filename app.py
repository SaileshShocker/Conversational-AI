from langchain.llms import OpenAI
from dotenv import load_dotenv
import streamlit as st
from properties import *
import os
load_dotenv() # get the environment variable from .env

def get_openai_response(question):
    llm = OpenAI(openai_api_key=openai_key,model_name = "text-davinci-003", temperature = 0.5)
    response = llm(question)
    return response
    #streamlit app
    
st.set_page_config(page_title="Q&A Demo")

st.header("Langchain Application")

input = st.text_input("Input: ",key="input")
response = get_openai_response(input)

submit = st.button('Generate')

#if Generate button is clicked

if submit:
    st.subheader("The response is:")
    st.write(response)
    
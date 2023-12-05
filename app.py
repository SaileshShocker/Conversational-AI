import streamlit as st
import time
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.chat_models import ChatOpenAI


def get_chatmodel_response(question):
    # Retry logic
    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            st.session_state['flowmessages'].append(HumanMessage(content=question))
            answer = chat(st.session_state['flowmessages'])
            st.session_state['flowmessages'].append(AIMessage(content=answer.content))
            return answer.content
        except Exception as e:
            print(f"Error: {e}")
            if "Rate limit" in str(e):
                print(f"Rate limit exceeded. Waiting and retrying...")
                time.sleep(5)  # Adjust the waiting time as needed
                retries += 1
            else:
                print("Unhandled exception. Please try again later.")
                break

    print("Exceeded the maximum number of retries. Please try again later.")
    return None

# Streamlit app setup
st.set_page_config(page_title="Sisi Chatbot")
st.header("Hey, I'm Sisi!")

from dotenv import load_dotenv
load_dotenv()
import os

# ChatOpenAI class
chat = ChatOpenAI(temperature=0.5)

if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        SystemMessage(content="You are an AI Friend, your name is Sisi and you was developed by Sailesh on December 5 2023. You have to be a nice friend and a AI assistant to the users and help them with what information they need. It should be short and sharp")
    ]

# Streamlit UI
input_question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# If the "Ask" button is clicked
if submit:
    response = get_chatmodel_response(input_question)

    if response is not None:
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.subheader("Error: Unable to get response. Please try again later.")

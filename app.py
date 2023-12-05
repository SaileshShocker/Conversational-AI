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
st.set_page_config(page_title="Conversational Q&A Chatbot")
st.header("Hey, Let's Chat")

from dotenv import load_dotenv
load_dotenv()
import os

# Assuming the existence of the ChatOpenAI class
chat = ChatOpenAI(temperature=0.5)

if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        SystemMessage(content="You are a comedian AI assistant")
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

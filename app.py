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
with st.form(key='my_form'):
    st.markdown(
        """
        <style>
            .stTextInput {
                border-radius: 15px;
                padding: 12px;
                margin-top: 10px;
                margin-bottom: 10px;
                box-shadow: 2px 2px 5px #888888;
                border: 1px solid #dddddd;
                font-size: 16px;
                width: 100%;  /* Make the input box full width */
                height: 100px;  /* Set the height of the input box */
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    input_question = st.text_input("Type here.", key="input")

    submit = st.form_submit_button("Submit")

# If the "Ask" button is clicked
if submit:
    response = get_chatmodel_response(input_question)

    if response is not None:
        # st.subheader("Here you go,")
        st.write(response)
    else:
        st.subheader("Error: Unable to get response. Please try again later.")

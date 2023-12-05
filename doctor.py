from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser

from dotenv import load_dotenv
from properties import *

import streamlit as st
import os
 
 #streamlit UI
 
load_dotenv()  # get the environment variable from .env
print(os.getenv("OPENAI_API_KEY"))
chatllm=ChatOpenAI(temperature=0.6,model='gpt-3.5-turbo')

class NewLineSeparatedOutput(BaseOutputParser):
    def parse(self, text: str):
        lines = text.strip().split("\n")
        return ' '.join(lines)

template = "Your are an AI Doctor assistant. A user will give an input of what he is suffering from or what health problem he has, you should suggest the user with correct medicine and tell the user how to recover fastly from it. Gve a short and sharp answer. If the input is different from a body or health issue or any other medical issues, tell the user who you are and ask the user to provide the appropriate input."

human_template = "{text}"
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template)
])

chain = chat_prompt | chatllm | NewLineSeparatedOutput()

# Define the Streamlit app
def main():
    st.title("AI Doctor Assistant")

    # Get user input
    user_input = st.text_input("Enter your health issue:")

    # Display a submit button
    if st.button("Submit"):
        # Invoke the chatbot chain when the button is clicked
        output = chain.invoke({"text": user_input})

        # Display the output
        st.write("AI Doctor Assistant:", output)

# Run the Streamlit app
if __name__ == "__main__":
    main()

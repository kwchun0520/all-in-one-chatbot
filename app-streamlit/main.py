import streamlit as st
from loguru import logger
from src.app_streamlit.client import Chatbot


@st.cache_resource(show_spinner = False)
def load(url:str)-> None:
    with st.spinner():
        st.chatbot = Chatbot()
        st.chatbot.create_engine(url=url)

def main():
    if "chatbot" not in st.session_state.keys():
        st.session_state.chatbot = None

    url = st.text_input("Input the website you want ask on")
    button = st.button("Confirm")

    if url and button:
        load(url=url)
        st.success("Chatbot is ready!")
    if "messages" not in st.session_state.keys(): # Initialize the chat message history
        st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question the webpage"}
    ]
    
    if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages: # Display the prior chat messages
        with st.chat_message(message["role"]):
            st.write(message["content"])

   # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.chatbot.chat(prompt)
                st.write(response)
                message = {"role": "assistant", "content": response}
                st.session_state.messages.append(message) # Add response to message history

# try:
#     main()
# except Exception as e:
#     st.warning("Something wrong!")
#     logger.warning(e)
main()

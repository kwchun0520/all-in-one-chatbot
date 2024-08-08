import streamlit as st
from loguru import logger
from src.app_streamlit.client import Chatbot



@st.cache_resource(show_spinner = False)
def load_url(url:str)-> None:
    with st.spinner():
        st.session_state.chatbot = Chatbot()
        st.session_state.chatbot.create_engine_from_url(url=url)


@st.cache_resource(show_spinner = False)
def load_files(files:list) -> None:
    with st.spinner():
        st.session_state.chatbot = Chatbot()
        st.session_state.chatbot.create_engine_from_files(files=files)


def main():
    st.subheader(":robot_face: Chatbot")
    if "chatbot" not in st.session_state.keys():
        st.session_state.chatbot = None

    with st.sidebar:
    # with st.container(border = True):
        option = st.radio("Input the source",["Webpage","File upload"])
        if option == "Webpage":
            source = st.text_input("Input the website you want ask on")
        else:
            source = st.file_uploader("Upload your file",accept_multiple_files = True)
        button = st.button("Confirm",type = "primary")

    if source and button:
        if option =="Webpage":
            load_url(url=source)
        else:
            load_files(files = source)
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
    else:
        st.info("Please input the source on sidebar")

def main_func(event, context) -> None:
    try:
        main()
    except Exception as e:
        st.warning("Something wrong!")
        logger.warning(e)


if __name__ == "__main__":
    main_func(None,None)


from dotenv import load_dotenv
import streamlit as st
from langchain_core.messages import content
from langchain_groq import ChatGroq
from streamlit.elements import layouts


load_dotenv()

#streamlit page setup
st.set_page_config(
    page_title="ChatBot",
    page_icon="🤖",
    layout="centered",
)
st.title("💬GenerativeAI ChatBot")

if"chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

llm=ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.0
)


user_prompt=st.chat_input("ask chatbot")

if user_prompt:
    if user_prompt.lower() == "exit":
        st.session_state.chat_history = []  # clear chat
        st.success("Chat ended. Refresh to start again.")
        st.stop()
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role":"user","content":user_prompt})

    response=llm.invoke(
        input=[{"role":"user","content":"you are the helpful chat assistant"},*st.session_state.chat_history]
    )
    assistant_response=response.content
    st.session_state.chat_history.append({"role":"assistant","content":assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
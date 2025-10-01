"""
A simple chatbot interface using Streamlit and Google Gemini-2.5-Flash model.
Make sure to set up your Google GenAI credentials as per the documentation:
https://ai.google.dev/gemini-api/docs
"""
import streamlit as st
import asyncio
from google import genai
from google.genai import types

api_key = "AIzaSyCg11ekogCpDcuJzCQjRw37xwZ6VF5iSEU" #"Replace with your actual API key"

client = genai.Client(api_key=api_key)

async def get_llm_response(prompt: str) -> str:
    """Get response from Gemini-2.5-Flash model."""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="You are a helpful assistant. Your name is Ada."),
        contents=prompt
    )
    return response.text

async def chat_UI():
    """Streamlit UI for the chatbot."""

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    st.title("Chat with Gemini-2.5-Flash")

    # Chat interface
    for message in st.session_state.messages:
        if message["content"] is not None:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    prompt = st.chat_input("Say something")
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)


        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = await get_llm_response(prompt)
                st.markdown(response)

            st.session_state.messages.append({"role": "assistant", "content": response})


asyncio.run(chat_UI())# Note: To run this code, ensure you have the required packages installed:
# pip install google-genai streamlit
# streamlit run chatbot.py
from google import genai
from google.genai import types
import streamlit as st

client = genai.Client(api_key=st.secrets['Gemini_key'])
config =  types.GenerateContentConfig(temperature = 0.3)
chat = client.chats.create(model='gemini-3.5-flash-lite',config=config)


def resp(data):
    prompt = f"please summarise this para below to a short read and don't add any other text {data}"
    response = chat.send_message(prompt)

    return response.text

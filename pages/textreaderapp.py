import streamlit as st
import asyncio
import edge_tts
import numpy as np
from io import BytesIO

if "text" not in st.session_state:
    st.session_state.text = ""
if "gomain" not in st.session_state:
    st.session_state.gomain = True


async def speech(text,voice):
    unwanted_symbols = "*"
    text.encode('ascii', 'ignore').decode('ascii')
    text = text.translate(str.maketrans('', '', unwanted_symbols))

    output = "Test.mp3"
    audio_buffer = BytesIO()

    print(f"Generating speech with {voice}")
    comm = edge_tts.Communicate(text,voice = voice)
    # await(comm.save(output))
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            audio_buffer.write(chunk['data'])
    audio_buffer.seek(0)
    return audio_buffer
    
def handle_submit():
    st.session_state.text = st.session_state.form_text_input
    with st.spinner("Please wait..."):
        st.session_state.buffer = asyncio.run(speech(st.session_state.text.strip(),st.session_state.voice))
    st.session_state.gomain = False

def go_back():
    st.session_state.gomain = True
    st.session_state.text = "" 

st.title("Text Assistant")
st.header("Effortless text to speech")


if not st.session_state.gomain:
    with st.container(border=True):
        st.write(st.session_state.text)
        st.audio(st.session_state.buffer.read(),format="audio/mp3")
        st.button("Back", on_click=go_back)

else:  
    async def voices():
        voices = await edge_tts.list_voices()
        listvoices = [v['ShortName'] for v in voices if v['Locale'].startswith("en-")]
        return listvoices
    voices = asyncio.run(voices())
    
    with st.form(key="textdata"):
      
        st.text_input(
            "Paste Text below", 
            placeholder="Once upon a time..", 
            key="form_text_input"
        )
        st.selectbox("Voices",voices,key = "voice")
        st.form_submit_button("Submit", on_click=handle_submit)
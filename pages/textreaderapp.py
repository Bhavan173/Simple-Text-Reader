import streamlit as st
import asyncio
import edge_tts
from io import BytesIO
import VoicesGenerator

if "text" not in st.session_state:
    st.session_state.text = ""
if "gomain" not in st.session_state:
    st.session_state.gomain = True


    
def handle_submit():
    if not st.session_state.form_text_input:
        st.warning("Enter text!")
        return
    st.session_state.text = st.session_state.form_text_input
    with st.spinner("Please wait..."):
        st.session_state.buffer = asyncio.run(VoicesGenerator.speech(st.session_state.text.strip(),st.session_state.voice))
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
    voices = ['William', 'Neerja', 'Ava', 'Christopher', 'Maisie']
    with st.form(key="textdata"):
      
        st.text_input(
            "Paste Text below", 
            placeholder="Once upon a time..", 
            key="form_text_input"
        )
        cols = st.columns(2)
        with cols[0]:
            st.selectbox("Select service",['Text to Speech','AI Summary'])
        with cols[1]:
            st.selectbox("Voices",voices,key = "voice")
        st.form_submit_button("Submit", on_click=handle_submit)
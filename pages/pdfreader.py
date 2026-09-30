import streamlit as st
import fitz
import edge_tts
from io import BytesIO
import asyncio
import VoicesGenerator

st.title("Text Assistant")
st.header("Effortless text to speech")
st.subheader("Listen to your PDFs")


if "gomain" not in st.session_state:
    st.session_state.gomain = True




def upload():
    st.session_state.gomain = False
    pdf_bytes = st.session_state.file.read()
    doc = fitz.open(stream=pdf_bytes,filetype="pdf")

    text = ''
    for page in doc:
        blocks = page.get_text("blocks")
        for block in blocks:
            text += block[4] + "\n\n"
    st.session_state.pdfdata = text

    with st.spinner("Generating Speech..."):
        st.session_state.audio = asyncio.run(VoicesGenerator.speech(st.session_state.pdfdata,st.session_state.voice))

def goback():
    st.session_state.gomain = True



if st.session_state.gomain:

    voices = ['William', 'Neerja', 'Ava', 'Christopher', 'Maisie']
    
    with st.form(key = "Filedata"):
        st.file_uploader("Upload Pdf file with text...",key="file",type=["pdf"])
        cols = st.columns(2)
        with cols[0]:
            st.selectbox("Select service",['Text To Speech','AI Summary'])
        with cols[1]:
            st.selectbox("Voices",voices,key = "voice")
        st.form_submit_button("Upload",on_click=upload)

else:
    st.audio(st.session_state.audio.read(),format="audio/mp3")
    st.write(st.session_state.pdfdata)
    back = st.button("Back",on_click=goback)

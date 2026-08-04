import streamlit as st
import fitz
import edge_tts
from io import BytesIO
import asyncio


st.title("Text Assistant")
st.header("Effortless text to speech")
st.subheader("Listen to your PDFs")


if "gomain" not in st.session_state:
    st.session_state.gomain = True

    
async def speech(text,voice):
    unwanted_symbols = "***>"
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.translate(str.maketrans('', '', unwanted_symbols))

    # output = "Test.mp3"
    audio_buffer = BytesIO()

    print(f"Generating speech with {voice}")
    comm = edge_tts.Communicate(text,voice = voice)
    # await(comm.save(output))
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            audio_buffer.write(chunk['data'])
    audio_buffer.seek(0)
    return audio_buffer


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
        st.session_state.audio = asyncio.run(speech(st.session_state.pdfdata,st.session_state.voice))

def goback():
    st.session_state.gomain = True



if st.session_state.gomain:
    async def voices():
            voices = await edge_tts.list_voices()
            listvoices = [v['ShortName'] for v in voices if v['Locale'].startswith("en-")]
            return listvoices
    voices = asyncio.run(voices())
    
    with st.form(key = "Filedata"):
        st.file_uploader("Upload Pdf file with text...",key="file",type=["pdf"])
        st.selectbox("Select Voice",voices,key = "voice")
        st.form_submit_button("Upload",on_click=upload)

else:
    st.audio(st.session_state.audio.read(),format="audio/mp3")
    st.write(st.session_state.pdfdata)
    back = st.button("Back",on_click=goback)

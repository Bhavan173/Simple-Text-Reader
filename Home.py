import streamlit as st
st.set_page_config(page_title="EchoRead", page_icon = "🎧",layout="wide",menu_items={"About":"A Helpful text to speech app powered by AI - By Bhavan"})

reader_app = st.Page("pages/textreaderapp.py", title="Text Reader Assistant", icon="🎙️")
pdfreader = st.Page("pages/pdfreader.py", title="Pdf Reader and Summariser", icon="🎧")

pg = st.navigation([reader_app, pdfreader])
pg.run()




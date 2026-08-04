import streamlit as st
st.set_page_config(page_title="My App", page_icon="❤️")

reader_app = st.Page("pages/textreaderapp.py", title="Text Reader Assistant", icon="🎙️")
pdfreader = st.Page("pages/pdfreader.py", title="Pdf Reader and Summariser", icon="🎧")

pg = st.navigation([reader_app, pdfreader])
pg.run()




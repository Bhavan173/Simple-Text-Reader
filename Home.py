import streamlit as st
st.set_page_config(page_title="My App", page_icon="❤️")

reader_app = st.Page("pages/textreaderapp.py", title="Text Reader Assistant", icon="🎙️", default=True)

pg = st.navigation([reader_app])

with st.sidebar:
    st.title("⚙️ Settings")
    st.write("Sidebar content above navigation!")

pg.run()
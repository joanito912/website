import streamlit as st
import os

with open('./pages/blog/school_agenda.md','r') as f:
  content = f.read()
f.close()
st.markdown(content)

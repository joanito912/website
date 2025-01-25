import streamlit as st
import os

st.title("My blog page")

with open('./pages/blog/article.md','r') as f:
  content = f.read()
f.close()
st.markdown(content)

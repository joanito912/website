import streamlit as st
import os

files = os.listdir('./pages/blog')

for each_file in files:
    with st.container(border=True):
        with open('./pages/blog/' + each_file,'r') as f:
          content = f.read()
        f.close()
        st.markdown(content)

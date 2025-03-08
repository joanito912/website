import streamlit as st

st.set_page_config(layout='wide')

leftcolumn,rightcolumn = st.columns(2)

with leftcolumn:
    pass
    with st.container(border=True):
        st.write("Check-out items:")

    with st.container(border=True):
        st.write("Total:")

    with st.container(border=True):
        st.write("Payment:")

    with st.container(border=True):
        st.write("Return:")

with rightcolumn:
    pass
    with st.container(border=True):
        st.write("Right")

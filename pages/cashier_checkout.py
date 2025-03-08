import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')

dummy_data = {'description':['blueband','bread','egg'],
              'price':[12000,18000,15000],
              'quantity':[1,2,3]}

dummy_data['amount'] = dummy_data['price'] * dummy_data['quantity']

leftcolumn,rightcolumn = st.columns(2)

with leftcolumn:
    pass
    with st.container(border=True):
        st.write("Check-out items:")
        st.dataframe(dummy_data)
        

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

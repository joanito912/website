import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')

dummy_data = {'description':['blueband','bread','egg'],
              'price':[12000,18000,15000],
              'quantity':[1,2,3]}

df = pd.DataFrame(dummy_data)
df['amount'] = df['price'] * df['quantity']

leftcolumn,rightcolumn = st.columns(2)

with leftcolumn:
    pass
    with st.container(border=True):
        st.write("Check-out items:")
        st.dataframe(df)
        
    with st.container(border=True):
        st.write("Total:")
        total_amount = df['amount'].sum()
        st.write(f'{total_amount}')

    with st.container(border=True):
        st.write("Payment:")
        payment_received = st.number_input("Enter payment amount",min_value=0,step=1)
        st.write(f'{payment_received}')
        
    with st.container(border=True):
        st.write("Return:")
        return_amount = payment_recevied - total_amount

with rightcolumn:
    pass
    with st.container(border=True):
        st.write("Right")

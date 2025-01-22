import streamlit as st
import pandas as pd

data = pd.read_excel('./pages/source.xlsx')
st.dataframe(data)

#develop search criteria
criteria1 = data['category'] == 'non food'
criteria2 = data['store_name'] == 'Alfamart'

#to apply the criteria
st.dataframe(data[criteria1])
st.dataframe(data[criteria2])

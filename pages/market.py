import streamlit as st
import pandas as pd

data = pd.read_excel('./pages/source.xlsx')
st.dataframe(data)

#develop search criteria
criteria1 = data['category'] == 'non food'
criteria2 = data['store_name'] == 'Alfamart'
criteria3 = (criteria1) & (criteria2)
criteria4 = data['price'] >= 30000

#to apply the criteria
st.dataframe(data[criteria1])
st.dataframe(data[criteria2])
st.dataframe(data[criteria3])
st.dataframe(data[criteria4])

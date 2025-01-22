import streamlit as st
import pandas as pd

data = pd.read_excel('./pages/source.xlsx')
st.dataframe(data)

category_values = data['category'].unique()
selected_category = st.selectbox("Select Category",options=category_values)

#develop search criteria
criteria1 = data['category'] == selected_category
criteria2 = data['store_name'] == 'Alfamart'
criteria3 = (criteria1) & (criteria2)
criteria4 = data['price'] >= 10000
criteria5 = data['price'] <= 30000
criteria6 = (criteria4) & (criteria5)

#to apply the criteria
st.dataframe(data[criteria1])
st.dataframe(data[criteria2])
st.dataframe(data[criteria3])
st.dataframe(data[criteria4])
st.dataframe(data[criteria5])
st.dataframe(data[criteria6])

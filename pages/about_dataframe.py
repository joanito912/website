import pandas as pd
import streamlit as st

data = pd.read_excel('./pages/source.xlsx')

criteria1 = data['category'] == 'non food'
criteria2 = data['store_name'] == 'Alfamart'
criteria3 = data['price'] > 12000
criteria4 = (data['price'] >= 12000) & (data['price'] <= 40000)
criteria5 = (criteria1) & (criteria2) & (criteria4)

#print(data[criteria5])
print(data[criteria2].sort_values('price',ascending=True))
st.dataframe(data)

import streamlit as st
import pandas as pd

data = pd.read_excel('./pages/source.xlsx')

st.dataframe(data)

criteria1 = data['category'] == 'food'

st.dataframe(data[criteria1])

import streamlit as st
import pandas as pd

data = pd.read_excel('source.xlsx')

st.dataframe(data)

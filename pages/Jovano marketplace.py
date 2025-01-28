import streamlit as st
import pandas as pd


df = pd.read_excel('./pages/source.xlsx')

with st.container(border=True):
    col1,col2,col3 = st.columns(3)
    
    with col1:
        selected_category = st.selectbox("Choose category",
                                         options=df['category'].unique())

    with col2:
        selected_name = st.selectbox("Choose name",
                                         options=df['name'].unique())

    with col3:
        selected_store = st.selectbox("Choose store",
                                         options=df['store_name'].unique())

#create df subset based on certain condition
df = df[df['category'] == selected_category ]
# df = df[df['name'] == selected_name ]
# df = df[df['store_name'] == selected_store ]

for i in range(len(df)):
    record = df.iloc[i]
    st.image(f"{record['picture']}",width=250)


st.dataframe(df)





import streamlit as st
import pandas as pd


df = pd.read_excel('./pages/source.xlsx')

with st.container(border=True):
    col1,col2,col3 = st.columns(3)
    
    with col1:
        selected_category = st.multiselect("Choose category",
                                           options=df['category'].unique(),
                                           default=df['category'].unique())

    with col2:
        selected_name = st.multiselect("Choose product name",
                                       options=df['name'].unique(),
                                       default=df['name'].unique())

    with col3:
        selected_store = st.multiselect("Choose store",
                                         options=df['store_name'].unique(),
                                         default=df['store_name'].unique())

#create df subset based on certain condition
df = df[df['category'].isin(selected_category)]
df = df[df['name'].isin(selected_name)]
df = df[df['store_name'].isin(selected_store)]

num_of_columns = st.number_input("How many columns:",value = 4,step=1) # create variable to set the column
columns = st.columns(num_of_columns) # create the column
data_length = len(df)
#num_of_rows = int(data_length / num_of_columns) + 1

for i in range(data_length):
    for r in range(num_of_columns):
        if i%num_of_columns == r:
            col = columns[r]

            with col:
                with st.container(border=True):
                    record = df.iloc[i]
                    st.image(f"{record['picture']}",width=250)
                    st.write(f"{record['name']}")
                    st.write(f"{record['price']}")
                    if st.button("Add to Cart",key=f'cart{i}'):
                        st.write("Added to cart")
                    if st.button("Buy",key=f'buy{i}'):
                        st.write("Thank you")
    





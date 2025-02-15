import pandas as pd
import streamlit as st

data = pd.read_excel('./pages/source.xlsx')
unique_category = data['category'].unique()
unique_storename = data['store_name'].unique()
minimum_price = data['price'].min()
maximum_price = data['price'].max()

selected_category = st.multiselect("Select Category",options=unique_category,default=unique_category)
selected_store = st.multiselect("Select Store",options=unique_storename,default=unique_storename)
price_point = st.slider("Price",min_value=minimum_price,max_value=maximum_price,value=maximum_price)

criteria1 = data['category'].isin(selected_category) 
criteria2 = data['store_name'].isin(selected_store)
criteria3 = data['price'] <= price_point

join_criteria =  (criteria1) & (criteria2) & (criteria3)

with st.container(border=True):
  data = data[join_criteria]

  product_picture = data.iloc[0]['picture']
  st.write(product_picture)
  st.image(product_picture)

  
  st.dataframe(data,use_container_width=True)








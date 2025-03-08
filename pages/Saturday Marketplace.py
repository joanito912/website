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
  data_count = len(data)
  
  for i in range(data_count):
    product_picture = data.iloc[i]['picture']
    st.image(product_picture,width = 240)
    
    btnc1,btnc2 = st.columns(2)
    with st.container():
        with btnc1:
            if st.button("Buy now",key=str(i)):
                st.write("OK Thank you")
        with btnc2:
            if st.button("Add to cart",key=str(i)+"a"):
                st.write("Added to Cart")
    
    
  st.dataframe(data,use_container_width=True)








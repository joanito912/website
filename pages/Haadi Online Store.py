import streamlit as st
import pandas as pd

st.title("Online Groceries")
data = pd.read_excel('./pages/source.xlsx')
# st.dataframe(data)
column1,column2,column3 = st.columns(3)

with column1:
  category_values = data['category'].unique()
  selected_category = st.multiselect("Select Category",options=category_values,default=category_values)

with column2:
  store_values = data['store_name'].unique()
  selected_store = st.multiselect("Select Store",options=store_values,default=store_values)

with column3:
  minimum_price = data['price'].min() #lowest price
  maximum_price = data['price'].max() #highest price
  price_range = st.slider("Price range",min_value=minimum_price,max_value=maximum_price)

# develop search criteria
criteria1 = data['category'].isin(selected_category)
criteria2 = data['store_name'].isin(selected_store)
criteria3 = data['price'] <= price_range

join_criteria = (criteria1) & (criteria2) & (criteria3)

ncolumns = st.number_input("Column Configuration",min_value = 1, value=4,step=1)
columns = st.columns(ncolumns)

data_length = len(data[join_criteria]) #determine the length of a dataframe

for i in range(data_length): # i value starts from 0, 1, ... end of the dataframe
    for c in range(ncolumns): #c value starts from 0, 1, 2, 3
      if i%ncolumns == c:
        col = columns[c]
        with col:
            with st.container(border=True):
              st.image(data.iloc[i]['picture'])
              st.write(data.iloc[i]['name'])
              st.write(data.iloc[i]['price'])
              st.write(data.iloc[i]['store_name'])
              if st.button("Add to Cart", key= str(i)):
                st.write("Items added in cart")
              if st.button("Buy Now", key= "a"+str(i)):
                st.write("Items added in cart")

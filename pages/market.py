import streamlit as st
import pandas as pd

data = pd.read_excel('./pages/source.xlsx')
# st.dataframe(data)

category_values = data['category'].unique()
selected_category = st.multiselect("Select Category",options=category_values,default=category_values)

store_values = data['store_name'].unique()
selected_store = st.multiselect("Select Store",options=store_values,default=store_values)

minimum_price = data['price'].min() #lowest price
maximum_price = data['price'].max() #highest price

price_range = st.slider("Price range",min_value=minimum_price,max_value=maximum_price)

# develop search criteria
criteria1 = data['category'].isin(selected_category)
criteria2 = data['store_name'].isin(selected_store)
criteria3 = data['price'] <= price_range

join_criteria = (criteria1) & (criteria2) & (criteria3)

#display the picture
columns = st.columns(2)

with columns[0]:
  with st.container(border=True):
    st.image('./images/sabun_cuci_piring.jpeg')

with columns[1]:
  with st.container(border=True):
    st.image('./images/margarin_filma.jpeg')



# to apply the criteria
st.dataframe(data[join_criteria])

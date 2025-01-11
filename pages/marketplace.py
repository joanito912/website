import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')

@st.cache_data
def get_data():
    data = pd.read_excel('./pages/dataset_marketplace.xlsx')
    return data

data = get_data()

stores = data['store'].unique()
category = sorted(list(data['category'].unique()),reverse=False)
product = sorted(list(data['product'].unique()),reverse=False)

with st.container(border=True):
    st.write("Filters")
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        filter_store = st.selectbox("Filter Store",options=stores,index=None)
    with col2:
        filter_category = st.selectbox("Filter Category",options=category, index=None)
    with col3:
        filter_product = st.selectbox("Filter Product",options=product,index=None)

    if filter_category is None:
        min_price=data['price'].min()
        max_price=data['price'].max()
    else:
        min_price = data[data['category'] == filter_category]['price'].min()
        max_price = data[data['category'] == filter_category]['price'].max()
    with col4:   
        filter_price = st.slider("Price Filter",
                                min_value=min_price,
                                max_value=max_price,
                                value=max_price)

def filter_data(data):
    filtered_data = data.copy()

    if filter_store:
        filtered_data = filtered_data[filtered_data['store'] == filter_store]
    if filter_category:
        filtered_data = filtered_data[filtered_data['category'] == filter_category]
    if filter_product:
        filtered_data = filtered_data[filtered_data['product'] == filter_product]
    if filter_price:
        filtered_data = filtered_data[filtered_data['price'] <= filter_price]
        filtered_data = filtered_data.sort_values(by='price')

    return filtered_data

filtered_data = filter_data(data)

def grid_layout(cols, rows, filtered_data):
    st.header("🏪 Welcome to our Marketplace")
    st.write(f"There are {len(filtered_data)} products listed")
    for nr in range(rows):
        with st.container():
            columns = st.columns(cols)
            for nc,c in enumerate(columns):
                with c:
                    with st.container(border=True):
                        row_data = filtered_data.iloc[nr * cols + nc]
                        st.image(f"./images/{row_data['picture']}")
                        st.write(f"{row_data['product']}")
                        st.write(f"{row_data['description']}")
                        st.write(f"**Store:** {row_data['store']}")
                        st.write(f"**Price:** {row_data['price']}")
                        if st.button("🛒Cart",key=f"btncart{nr * cols + nc}"):
                            st.write("Added to Cart")
                        if st.button("💲Buy",key=f"btnbuy{nr * cols + nc}"):
                            st.write("Thank you")
cols = 5
rows = len(filtered_data) // cols

grid_layout(cols, len(filtered_data) // cols, filtered_data)
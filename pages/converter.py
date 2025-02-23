import streamlit as st

conversion_factors = {
  'distance':{'mm':1,
              'cm':0.1,
              'm' :0.01},
  'weight':None,
  'time':None
  }
col1,col2,col3,col4,col5 = st.columns(5)

with col1:
#category selection
    category_list = list(conversion_factors.keys())
    category = st.radio("Select category",options=category_list)

with col3:
    base_unit_list = list(conversion_factors[category].keys())
    base_unit = st.radio("From:",options=base_unit_list)

with col4:
    target_unit_list = list(conversion_factors[category].keys())
    target_unit = st.radio("To:",options=target_unit_list)


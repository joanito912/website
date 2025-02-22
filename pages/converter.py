import streamlit as st

conversion_factors = {
  'distance':{'mm':1,
              'cm':0.1,
              'm' :0.01},
  'weight':None,
  'time':None
  }

#category selection
category_list = list(conversion_factor.keys())
category = st.radio("Select category",options=category_list)




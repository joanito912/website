import streamlit as st

conversion_factors = {
  'distance':{'mm':1,
              'cm':0.1,
              'm' :0.01},
  'weight':None,
  'time':None
  }

#category selection
category_list = list(conversion_factors.keys())
category = st.radio("Select category",options=category_list)


base_unit_list = list(conversion_factors[category].keys())
base_unit = st.radio("From:",options=base_unit_list)


target_unit_list = list(conversion_factors[category].keys())
target_unit = st.radio("To:",options=target_unit_list)


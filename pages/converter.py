import streamlit as st

conversion_factors = {
  'distance':{'mm':1,
              'cm':0.1,
              'm' :0.01},
  'weight':pass,
  'time':pass
  }

#category selection
category = st.radio("Select category",options=conversion_factor.keys())




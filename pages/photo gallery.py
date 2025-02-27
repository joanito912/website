import streamlit as st
import os

folder = os.listdir('images') #return the list of image/picture stored in "images" folder
length_of_images = len(folder) #return an interger of how many images are in the folder

ncolumns = st.number_input("Column Configuration",min_value = 1, value = 4,step = 1)
columns = st.columns(ncolumns)

for i in range(length_of_images):
  for c in range(ncolumns):
    if i%ncolumns == c:
      col = columns[c]  
      with col:
        with st.container(border=True):
          st.image(r'./images/'+ folder[i])

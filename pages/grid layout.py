import streamlit as st

ncolumn = 4

columns = st.columns(ncolumn)

for i in range(ncolumn):
    if i%ncolumn == 0:
        col = column[0]
    if i%ncolumn == 1:
        col = column[1]
    if i%ncolumn == 2:
        col = column[2]  
    if i%ncolumn == 3:
        col = column[3]

    with col:
        with st.container(border=True):
            st.write("Hello")

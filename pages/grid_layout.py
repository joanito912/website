import streamlit as st

total_cols = 5
total_rows = 5

for nr in range(total_rows):
    with st.container(border=True):
        columns = st.columns(total_cols)
        for nc, column in enumerate(columns):
            with column:
                st.write(f"container {nr}, column {nc}")

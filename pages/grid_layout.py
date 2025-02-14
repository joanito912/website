import streamlit as st

total_cols = st.number_input("Columns",step=1)
total_rows = st.number_input("Rows",step=1)

for nr in range(total_rows):
    with st.container(border=True):
        columns = st.columns(total_cols)
        for nc, column in enumerate(columns):
            with column:
                with st.container(border=True):
                    st.write(f"container {nr}, column {nc}")

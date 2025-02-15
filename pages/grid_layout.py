import streamlit as st

st.markdown('### Two methods of grid you may choose, the first method on left, and second on the right column.')

col1,col2 = st.columns(2)

with col1:
    total_cols = st.number_input("Columns",value=3,step=1)
    total_rows = st.number_input("Rows",value=3,step=1)

    for nr in range(total_rows):
        with st.container(border=True):
            columns = st.columns(total_cols)
            for nc, column in enumerate(columns):
                with column:
                    with st.container(border=True):
                        st.write(f"container {nr}, column {nc}")

with col2:
    data_length = st.number_input("Columns",value=16, step=1)
    total_columns = 4

    columns = st.columns(total_columns)

    for i in range(total_columns):
        if i%total_columns == 0:
            column = columns[i]
            
            with column:
                with st.container(border=True):
                    st.write("Hello")
            
        
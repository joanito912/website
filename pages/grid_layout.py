import streamlit as st
st.set_page_config(layout='wide')

st.markdown('### Simple Grid Method')

col1,col2 = st.columns(2)

with col1:
    st.code('''

            data_length = st.number_input("Data Length",value=16, step=1)
            total_column = st.number_input("Total Columns",value=3,step=1)

            columns = st.columns(total_column)

            for i in range(data_length):
                for r in range(total_column):
                    if i%total_column == r:
                        column = columns[r]
                    
                        with column:
                            with st.container(border=True):
                                st.write(i+1))
            ''')

with col2:
    data_length = st.number_input("Data Length",value=16, step=1)
    total_column = st.number_input("Total Columns",value=3,step=1)

    columns = st.columns(total_column)

    for i in range(data_length):
        for r in range(total_column):
            if i%total_column == r:
                column = columns[r]
            
                with column:
                    with st.container(border=True):
                        st.write(i+1)
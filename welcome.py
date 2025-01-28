import streamlit as st

st.header("This website is written with 100% Python codes")
st.write("Click the button for fun surprise")
st.markdown("""
            <style>
                body {
                    background-color: #00d4ff;
                }
            </style>
            """, unsafe_allow_html=True)

if st.button("Snowflake"):
    st.snow()

if st.button("Balloon"):
    st.balloons()
    
st.write("Click the sidebar to find webapp we could make")

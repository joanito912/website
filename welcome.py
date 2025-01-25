import streamlit as st

st.header("This website is written with 100% Python codes")
st.write("Click the button for fun surprise")

if st.button("Snowflake"):
    st.snow()

if st.button("Balloon"):
    st.balloons()
    
st.write("Click the sidebar to find webapp we could make")

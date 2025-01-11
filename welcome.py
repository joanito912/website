import streamlit as st

st.title("Hello This is Andi's Brand New Website")
st.header("Written with 100% Python codes")
st.write("Click the button for fun surprise")

if st.button("Snowflake"):
    st.snow()

if st.button("Balloon"):
    st.balloons()
    
st.write("I'll put something great here, so stay tuned")
st.write("Bye)

with st.sidebar("Applications"):
    st.write("Choose App")

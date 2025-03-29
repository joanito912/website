import streamlit as st

st.header("Welcome to Colab Coding WebApp")
st.write("Choose the app on the side bar")
st.write("Thank you hope you enjoy it")

st.write("Security: uploaded data is not stored in github repository")

pages = {
    "Projects" : [
        st.Page("01_Unit Converter.py",title = "Converter"),
        st.Page("02_Online Marketplace.py",title = "Online Store"),
        st.Page("03_Cashier Webapp.py",title = "Cashier"),
        st.Page("04_Triangle Calculator.py",title = "Triangle")
    ],
    "Tools" : [
        st.Page("05_PDF Rotator.py",title="Rotate PDF"),
        st.Page("06_Inventory Simulation.py",title="Inventory Simulation"),
        st.Page("07_Batch Inventory Simulation.py",title="Batch Inventory Simulation"),
        st.Page("09_Led Matrix Simulation.py",title="Led Matrix Simulation")
    ]
}

import streamlit as st
# st.set_page_config(layout='wide')
st.info("Welcome to Colab Coding WebApp, choose the app on the side bar. Hope you find it useful. Uploaded data is not stored in github repository")

pages = {
    "Projects" : [
        st.Page("./pages/01_Unit Converter.py",title = "Converter",icon="📐"),
        st.Page("./pages/02_Online Marketplace.py",title = "Online Store",icon=":material/local_mall:"),
        st.Page("./pages/03_Cashier Webapp.py",title = "Cashier",icon=":material/payments:"),
        st.Page("./pages/04_Triangle Calculator.py",title = "Triangle",icon=":material/change_history:")
    ],
    "Tools" : [
        st.Page("./pages/05_PDF Rotator.py",title="Rotate PDF"),
        st.Page("./pages/06_Inventory Simulation.py",title="Inventory Simulation"),
        st.Page("./pages/07_Batch Inventory Simulation.py",title="Batch Inventory Simulation"),
        st.Page("./pages/09_Led Matrix Simulation.py",title="Led Matrix Simulation")
    ]
}

pg = st.navigation(pages)
pg.run()

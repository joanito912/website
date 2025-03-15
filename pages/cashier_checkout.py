import streamlit as st
import pandas as pd
import datetime

st.set_page_config(layout='wide')

dummy_data = {'description':['blueband','bread','egg'],
              'price':[12000,18000,15000],
              'quantity':[1,2,3]}

df = pd.DataFrame(dummy_data)
df['amount'] = df['price'] * df['quantity']

def printreceipt():
    receipt_text_width = 24

    current_time = datetime.datetime.now() #-> the output is tuple e.g. (2025,02,15,6,8,2,54,543)
    current_time_str = current_time.strftime("%d.%m.%Y %H:%M:%S") #https://strftime.org/
    
    content = f'My Online Shop\n'
    content += f'Purchase Receipt\n'
    content += f'{current_time_str}\n'
    content += f'------------------------\n'
    
    for i in range(len(df)):
        quantity = df.iloc[i]['quantity']
        description = df.iloc[i]['description']
        amount = df.iloc[i]['amount']
        
        qty_desc = f'{quantity}x {description}'
        amount = f'{amount}'
        
        white_space = " " * (receipt_text_width - (len(qty_desc) + len(amount))) 
        
        content += f'{qty_desc}{white_space}{amount}\n'

    content += f'------------------------\n'
    content += f'Total  : {total_amount}\n'
    content += f'Payment: {payment_received}\n'
    content += f'Return : {return_amount}\n'
    content += f'------------------------\n'
    content += f'Thank you for shopping'
    with rightcolumn:
        st.code(content)




leftcolumn,rightcolumn = st.columns(2)

with leftcolumn:
    pass
    with st.container(border=True):
        st.write("Check-out items:")
        st.dataframe(df)
        
    with st.container(border=True):
        st.write("Total:")
        total_amount = df['amount'].sum()
        st.write(f'{total_amount}')

    with st.container(border=True):
        st.write("Payment:")
        payment_received = st.number_input("Enter payment amount",min_value=0,step=1)
        
    with st.container(border=True):
        st.write("Return:")
        return_amount = payment_received - total_amount
        st.write(f'{return_amount}')
        
    with st.container():
        if st.button("Print receipt"):
            if return_amount >= 0:
                printreceipt()
            else:
                st.warning("Payment must be more or equal than the total purchase") 
        
        
        

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta, date
from io import BytesIO

# Simulate inventory function (unchanged)
def simulate_ddmrp_inventory(rop, max_qty, critical_level, moq, 
                           delivery_lead_time, qty_per_package, monthly_usage_avg, 
                           beginning_inventory, inventory_value, sim_days, start_date=datetime.now()):
    daily_avg_use = monthly_usage_avg / 30
    inventory = beginning_inventory
    dates = [start_date]
    inventory_levels = [inventory]
    pending_orders = []  # (delivery_date, quantity, order_day)
    order_annotations = []

    daily_consumption = np.random.uniform(daily_avg_use * 0.5, 
                                        daily_avg_use * 1.5, 
                                        sim_days)

    for day in range(sim_days):
        current_date = start_date + timedelta(days=day)
        dates.append(current_date)
        inventory = max(0, inventory - daily_consumption[day])
        
        # Check for delivered orders
        for delivery_date, qty, order_date in pending_orders[:]:
            if current_date >= delivery_date:
                inventory += qty
                order_amount = qty * inventory_value
                order_annotations.append({
                    'x': delivery_date,
                    'y': inventory,
                    'text': f'Order: {int(qty)}\n({order_amount:,.0f})',
                    'showarrow': True,
                    'arrowhead': 1,
                    'ax': 20,
                    'ay': -30
                })
                pending_orders.remove((delivery_date, qty, order_date))
        
        # Check if inventory falls below ROP and place order if needed
        if inventory <= rop and not any(current_date < d[0] < current_date + timedelta(days=delivery_lead_time) 
                                     for d in pending_orders):
            actual_order_qty = max(moq, 
                                 np.ceil((max_qty - inventory) / qty_per_package) * qty_per_package)
            actual_order_qty = min(actual_order_qty, max_qty - inventory)
            
            delivery_date = current_date + timedelta(days=delivery_lead_time)
            pending_orders.append((delivery_date, actual_order_qty, current_date))

        inventory_levels.append(min(inventory, max_qty))

    df = pd.DataFrame({
        'Date': dates,
        'Inventory': inventory_levels,
        'ROP': [rop] * len(dates),
        'Max_Qty': [max_qty] * len(dates),
        'Critical_Level': [critical_level] * len(dates)
    })
    
    order_dates = [d[2] for d in pending_orders]
    if len(order_dates) > 1:
        avg_cycle = np.mean([(order_dates[i+1] - order_dates[i]).days 
                           for i in range(len(order_dates)-1)])
    else:
        avg_cycle = None

    return df, avg_cycle, daily_avg_use, order_annotations

# Function to convert DataFrame to Excel bytes
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    excel_data = output.getvalue()
    return excel_data

st.subheader("Batch Inventory Simulation")

# Suggested Excel column names
excel_template_columns = [
    'Material Name',
    'Monthly Usage Average',
    'Beginning Inventory',
    'Lead Time (days)',
    'Critical Level',
    'Re-Order Point (ROP)',
    'Maximum Quantity',
    'Inventory Value per UoM',
    'Quantity per Package',
    'Minimum Order Quantity (MOQ)',
    'Simulation Days'
]

# File uploader for Excel
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is not None:
    # Read Excel file
    materials_df = pd.read_excel(uploaded_file)
    
    # Ensure Simulation Days is integer
    if 'Simulation Days' in materials_df.columns:
        materials_df['Simulation Days'] = materials_df['Simulation Days'].astype(int)
    
    # Validate required columns
    required_columns = excel_template_columns
    missing_columns = [col for col in required_columns if col not in materials_df.columns]
    if missing_columns:
        st.error(f"Excel file is missing required columns: {', '.join(missing_columns)}. Please ensure all columns are present.")
    else:
        # Display editable DataFrame in expander
        with st.expander("Preview and Edit Materials Data"):
            edited_df = st.data_editor(materials_df, num_rows="dynamic")
            materials_data = edited_df

            # Download button for edited DataFrame
            original_filename = uploaded_file.name
            base_name = original_filename.rsplit('.', 1)[0]  # Remove extension
            new_filename = f"{base_name}_edited.xlsx"
            excel_data = to_excel(edited_df)
            st.download_button(
                label="Download Edited Data as Excel",
                data=excel_data,
                file_name=new_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # Start date input
        start_date_input = st.date_input("Simulation Start Date", 
                                        value=date.today(),
                                        min_value=date.today() - timedelta(days=365),
                                        max_value=date.today() + timedelta(days=365))
        start_date = datetime.combine(start_date_input, datetime.min.time())

        # Calculate number of rows needed (2 columns fixed)
        num_materials = len(materials_data)
        num_rows = (num_materials + 1) // 2  # Ceiling division to get rows

        # Simulation and visualization in a 2-column layout
        for row_idx in range(num_rows):
            cols = st.columns(2)  # Always 2 columns
            for col_idx in range(2):
                material_idx = row_idx * 2 + col_idx
                if material_idx < num_materials:  # Check if there’s a material for this slot
                    with cols[col_idx]:
                        row = materials_data.iloc[material_idx]
                        material_name = row['Material Name']
                        monthly_usage_avg = row['Monthly Usage Average']
                        beginning_inventory = row['Beginning Inventory']
                        delivery_lead_time = row['Lead Time (days)']
                        critical_level = row['Critical Level']
                        rop = row['Re-Order Point (ROP)']
                        max_qty = row['Maximum Quantity']
                        inventory_value = row['Inventory Value per UoM']
                        qty_per_package = row['Quantity per Package']
                        moq = row['Minimum Order Quantity (MOQ)']
                        sim_days = int(row['Simulation Days'])  # Ensure integer

                        # Run simulation
                        df, avg_cycle, daily_avg_use, order_annotations = simulate_ddmrp_inventory(
                            rop, max_qty, critical_level, moq, delivery_lead_time, qty_per_package,
                            monthly_usage_avg, beginning_inventory, inventory_value, sim_days, start_date
                        )

                        # Chart with material name in title
                        fig = px.line(df, x='Date', y=['Inventory', 'ROP', 'Max_Qty', 'Critical_Level'],
                                     title=f'Inventory Simulation for {material_name} (Starting {start_date.strftime("%Y-%m-%d")})')
                        
                        # Month-end markers
                        end_date = start_date + timedelta(days=sim_days)
                        current_date = start_date.replace(day=1)
                        month_end_dates = []
                        while current_date <= end_date:
                            next_month = current_date.replace(day=28) + timedelta(days=4)
                            last_day = next_month - timedelta(days=next_month.day)
                            if last_day >= start_date and last_day <= end_date:
                                month_end_dates.append(last_day)
                            current_date = (last_day + timedelta(days=1)).replace(day=1)
                        
                        month_end_df = df[df['Date'].isin(month_end_dates)].copy()
                        fig.add_scatter(
                            x=month_end_df['Date'],
                            y=month_end_df['Inventory'],
                            mode='markers',
                            marker=dict(symbol='circle', size=10, color='grey', opacity=0.7),
                            name='Month End',
                            hovertemplate='%{x|%Y-%m-%d}<br>Inventory: %{y:.0f}'
                        )
                        
                        fig.update_layout(
                            yaxis_title="Inventory Qty",
                            legend_title="Metrics",
                            xaxis_title="Date",
                            yaxis=dict(range=[0, max(max_qty, df['Inventory'].max()) * 1.1]),
                            annotations=order_annotations
                        )
                        st.plotly_chart(fig, use_container_width=True)

                        # Interval table with material name in header
                        interval_data = []
                        current_date = start_date.replace(day=1)
                        while current_date <= end_date:
                            next_month = current_date.replace(day=28) + timedelta(days=4)
                            last_day = next_month - timedelta(days=next_month.day)
                            if last_day >= start_date and last_day <= end_date:
                                qty = df.loc[df['Date'] == last_day, 'Inventory'].iloc[0] if not df[df['Date'] == last_day].empty else 0
                                value = qty * inventory_value
                                interval_data.append({
                                    'Date': last_day.strftime('%Y-%m-%d'),
                                    'Inventory Quantity': f"{qty:,.0f}",
                                    'Inventory Value': f"{value:,.0f}"
                                })
                            current_date = (last_day + timedelta(days=1)).replace(day=1)
                        
                        interval_df = pd.DataFrame(interval_data)
                        st.write(f"Month-End Inventory for {material_name}")
                        st.table(interval_df)
else:
    st.info("Please upload an Excel file to start the simulation.")
# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# from datetime import datetime, timedelta, date
# from io import BytesIO

# # Simulate inventory function (unchanged)
# def simulate_ddmrp_inventory(rop, max_qty, critical_level, moq, 
#                            delivery_lead_time, qty_per_package, monthly_usage_avg, 
#                            beginning_inventory, inventory_value, sim_days, start_date=datetime.now()):
#     daily_avg_use = monthly_usage_avg / 30
#     inventory = beginning_inventory
#     dates = [start_date]
#     inventory_levels = [inventory]
#     pending_orders = []  # (delivery_date, quantity, order_day)
#     order_annotations = []

#     daily_consumption = np.random.uniform(daily_avg_use * 0.5, 
#                                         daily_avg_use * 1.5, 
#                                         sim_days)

#     for day in range(sim_days):
#         current_date = start_date + timedelta(days=day)
#         dates.append(current_date)
#         inventory = max(0, inventory - daily_consumption[day])
        
#         # Check for delivered orders
#         for delivery_date, qty, order_date in pending_orders[:]:
#             if current_date >= delivery_date:
#                 inventory += qty
#                 order_amount = qty * inventory_value
#                 order_annotations.append({
#                     'x': delivery_date,
#                     'y': inventory,
#                     'text': f'Order: {int(qty)}\n({order_amount:,.0f})',
#                     'showarrow': True,
#                     'arrowhead': 1,
#                     'ax': 20,
#                     'ay': -30
#                 })
#                 pending_orders.remove((delivery_date, qty, order_date))
        
#         # Check if inventory falls below ROP and place order if needed
#         if inventory <= rop and not any(current_date < d[0] < current_date + timedelta(days=delivery_lead_time) 
#                                      for d in pending_orders):
#             actual_order_qty = max(moq, 
#                                  np.ceil((max_qty - inventory) / qty_per_package) * qty_per_package)
#             actual_order_qty = min(actual_order_qty, max_qty - inventory)
            
#             delivery_date = current_date + timedelta(days=delivery_lead_time)
#             pending_orders.append((delivery_date, actual_order_qty, current_date))

#         inventory_levels.append(min(inventory, max_qty))

#     df = pd.DataFrame({
#         'Date': dates,
#         'Inventory': inventory_levels,
#         'ROP': [rop] * len(dates),
#         'Max_Qty': [max_qty] * len(dates),
#         'Critical_Level': [critical_level] * len(dates)
#     })
    
#     order_dates = [d[2] for d in pending_orders]
#     if len(order_dates) > 1:
#         avg_cycle = np.mean([(order_dates[i+1] - order_dates[i]).days 
#                            for i in range(len(order_dates)-1)])
#     else:
#         avg_cycle = None

#     return df, avg_cycle, daily_avg_use, order_annotations

# # Function to convert DataFrame to Excel bytes
# def to_excel(df):
#     output = BytesIO()
#     with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
#         df.to_excel(writer, index=False, sheet_name='Sheet1')
#     excel_data = output.getvalue()
#     return excel_data

# st.subheader("Batch Inventory Simulation")

# # Suggested Excel column names
# excel_template_columns = [
#     'Material Name',
#     'Monthly Usage Average',
#     'Beginning Inventory',
#     'Lead Time (days)',
#     'Critical Level',
#     'Re-Order Point (ROP)',
#     'Maximum Quantity',
#     'Inventory Value per UoM',
#     'Quantity per Package',
#     'Minimum Order Quantity (MOQ)',
#     'Simulation Days'
# ]

# # File uploader for Excel
# uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

# if uploaded_file is not None:
#     # Read Excel file
#     materials_df = pd.read_excel(uploaded_file)
    
#     # Ensure Simulation Days is integer
#     if 'Simulation Days' in materials_df.columns:
#         materials_df['Simulation Days'] = materials_df['Simulation Days'].astype(int)
    
#     # Validate required columns
#     required_columns = excel_template_columns
#     missing_columns = [col for col in required_columns if col not in materials_df.columns]
#     if missing_columns:
#         st.error(f"Excel file is missing required columns: {', '.join(missing_columns)}. Please ensure all columns are present.")
#     else:
#         # Display editable DataFrame in expander
#         with st.expander("Preview and Edit Materials Data"):
#             edited_df = st.data_editor(materials_df, num_rows="dynamic")
#             materials_data = edited_df

#             # Download button for edited DataFrame
#             original_filename = uploaded_file.name
#             base_name = original_filename.rsplit('.', 1)[0]  # Remove extension
#             new_filename = f"{base_name}_edited.xlsx"
#             excel_data = to_excel(edited_df)
#             st.download_button(
#                 label="Download Edited Data as Excel",
#                 data=excel_data,
#                 file_name=new_filename,
#                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#             )

#         # Start date input
#         start_date_input = st.date_input("Simulation Start Date", 
#                                         value=date.today(),
#                                         min_value=date.today() - timedelta(days=365),
#                                         max_value=date.today() + timedelta(days=365))
#         start_date = datetime.combine(start_date_input, datetime.min.time())

#         # Create columns for each material
#         num_materials = len(materials_data)
#         cols = st.columns(num_materials)  # Create as many columns as there are materials

#         # Simulation and visualization for each material in its own column
#         for idx, (index, row) in enumerate(materials_data.iterrows()):
#             with cols[idx]:  # Use the corresponding column for this material
#                 material_name = row['Material Name']
#                 monthly_usage_avg = row['Monthly Usage Average']
#                 beginning_inventory = row['Beginning Inventory']
#                 delivery_lead_time = row['Lead Time (days)']
#                 critical_level = row['Critical Level']
#                 rop = row['Re-Order Point (ROP)']
#                 max_qty = row['Maximum Quantity']
#                 inventory_value = row['Inventory Value per UoM']
#                 qty_per_package = row['Quantity per Package']
#                 moq = row['Minimum Order Quantity (MOQ)']
#                 sim_days = int(row['Simulation Days'])  # Ensure integer

#                 # Run simulation
#                 df, avg_cycle, daily_avg_use, order_annotations = simulate_ddmrp_inventory(
#                     rop, max_qty, critical_level, moq, delivery_lead_time, qty_per_package,
#                     monthly_usage_avg, beginning_inventory, inventory_value, sim_days, start_date
#                 )

#                 # Chart with material name in title
#                 fig = px.line(df, x='Date', y=['Inventory', 'ROP', 'Max_Qty', 'Critical_Level'],
#                              title=f'Inventory Simulation for {material_name} (Starting {start_date.strftime("%Y-%m-%d")})')
                
#                 # Month-end markers
#                 end_date = start_date + timedelta(days=sim_days)
#                 current_date = start_date.replace(day=1)
#                 month_end_dates = []
#                 while current_date <= end_date:
#                     next_month = current_date.replace(day=28) + timedelta(days=4)
#                     last_day = next_month - timedelta(days=next_month.day)
#                     if last_day >= start_date and last_day <= end_date:
#                         month_end_dates.append(last_day)
#                     current_date = (last_day + timedelta(days=1)).replace(day=1)
                
#                 month_end_df = df[df['Date'].isin(month_end_dates)].copy()
#                 fig.add_scatter(
#                     x=month_end_df['Date'],
#                     y=month_end_df['Inventory'],
#                     mode='markers',
#                     marker=dict(symbol='circle', size=10, color='grey', opacity=0.7),
#                     name='Month End',
#                     hovertemplate='%{x|%Y-%m-%d}<br>Inventory: %{y:.0f}'
#                 )
                
#                 fig.update_layout(
#                     yaxis_title="Inventory Qty",
#                     legend_title="Metrics",
#                     xaxis_title="Date",
#                     yaxis=dict(range=[0, max(max_qty, df['Inventory'].max()) * 1.1]),
#                     annotations=order_annotations
#                 )
#                 st.plotly_chart(fig, use_container_width=True)

#                 # Interval table with material name in header
#                 interval_data = []
#                 current_date = start_date.replace(day=1)
#                 while current_date <= end_date:
#                     next_month = current_date.replace(day=28) + timedelta(days=4)
#                     last_day = next_month - timedelta(days=next_month.day)
#                     if last_day >= start_date and last_day <= end_date:
#                         qty = df.loc[df['Date'] == last_day, 'Inventory'].iloc[0] if not df[df['Date'] == last_day].empty else 0
#                         value = qty * inventory_value
#                         interval_data.append({
#                             'Date': last_day.strftime('%Y-%m-%d'),
#                             'Inventory Quantity': f"{qty:,.0f}",
#                             'Inventory Value': f"{value:,.0f}"
#                         })
#                     current_date = (last_day + timedelta(days=1)).replace(day=1)
                
#                 interval_df = pd.DataFrame(interval_data)
#                 st.write(f"Month-End Inventory for {material_name}")
#                 st.table(interval_df)
# else:
#     st.info("Please upload an Excel file to start the simulation.")


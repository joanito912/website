import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout='wide')

def simulate_ddmrp_inventory(rop, max_qty, critical_level, moq, 
                           delivery_lead_time, qty_per_package, monthly_usage_avg, 
                           beginning_inventory, inventory_value, sim_days=90):
    daily_avg_use = monthly_usage_avg / 30
    inventory = beginning_inventory
    day_numbers = [1]
    inventory_levels = [inventory]
    pending_orders = []  # (delivery_day, quantity, order_day)
    order_annotations = []  # For chart annotations

    daily_consumption = np.random.uniform(daily_avg_use * 0.5, 
                                        daily_avg_use * 1.5, 
                                        sim_days)

    for day in range(1, sim_days):
        day_numbers.append(day + 1)
        inventory = max(0, inventory - daily_consumption[day])
        
        # Check for delivered orders
        for delivery_day, qty, order_day in pending_orders[:]:
            if day >= delivery_day:
                inventory += qty
                order_amount = qty * inventory_value
                order_annotations.append({
                    'x': delivery_day,
                    'y': inventory,
                    'text': f'Order: {int(qty)}\n({order_amount:,.0f})',
                    'showarrow': True,
                    'arrowhead': 1,
                    'ax': 20,
                    'ay': -30
                })
                pending_orders.remove((delivery_day, qty, order_day))
        
        # Check if inventory falls below ROP and place order if needed
        if inventory <= rop and not any(day < d[0] < day + delivery_lead_time 
                                     for d in pending_orders):
            actual_order_qty = max(moq, 
                                 np.ceil((max_qty - inventory) / qty_per_package) * qty_per_package)
            actual_order_qty = min(actual_order_qty, max_qty - inventory)
            
            delivery_day = day + delivery_lead_time
            pending_orders.append((delivery_day, actual_order_qty, day))

        inventory_levels.append(min(inventory, max_qty))

    df = pd.DataFrame({
        'Day': day_numbers,
        'Inventory': inventory_levels,
        'ROP': [rop] * len(day_numbers),
        'Max_Qty': [max_qty] * len(day_numbers),
        'Critical_Level': [critical_level] * len(day_numbers)
    })
    
    order_days = [d[2] for d in pending_orders]
    if len(order_days) > 1:
        avg_cycle = np.mean([order_days[i+1] - order_days[i] 
                           for i in range(len(order_days)-1)])
    else:
        avg_cycle = None

    return df, avg_cycle, daily_avg_use, order_annotations

st.header("Inventory Simulation")

col_left, col_right = st.columns(2)

with col_left:    
    col1, col2 = st.columns(2)
    
    with col1:
        monthly_usage_avg = st.number_input("Monthly Usage Average", 
                                          min_value=10, 
                                          max_value=9000, 
                                          value=900, 
                                          step=1)
        
        daily_usage_avg = monthly_usage_avg / 30
        
        delivery_lead_time = st.number_input("PR Release - ETA Lead Time (days)", 
                                           min_value=1, 
                                           max_value=120, 
                                           value=7, 
                                           step=1)
        
        critical_default = int(daily_usage_avg * delivery_lead_time)  # Updated calculation
        if st.toggle("Run to zero"):
          critical_default = 0
        critical_level = st.number_input("Critical Level", 
                                       min_value=0, 
                                       max_value=9000, 
                                       value=critical_default, 
                                       step=1)
        
        rop_default = int((daily_usage_avg * delivery_lead_time) + critical_level)
        rop = st.number_input("Re-Order Point (ROP)", 
                            min_value=0, 
                            max_value=9000, 
                            value=rop_default, 
                            step=1)
      
        
    with col2:
        beginning_inventory_default = int(monthly_usage_avg)
        beginning_inventory = st.number_input("Inventory Quantity", 
                                            min_value=0, 
                                            max_value=9000, 
                                            value=beginning_inventory_default, 
                                            step=1)

        max_qty_default = int(monthly_usage_avg + rop)
        if st.toggle("Half Monthly Usage"):
          max_qty_default = int((0.5*monthly_usage_avg) + rop)
        max_qty = st.number_input("Maximum Quantity", 
                                min_value=rop, 
                                max_value=9000, 
                                value=max_qty_default, 
                                step=1)
        
        inventory_value = st.number_input("Material price per UoM", 
                                        min_value=0.01, 
                                        max_value=500000.00, 
                                        value=1.00, 
                                        step=0.01,
                                        format="%.2f")

        qty_per_package = st.number_input("Quantity per Package", 
                                        min_value=1, 
                                        max_value=100, 
                                        value=1, 
                                        step=1)
        moq = st.number_input("Minimum Order Quantity (MOQ)", 
                            min_value=0, 
                            max_value=500, 
                            value=qty_per_package, 
                            step=1)
        
    with col1:
      sim_days = st.number_input("Simulation Days", 
                                   min_value=30, 
                                   max_value=365, 
                                   value=90, 
                                   step=1)

# Run simulation
df, avg_cycle, daily_avg_use, order_annotations = simulate_ddmrp_inventory(
    rop, max_qty, critical_level, moq, 
    delivery_lead_time, qty_per_package, monthly_usage_avg, 
    beginning_inventory, inventory_value, sim_days
)

# Right column: Chart and Results
with col_right:    
    fig = px.line(df, x='Day', y=['Inventory', 'ROP', 'Max_Qty', 'Critical_Level'],
                 title='Inventory Simulation')
    fig.update_layout(
        yaxis_title="Inventory Qty",
        legend_title="Metrics",
        xaxis_title="Day Number",
        yaxis=dict(range=[0, max(max_qty, df['Inventory'].max()) * 1.1]),
        xaxis=dict(range=[1, sim_days]),
        annotations=order_annotations
    )
    st.plotly_chart(fig, use_container_width=True)
        
    st.write(f"Daily Average Use: {daily_avg_use:.1f} units")

with col_left:
    rop_formula = (r"\text{ROP} = (\text{Daily Usage} \times \text{Lead Time}) + \text{Critical Level} = "
                  f"({daily_usage_avg:.1f} \\times {delivery_lead_time}) + {critical_level} = {rop_default}")
    max_qty_formula = r"\text{Max Qty} = \text{Monthly Usage Avg} + \text{ROP} = " + f"{monthly_usage_avg} + {rop} = {max_qty_default}"
    critical_formula = (r"\text{Critical Level} = \text{Daily Usage} \times \text{Lead Time} = "
                      f"{daily_usage_avg:.1f} \\times {delivery_lead_time} = {critical_default}")
    order_qty_formula = r"\text{Order Qty} = \max(\text{MOQ}, \lceil\frac{\text{Max Qty} - \text{Inventory}}{\text{Qty per Package}}\rceil \times \text{Qty per Package})"

    st.latex(rop_formula)
    st.latex(max_qty_formula)
    st.latex(critical_formula)
    st.latex(order_qty_formula)


with col_right:
    interval_data = []
    for day in range(0, sim_days, 30):
        if day < len(df):
            qty = df.loc[df['Day'] == day + 1, 'Inventory'].values[0]
            value = qty * inventory_value
            interval_data.append({
                'Day': day + 1,
                'Inventory Quantity': f"{qty:,.0f}",
                'Inventory Value': f"{value:,.0f}"
            })

    interval_df = pd.DataFrame(interval_data)
    st.table(interval_df)

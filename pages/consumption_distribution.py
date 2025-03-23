import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from scipy.stats import norm

# Streamlit input widgets
daily_avg_use = st.number_input("Daily Average Use", 
                              min_value=0.1, 
                              value=1.7, 
                              step=0.1)
sim_days = st.number_input("Simulation Days", 
                          min_value=1, 
                          value=30, 
                          step=1)
percent_deviation = st.number_input("Percent Deviation", 
                                  min_value=1.0, 
                                  value=50.0, 
                                  step=1.0)
bins = st.number_input("Number of Bins", 
                      min_value=1, 
                      value=10, 
                      step=1)

# Calculate min and max bounds based on percent deviation
min_value = daily_avg_use * (1 - percent_deviation/100)
max_value = daily_avg_use * (1 + percent_deviation/100)

# Generate random daily consumption data
daily_consumption = np.random.uniform(min_value, 
                                    max_value, 
                                    sim_days)

# Create the histogram
fig, ax = plt.subplots()
# Plot histogram with density=True for normalized height
n, bins_edges, patches = ax.hist(daily_consumption, 
                                bins=bins, 
                                edgecolor='black', 
                                density=True)

# Fit and plot normal distribution curve
mu, sigma = norm.fit(daily_consumption)
x = np.linspace(min_value, max_value, 100)
y = norm.pdf(x, mu, sigma)
ax.plot(x, y, 'r-', lw=2, label='Normal Fit')

# Customize plot
ax.set_title(f'Daily Consumption Distribution (±{percent_deviation}% deviation)')
ax.set_xlabel('Consumption')
ax.set_ylabel('Density')
ax.legend()

# Display in Streamlit
st.pyplot(fig)
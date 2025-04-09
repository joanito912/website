import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Distribution fitting functions
from scipy.stats import norm, lognorm, expon, gamma, weibull_min

def find_best_distribution(data):
    distributions = [
        norm,        # Normal distribution
        lognorm,     # Log-normal distribution
        expon,       # Exponential distribution
        gamma,       # Gamma distribution
        weibull_min  # Weibull distribution
    ]
    
    best_distribution = None
    best_p_value = -1
    
    for distribution in distributions:
        try:
            # Fit distribution to data
            params = distribution.fit(data)
            # Perform Kolmogorov-Smirnov test
            statistic, p_value = stats.kstest(data, distribution.name, args=params)
            
            if p_value > best_p_value:
                best_p_value = p_value
                best_distribution = distribution
                best_params = params
                
        except:
            continue
    
    return best_distribution, best_params, best_p_value

def main():
    st.title("Distribution Analyzer")
    st.write("Upload an Excel file to analyze the distribution of your data")
    
    # File upload
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        try:
            # Read Excel file with explicit engine specification
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            
            # Display available columns
            st.write("Available columns:", df.columns.tolist())
            
            # Column selection
            selected_column = st.selectbox("Select a column to analyze", df.columns)
            
            # Get data and handle null values
            data = df[selected_column].dropna()
            # Convert to numeric, coercing errors to NaN, then drop them
            data = pd.to_numeric(data, errors='coerce').dropna()
            
            if len(data) > 0:
                # Create figure
                fig, ax = plt.subplots(figsize=(10, 6))
                
                # Plot histogram
                sns.histplot(data=data, kde=False, stat='density', ax=ax, color='skyblue', 
                           label='Histogram')
                
                # Fit and plot distribution
                best_dist, best_params, p_value = find_best_distribution(data)
                
                if best_dist:
                    # Generate points for distribution curve
                    x = np.linspace(min(data), max(data), 100)
                    dist_values = best_dist.pdf(x, *best_params)
                    ax.plot(x, dist_values, 'r-', lw=2, label=f'Best fit: {best_dist.name}')
                    
                    st.write(f"Best fitting distribution: {best_dist.name}")
                    st.write(f"P-value: {p_value:.4f}")
                    st.write("Note: Higher p-value indicates better fit (max 1.0)")
                
                # Customize plot
                ax.set_title(f'Distribution of {selected_column}')
                ax.set_xlabel(selected_column)
                ax.set_ylabel('Density')
                ax.legend()
                
                # Display plot
                st.pyplot(fig)
                
                # Display basic statistics
                st.write("Basic Statistics:")
                st.write(data.describe())
                
            else:
                st.error("No valid data in selected column")
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    
    else:
        st.info("Please upload an Excel file to begin")

if __name__ == "__main__":
    main()
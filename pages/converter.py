import streamlit as st

st.title("Unit Converter")
conversion_factor = {
                    'distance': {
                        'mm': 1,
                        'cm': 0.1,
                        'm': 0.001,
                        'km': 0.000001,
                        'inch': 0.0393701,
                        'feet': 0.00328084,
                        'yards': 0.00109361,
                        'miles': 6.2137e-7,
                        'AU': 6.68459e-12,
                        'light_year': 1.057e-16},
                    'weight': {
                        'gr': 1,
                        'kg': 0.001,
                        'mg': 1000,
                        'ton': 1e-6,
                        'pound': 0.00220462,
                        'ounce': 0.035274},
                    'speed': {
                        'm/s': 1,
                        'km/h': 3.6,
                        'miles/h': 2.23694,
                        'knot': 1.94384,
                        'light_speed': 3.33564e-9},
                    'volume':{
                        'lt': 1,
                        'ml': 1000,
                        'tbsp': 67.628,
                        'tsp': 202.884,
                        'm3': 0.001,
                        'km3': 1e-12},
                    'planet':{
                        'earth': 1,
                        'mercury': 0.056,
                        'venus': 0.866,
                        'mars': 0.151,
                        'jupiter': 1321,
                        'saturn': 763.6,
                        'uranus': 63.1,
                        'neptune': 57.7,
                        'sun': 1.4122e18},
                    'temperature': ['Celsius', 'Fahrenheit', 'Kelvin']}
def show_formula(category, base_unit=None, target_unit=None):
    if category == 'temperature' and base_unit and target_unit:
        if base_unit == 'Celsius' and target_unit == 'Fahrenheit':
            st.latex(r'\text{F} = \text{C} \times \frac{9}{5} + 32')
        elif base_unit == 'Celsius' and target_unit == 'Kelvin':
            st.latex(r'\text{K} = \text{C} + 273.15')
        elif base_unit == 'Fahrenheit' and target_unit == 'Celsius':
            st.latex(r'\text{C} = (\text{F} - 32) \times \frac{5}{9}')
        elif base_unit == 'Fahrenheit' and target_unit == 'Kelvin':
            st.latex(r'\text{K} = (\text{F} - 32) \times \frac{5}{9} + 273.15')
        elif base_unit == 'Kelvin' and target_unit == 'Celsius':
            st.latex(r'\text{C} = \text{K} - 273.15')
        elif base_unit == 'Kelvin' and target_unit == 'Fahrenheit':
            st.latex(r'\text{F} = (\text{K} - 273.15) \times \frac{9}{5} + 32')
        else:
            st.latex(r'\text{Converted Value} = \text{Input Value}')
    else:
        st.latex(r'''
        \text{Converted Value} = \frac{\text{Input Value}}{\text{Conversion Factor of Base Unit}} \times \text{Conversion Factor of Target Unit}
        ''')

def convert(input_value, category, base_unit, target_unit):
    if category == 'temperature':
        if base_unit == 'Celsius':
            if target_unit == 'Fahrenheit':
                return input_value * 9 / 5 + 32
            elif target_unit == 'Kelvin':
                return input_value + 273.15
        elif base_unit == 'Fahrenheit':
            if target_unit == 'Celsius':
                return (input_value - 32) * 5 / 9
            elif target_unit == 'Kelvin':
                return (input_value - 32) * 5 / 9 + 273.15
        elif base_unit == 'Kelvin':
            if target_unit == 'Celsius':
                return input_value - 273.15
            elif target_unit == 'Fahrenheit':
                return (input_value - 273.15) * 9 / 5 + 32
        return input_value 
    else:
        return input_value / conversion_factor[category][base_unit] * conversion_factor[category][target_unit]

with st.expander("Converter"):
    if 'result' not in st.session_state:
        st.session_state.result = 0.0
    
    with st.container():
        col0, col1, col2, col3, col4 = st.columns(5)
    
        with col0:
            category = st.radio("Category", list(conversion_factor.keys()), key="category")
    
        with col1:
            input_value = st.number_input("Input Value", min_value=0.0, step=0.1, key="input_value")
    
        with col2:
            if category == 'temperature':
                base_unit = st.radio("From", conversion_factor[category], key="base_unit")
            else:
                base_unit = st.radio("From", conversion_factor[category], key="base_unit")
    
        with col3:
            if category == 'temperature':
                target_unit = st.radio("To", conversion_factor[category], key="target_unit")
            else:
                target_unit = st.radio("To", conversion_factor[category], key="target_unit")
    
        with col4:
            st.write("Converted Value")
            if base_unit and target_unit:
                st.session_state.result = convert(input_value, category, base_unit, target_unit)
            if category == 'planet':
                st.write(f'{target_unit} volume is {st.session_state.result:#,.3f} times of {base_unit}')
            else:
                st.write(f'{st.session_state.result:#,.3f} {target_unit}')
    
    show_formula(category, base_unit, target_unit)

import streamlit as st
from forex_python.converter import CurrencyRates
from pint import UnitRegistry
import time

# Initialize unit registry
ureg = UnitRegistry()
c = CurrencyRates()

def convert_units(value, from_unit, to_unit):
    try:
        return (value * ureg(from_unit)).to(to_unit).magnitude
    except:
        return "Invalid Conversion"

def convert_currency(value, from_currency, to_currency):
    try:
        rate = c.get_rate(from_currency, to_currency)
        return value * rate
    except:
        return "Invalid Conversion"

# Animated Title
title_html = """
<style>
@keyframes flicker {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}
.title {
  color: red;
  text-shadow: 2px 2px 5px #BA0D0D ;
  font-size: 40px;
  font-weight: bold;
  text-align: center;
  animation: flicker 1s infinite;
}
.result-box {
  color: white;
  background-color: #FB1616;
  padding: 10px;
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  border-radius: 10px;
  margin-top: 20px;
}
</style>
<h1 class="title">🔥 Unit Converter 🔥</h1>
"""
st.markdown(title_html, unsafe_allow_html=True)

option = st.selectbox("Select Conversion Type", ["Length", "Weight", "Temperature", "Currency"])

value = st.number_input("Enter Value", min_value=0.0, format="%f")

if option == "Length":
    from_unit = st.selectbox("From", ["meter", "kilometer", "mile", "yard", "foot", "inch"])
    to_unit = st.selectbox("To", ["meter", "kilometer", "mile", "yard", "foot", "inch"])
    result = convert_units(value, from_unit, to_unit)

elif option == "Weight":
    from_unit = st.selectbox("From", ["gram", "kilogram", "pound", "ounce"])
    to_unit = st.selectbox("To", ["gram", "kilogram", "pound", "ounce"])
    result = convert_units(value, from_unit, to_unit)

elif option == "Temperature":
    from_unit = st.selectbox("From", ["celsius", "fahrenheit", "kelvin"])
    to_unit = st.selectbox("To", ["celsius", "fahrenheit", "kelvin"])
    
    if from_unit == "celsius" and to_unit == "fahrenheit":
        result = (value * 9/5) + 32
    elif from_unit == "fahrenheit" and to_unit == "celsius":
        result = (value - 32) * 5/9
    elif from_unit == "celsius" and to_unit == "kelvin":
        result = value + 273.15
    elif from_unit == "kelvin" and to_unit == "celsius":
        result = value - 273.15
    elif from_unit == "fahrenheit" and to_unit == "kelvin":
        result = (value - 32) * 5/9 + 273.15
    elif from_unit == "kelvin" and to_unit == "fahrenheit":
        result = (value - 273.15) * 9/5 + 32
    else:
        result = value

elif option == "Currency":
    from_currency = st.text_input("From Currency (e.g. USD, EUR, PKR)")
    to_currency = st.text_input("To Currency (e.g. USD, EUR, PKR)")
    result = convert_currency(value, from_currency.upper(), to_currency.upper())

st.markdown(f'<div class="result-box">Converted Value: {result}</div>', unsafe_allow_html=True)

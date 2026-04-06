import streamlit as st
from src.components import calcular_gasto_amb_total

# Perform query.

df = calcular_gasto_amb_total

# Print results.
st.write(f"{df}")

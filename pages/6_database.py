import streamlit as st
from src.components import calcular_gasto_amb_total

# Perform query.

df = calcular_gasto_amb_total()

# Print results.
for row in df.itertuples():
    st.write(f"{row.gasto_gestion_amb_total}")

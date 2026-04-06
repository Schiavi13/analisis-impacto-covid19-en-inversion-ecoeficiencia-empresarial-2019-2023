import streamlit as st
from src.connection import get_connection

# Perform query.
conn = get_connection()
df = conn.query('SELECT * from sector_economico;', ttl=600)

# Print results.
for row in df.itertuples():
    st.write(f"{row.id_sector}, {row.sector_nombre}:")

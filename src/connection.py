import streamlit as st
from mysql.connector import Error

def get_connection():
    try:
        connection = st.connection('mysql', type='sql')  
    except Error as e:
        print(f"ERROR DE CONEXIÓN: {e}") 
        return None
    return connection
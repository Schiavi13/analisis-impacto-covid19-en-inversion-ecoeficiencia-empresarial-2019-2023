import streamlit as st

def get_connection():
    connection = st.connection('mysql', type='sql')  
    return connection
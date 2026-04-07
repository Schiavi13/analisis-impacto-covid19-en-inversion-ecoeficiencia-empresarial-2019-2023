import streamlit as st


def get_connection():
    connection = st.connection('mysql', type='sql')  
    connection.session.close()   # Close the SQLAlchemy session
    connection.engine.dispose()
    return None

def close_connection(conn):
    conn.session.close()   # Close the SQLAlchemy session
    conn.engine.dispose()
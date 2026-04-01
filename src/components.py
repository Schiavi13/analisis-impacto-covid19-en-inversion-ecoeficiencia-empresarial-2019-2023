"""
Módulo centralizado de componentes para EcoAnalytics Pro.
Solo funciones puras de datos + CSS mínimo para sidebar.
NO usa unsafe_allow_html con contenido dinámico.
"""
import streamlit as st
import pandas as pd
import plotly.io as pio
import os


# ---------------------------------------------------------------------------
# 1. CARGA DE DATOS (cacheada)
# ---------------------------------------------------------------------------

@st.cache_data
def cargar_datos() -> pd.DataFrame:
    """Carga datos_unificados.csv con limpieza de tipos."""
    rutas = [
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'datos_unificados.csv'),
        'datos_unificados.csv',
        os.path.join('..', 'datos_unificados.csv'),
    ]
    ruta = next((r for r in rutas if os.path.exists(r)), None)
    if ruta is None:
        st.error("No se encontró **datos_unificados.csv**. Ejecute `python src/unificar_datos.py`.")
        return pd.DataFrame()

    df = pd.read_csv(ruta, low_memory=False)
    if 'anio' in df.columns:
        df = df.dropna(subset=['anio'])
        df['anio'] = df['anio'].astype(int)
    for col in ('gastos_totales', 'gasto_gestion_amb', 'total_ingresos', 'personal_ocupado_total'):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df


# ---------------------------------------------------------------------------
# 2. TEMA VISUAL — estilo predeterminado de Streamlit
# ---------------------------------------------------------------------------

def aplicar_tema() -> None:
    """Configura el template de Plotly. Sin CSS personalizado."""
    pio.templates.default = "plotly"


# ---------------------------------------------------------------------------
# 3. HELPERS (funciones puras, sin HTML)
# ---------------------------------------------------------------------------

def delta_pct(actual, anterior):
    """Calcula variación porcentual. Soporta escalares y pandas Series."""
    if isinstance(anterior, pd.Series):
        return ((actual - anterior) / anterior.replace(0, float('nan')) * 100).fillna(0)
    return ((actual - anterior) / anterior * 100) if anterior > 0 else 0.0
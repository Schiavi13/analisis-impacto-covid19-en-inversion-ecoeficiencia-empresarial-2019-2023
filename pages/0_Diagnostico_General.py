import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. CONFIGURACIÓN
st.set_page_config(page_title="EcoAnalytics | Diagnóstico", layout="wide", page_icon="🌳")

def cargar_datos():
    # Buscamos el archivo subido (asegúrate de que en GitHub se llame 'dane.csv')
    ruta_csv = os.path.join(os.path.dirname(__file__), '..', 'dane.csv')
    
    
    if os.path.exists(ruta_csv):
        try:
            # Leemos el CSV original
            df = pd.read_csv(ruta_csv)
            
            # LIMPIEZA DE COLUMNAS: Quitamos espacios y comillas
            df.columns = [str(c).strip().replace('"', '').lower() for c in df.columns]
            
            # LIMPIEZA DE DATOS: Forzar periodo y gastos a números
            if 'periodo' in df.columns:
                df['periodo'] = pd.to_numeric(df['periodo'], errors='coerce')
                df = df.dropna(subset=['periodo'])
                df['periodo'] = df['periodo'].astype(int)
            
            if 'gastos_tot' in df.columns:
                df['gastos_tot'] = pd.to_numeric(df['gastos_tot'], errors='coerce').fillna(0)
                
            return df
        except Exception as e:
            st.error(f"Error al procesar el CSV: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

def main():
    st.title("🌳 Diagnóstico Ambiental (Datos DANE)")
    
    df = cargar_datos()

    if not df.empty:
        # Barra lateral: Filtro de Año
        anios_disponibles = sorted(df['periodo'].unique(), reverse=True)
        # Filtramos para que solo salgan años lógicos (ej. mayores a 2000)
        anios_disponibles = [a for a in anios_disponibles if a > 2000]
        
        anio_sel = st.sidebar.selectbox("Seleccione el Año de Análisis", anios_disponibles)

        # FILTRADO DINÁMICO
        df_f = df[df['periodo'] == anio_sel].copy()
        
        # Agrupación por Sección
        df_grafico = df_f.groupby('seccion')['gastos_tot'].sum().reset_index()
        df_top = df_grafico.sort_values('gastos_tot', ascending=False).head(10)

        # MÉTRICAS
        inversion_total = df_f['gastos_tot'].sum()
        num_empresas = len(df_f)

        col1, col2 = st.columns(2)
        col1.metric(f"Inversión Total {anio_sel}", f"${inversion_total:,.0f}")
        col2.metric("Registros analizados", f"{num_empresas:,}")

        st.markdown("---")

        # GRÁFICO
        if inversion_total > 0:
            st.subheader(f"Top 10 Sectores con mayor Inversión Ambiental - {anio_sel}")
            fig = px.treemap(
                df_top, 
                path=['seccion'], 
                values='gastos_tot',
                color='gastos_tot',
                color_continuous_scale='YlGnBu',
                labels={'gastos_tot': 'Inversión ($)', 'seccion': 'Sector'}
            )
            fig.update_layout(height=600, margin=dict(t=30, l=10, r=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"No se encontraron montos de inversión para el año {anio_sel}. Revisa si los datos están en ceros.")

    else:
        st.error("No se encontró el archivo 'dane.csv' en la raíz del proyecto.")

if __name__ == "__main__":
    main()
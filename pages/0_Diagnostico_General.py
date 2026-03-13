import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="EcoAnalytics | Diagnóstico", layout="wide", page_icon="🌳")

# 2. CARGA DE DATOS INTELIGENTE (Corregida para asegurar tipos de datos)
def obtener_datos():
    # Buscamos el archivo CSV en la raíz del proyecto (un nivel arriba de /pages)
    ruta_csv = os.path.join(os.path.dirname(__file__), '..', 'datos_dane.csv')
    
    if os.path.exists(ruta_csv):
        try:
            df = pd.read_csv(ruta_csv)
            
            # Limpieza de nombres de columnas: quita espacios, comillas y pasa a minúsculas
            df.columns = [c.strip().replace('"', '').lower() for c in df.columns]
            
            # ASEGURAR QUE EL AÑO SEA NUMÉRICO (Evita errores de comparación texto vs número)
            if 'periodo' in df.columns:
                df['periodo'] = pd.to_numeric(df['periodo'], errors='coerce')
                df = df.dropna(subset=['periodo']) # Quita filas sin año
                df['periodo'] = df['periodo'].astype(int)
            
            # Asegurar que gastos_tot sea numérico
            if 'gastos_tot' in df.columns:
                df['gastos_tot'] = pd.to_numeric(df['gastos_tot'], errors='coerce').fillna(0)
                
            return df, "Archivo CSV"
        except Exception as e:
            st.error(f"Error al leer el archivo de datos: {e}")
            return pd.DataFrame(), None
    else:
        st.warning("No se encontró el archivo datos_dane.csv")
        return pd.DataFrame(), None

# 3. INTERFAZ PRINCIPAL
def main():
    st.title("🌳 Diagnóstico de Impacto Ambiental")
    
    df, fuente = obtener_datos()

    if not df.empty:
        st.caption(f"✅ Datos cargados correctamente vía: {fuente}")

        # Identificación de columnas clave
        col_anio = 'periodo'
        col_sec = 'seccion'
        col_val = 'gastos_tot'

        # Verificamos que las columnas existan antes de seguir
        if col_anio in df.columns and col_val in df.columns:
            
            # Filtro de Año en la barra lateral
            anios = sorted(df[col_anio].unique(), reverse=True)
            anio_sel = st.sidebar.selectbox("Seleccione el Año", anios)
            
            # FILTRADO CRUCIAL (Aquí es donde fallaba antes)
            df_f = df[df[col_anio] == anio_sel].copy()
            
            # Agrupar por sección para evitar duplicados en el Treemap y obtener el Top 10
            df_agrupado = df_f.groupby(col_sec)[col_val].sum().reset_index()
            df_top = df_agrupado.sort_values(col_val, ascending=False).head(10)

            # MÉTRICAS RÁPIDAS
            c1, c2, c3 = st.columns(3)
            total_anio = df_f[col_val].sum()
            total_top = df_top[col_val].sum()
            
            # Evitar división por cero
            porcentaje = (total_top / total_anio * 100) if total_anio > 0 else 0
            
            c1.metric("Inversión Total Año", f"${total_anio:,.0f}")
            c2.metric("Inversión Top 10 Sectores", f"${total_top:,.0f}")
            c3.metric("% Representación Top", f"{porcentaje:.1f}%")

            st.markdown("---")

            # GRÁFICO: TREEMAP
            st.subheader(f"Distribución del Gasto Ambiental por Sector - {anio_sel}")
            
            if not df_top.empty:
                fig = px.treemap(
                    df_top, 
                    path=[col_sec], 
                    values=col_val,
                    color=col_val,
                    color_continuous_scale='YlGnBu',
                    labels={col_val: 'Inversión', col_sec: 'Sector'}
                )
                fig.update_layout(margin=dict(t=30, l=10, r=10, b=10), height=550)
                fig.update_traces(textinfo="label+value+percent root")

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f"No hay datos de inversión para el año {anio_sel}")

        else:
            st.error(f"El archivo no tiene las columnas necesarias: {col_anio}, {col_sec}, {col_val}")

    else:
        st.error("No hay datos disponibles para mostrar. Verifica el archivo CSV.")

if __name__ == "__main__":
    main()
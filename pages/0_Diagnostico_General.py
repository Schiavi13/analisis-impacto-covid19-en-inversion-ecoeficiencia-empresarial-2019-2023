import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="EcoAnalytics | Diagnóstico", layout="wide", page_icon="🌳")

# 2. CARGA DE DATOS INTELIGENTE
def obtener_datos():
    # Buscamos el archivo CSV en la raíz del proyecto (un nivel arriba de /pages)
    ruta_csv = os.path.join(os.path.dirname(__file__), '..', 'datos_dane.csv')
    
    if os.path.exists(ruta_csv):
        try:
            df = pd.read_csv(ruta_csv)
            # Limpieza estándar de columnas
            df.columns = [c.strip().replace('"', '').lower() for c in df.columns]
            return df, "Archivo CSV"
        except Exception as e:
            st.error(f"Error al leer el archivo de datos: {e}")
            return pd.DataFrame(), None
    else:
        # Si por alguna razón no está el CSV, podrías mantener tu conexión a MariaDB aquí
        # Por ahora, priorizamos el CSV para asegurar el despliegue rápido.
        st.warning("No se encontró el archivo datos_dane.csv")
        return pd.DataFrame(), None

# 3. INTERFAZ PRINCIPAL
def main():
    st.title("🌳 Diagnóstico de Impacto Ambiental")
    
    df, fuente = obtener_datos()

    if not df.empty:
        st.caption(f"✅ Datos cargados correctamente vía: {fuente}")

        # Identificación automática de columnas (basado en lo que ya sabemos de tu DB)
        col_anio = 'periodo' if 'periodo' in df.columns else df.columns[0]
        col_sec = 'seccion' if 'seccion' in df.columns else df.columns[1]
        col_val = 'gastos_tot' if 'gastos_tot' in df.columns else df.columns[2]

        # Filtro de Año en la barra lateral
        anios = sorted(df[col_anio].unique(), reverse=True)
        anio_sel = st.sidebar.selectbox("Seleccione el Año", anios)
        
        # Filtrado para el Top 10
        df_f = df[df[col_anio] == anio_sel]
        df_top = df_f.sort_values(col_val, ascending=False).head(10)

        # MÉTRICAS RÁPIDAS
        c1, c2, c3 = st.columns(3)
        total_anio = df_f[col_val].sum()
        total_top = df_top[col_val].sum()
        
        c1.metric("Inversión Total Año", f"${total_anio:,.0f}")
        c2.metric("Inversión Top 10", f"${total_top:,.0f}")
        c3.metric("% Representación Top", f"{(total_top/total_anio)*100:.1f}%")

        st.markdown("---")

        # GRÁFICO: TREEMAP (Menos saturado)
        st.subheader(f"Distribución del Gasto Ambiental por Sector - {anio_sel}")
        
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
        st.error("No hay datos disponibles para mostrar.")

if __name__ == "__main__":
    main()
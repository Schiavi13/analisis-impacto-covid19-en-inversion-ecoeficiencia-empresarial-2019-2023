"""Página 4 — Análisis Sectorial."""
import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.components import cargar_datos, aplicar_tema

st.set_page_config(page_title="Sectorial", page_icon="🏭", layout="wide")
aplicar_tema()

st.header("🏭 Análisis Sectorial")
st.caption("Benchmarking macroeconómico frente al promedio nacional.")

df = cargar_datos()
if not df.empty:
    sectores = sorted(df['nombre_sector'].dropna().unique())

    # ── Filtro inline ──────────────────────────────────────────────────────
    with st.container(border=True):
        col_f, col_info = st.columns([2, 2])
        with col_f:
            sector = st.selectbox("🏭 Sector a analizar:", sectores)
        with col_info:
            n_emp_sect = df[df['nombre_sector']==sector]['id_empresa'].nunique()
            st.metric("Empresas en el sector", f"{n_emp_sect:,}")

    df_sec = df[df['nombre_sector']==sector]

    st.divider()
    n = df_sec['id_empresa'].nunique()
    gs = df_sec['gastos_totales'].sum()
    gn = df['gastos_totales'].sum()
    share = (gs/gn*100) if gn > 0 else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("🏭 Empresas", f"{n:,}")
    c2.metric("💵 Gasto Sectorial", f"${gs/1e6:,.1f}M")
    c3.metric("📊 Share Nacional", f"{share:.2f}%")

    tab1, tab2 = st.tabs(["📉 Boxplot Anual", "📊 Benchmarking"])

    with tab1:
        db = df_sec[df_sec['gastos_totales'] > 0]
        fig = px.box(db, x='anio', y='gastos_totales', points='outliers', color='anio',
                     labels={'gastos_totales':'Gasto Total ($)','anio':'Año'})
        fig.update_layout(xaxis=dict(tickmode='linear', dtick=1), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        av_s = df_sec.groupby('anio')['gastos_totales'].mean().reset_index()
        av_s['Tipo'] = f'Sector: {sector.title()}'
        av_n = df.groupby('anio')['gastos_totales'].mean().reset_index()
        av_n['Tipo'] = 'Promedio Nacional'
        db2 = pd.concat([av_s, av_n])
        fig2 = px.line(db2, x='anio', y='gastos_totales', color='Tipo', markers=True,
                       labels={'gastos_totales':'Gasto Promedio ($)','anio':'Año'},
                       color_discrete_sequence=['#3b82f6','#ef4444'])
        fig2.update_layout(xaxis=dict(tickmode='linear', dtick=1),
                           legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
        st.plotly_chart(fig2, use_container_width=True)
        csv_sec = df_sec.groupby('anio').agg(
            Empresas=('id_empresa','nunique'), Gasto=('gastos_totales','sum'),
            Amb=('gasto_gestion_amb','sum'), Ingresos=('total_ingresos','sum')
        ).reset_index().to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Descargar datos del sector", csv_sec,
                           f"sector_{sector.replace(' ','_')}.csv", "text/csv")
else:
    st.warning("No hay datos.")

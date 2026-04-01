"""Página 0 — Diagnóstico Ambiental General."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.components import cargar_datos, aplicar_tema, delta_pct

st.set_page_config(page_title="Diagnóstico", layout="wide", page_icon="🌳")
aplicar_tema()

st.header("🌳 Diagnóstico Ambiental Integral")
st.caption("Panorama macroeconómico y ambiental del ecosistema empresarial colombiano.")

df = cargar_datos()
if not df.empty:
    anios = sorted(df['anio'].unique(), reverse=True)

    # ── Filtro inline ──────────────────────────────────────────────────────
    with st.container(border=True):
        col_f, col_info = st.columns([1, 3])
        with col_f:
            anio = st.selectbox("📅 Año de análisis:", anios)
        with col_info:
            st.caption(f"Mostrando datos del año **{anio}**. Selecciona otro año para comparar.")

    df_f = df[df['anio'] == anio]
    df_prev = df[df['anio'] == anio - 1] if (anio - 1) in anios else pd.DataFrame()

    gasto = df_f['gastos_totales'].sum()
    ingresos = df_f['total_ingresos'].sum()
    empresas = df_f['id_empresa'].nunique()
    amb = df_f['gasto_gestion_amb'].sum()
    personal = df_f['personal_ocupado_total'].sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Gasto Total", f"${gasto/1e6:,.1f}M",
              f"{delta_pct(gasto, df_prev['gastos_totales'].sum() if not df_prev.empty else 0):+.1f}%")
    c2.metric("Ingresos", f"${ingresos/1e6:,.1f}M",
              f"{delta_pct(ingresos, df_prev['total_ingresos'].sum() if not df_prev.empty else 0):+.1f}%")
    c3.metric("Empresas", f"{empresas:,}")
    c4.metric("Gasto Ambiental", f"${amb/1e6:,.1f}M")
    c5.metric("Personal", f"{personal:,.0f}")

    st.divider()
    tab1, tab2, tab3, tab4 = st.tabs(["🌲 Treemap", "🥧 Composición", "📈 Tendencia", "📋 Tabla"])

    with tab1:
        df_top = df_f.groupby('nombre_sector')['gastos_totales'].sum().reset_index().nlargest(10, 'gastos_totales')
        if not df_top.empty and df_top['gastos_totales'].sum() > 0:
            fig = px.treemap(df_top, path=['nombre_sector'], values='gastos_totales',
                             color='gastos_totales', color_continuous_scale='Tealgrn')
            fig.update_layout(height=480, margin=dict(t=20, l=10, r=10, b=10))
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        col_p, col_t = st.columns([1.5, 1])
        with col_p:
            df_pie = df_f.groupby('nombre_sector')['gastos_totales'].sum().reset_index().nlargest(8, 'gastos_totales')
            fig_pie = px.pie(df_pie, values='gastos_totales', names='nombre_sector', hole=0.4,
                             color_discrete_sequence=px.colors.sequential.Tealgrn)
            fig_pie.update_traces(textinfo='percent+label', textposition='outside')
            fig_pie.update_layout(height=420, showlegend=False, margin=dict(t=20, b=20))
            st.plotly_chart(fig_pie, use_container_width=True)
        with col_t:
            ratio = (amb / gasto * 100) if gasto > 0 else 0
            prom = gasto / empresas if empresas > 0 else 0
            conc = (df_pie['gastos_totales'].sum() / gasto * 100) if gasto > 0 else 0
            st.info(
                f"**Insights — {anio}**\n\n"
                f"- **{ratio:.1f}%** del gasto → gestión ambiental\n"
                f"- Gasto promedio/empresa: **${prom/1e6:,.2f}M**\n"
                f"- Top 8 sectores = **{conc:.0f}%** del total"
            )

    with tab3:
        dh = df.groupby('anio').agg(g=('gastos_totales','sum'), a=('gasto_gestion_amb','sum'),
                                     i=('total_ingresos','sum')).reset_index()
        fig_l = go.Figure()
        fig_l.add_trace(go.Scatter(x=dh['anio'], y=dh['i'], name='Ingresos',
                                   mode='lines+markers', line=dict(color='#3b82f6', width=3)))
        fig_l.add_trace(go.Scatter(x=dh['anio'], y=dh['g'], name='Gasto Total',
                                   mode='lines+markers', line=dict(color='#ef4444', width=3)))
        fig_l.add_trace(go.Scatter(x=dh['anio'], y=dh['a'], name='Gasto Ambiental',
                                   mode='lines+markers', line=dict(color='#10b981', width=3, dash='dot')))
        fig_l.add_vrect(x0=anio-0.3, x1=anio+0.3, fillcolor='rgba(59,130,246,0.08)', line_width=0)
        fig_l.update_layout(xaxis=dict(tickmode='linear', dtick=1, title='Año'), yaxis_title='Monto ($)',
                            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1), height=420)
        st.plotly_chart(fig_l, use_container_width=True)

    with tab4:
        dt = df_f.groupby('nombre_sector').agg(
            Empresas=('id_empresa','nunique'), Gasto_Total=('gastos_totales','sum'),
            Gasto_Amb=('gasto_gestion_amb','sum'), Ingresos=('total_ingresos','sum'),
            Personal=('personal_ocupado_total','sum')).reset_index().sort_values('Gasto_Total', ascending=False)
        dt['%_Amb'] = (dt['Gasto_Amb'] / dt['Gasto_Total'] * 100).round(1).fillna(0)
        st.dataframe(dt, use_container_width=True, hide_index=True)
        st.info("**% Amb:** porcentaje del gasto sectorial destinado a gestión ambiental.")
        csv_dt = dt.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Descargar tabla como CSV", csv_dt,
                           f"diagnostico_sectorial_{anio}.csv", "text/csv")

else:
    st.error("❌ No se pudo cargar 'datos_unificados.csv'.")
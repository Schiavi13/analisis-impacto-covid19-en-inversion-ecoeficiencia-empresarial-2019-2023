"""Página 1 — Impacto Sistémico COVID-19."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.components import cargar_datos, aplicar_tema, delta_pct

st.set_page_config(page_title="Impacto COVID-19", page_icon="🦠", layout="wide")
aplicar_tema()

st.header("🦠 Impacto Sistémico COVID-19")
st.caption("Análisis multidimensional del choque pandémico (2019-2023).")

df = cargar_datos()
if not df.empty:
    g_pre = df[df['anio']==2019]['gastos_totales'].sum()
    g_covid = df[df['anio']==2020]['gastos_totales'].sum()
    g_post = df[df['anio'].isin([2022,2023])].groupby('anio')['gastos_totales'].sum().mean()
    caida = delta_pct(g_covid, g_pre)
    recup = delta_pct(g_post, g_covid)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📊 Gasto 2019 (Base)", f"${g_pre/1e6:,.1f}M")
    c2.metric("📉 Gasto 2020 (COVID)", f"${g_covid/1e6:,.1f}M")
    c3.metric("🦠 Caída COVID", f"{caida:+.1f}%")
    c4.metric("🚀 Recuperación 22-23", f"{recup:+.1f}%")

    st.divider()
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Curva", "🏭 Resiliencia", "🌱 Adopción", "📋 Tabla"])

    with tab1:
        dh = df.groupby('anio').agg(g=('gastos_totales','sum'), a=('gasto_gestion_amb','sum')).reset_index().sort_values('anio')
        etapas = {2019:'Pre-Pandemia',2020:'Caída',2021:'Recuperación',2022:'Estabilización',2023:'Crecimiento'}
        dh['Etapa'] = dh['anio'].map(etapas)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dh['anio'], y=dh['g'], name='Gasto Total', fill='tozeroy',
                                  fillcolor='rgba(239,68,68,0.15)', line=dict(color='#ef4444', width=3),
                                  mode='lines+markers+text', text=dh['Etapa'], textposition='top center',
                                  marker=dict(size=10, line=dict(width=2, color='white'))))
        fig.add_trace(go.Scatter(x=dh['anio'], y=dh['a'], name='Gasto Ambiental', fill='tozeroy',
                                  fillcolor='rgba(16,185,129,0.15)', line=dict(color='#10b981', width=3, dash='dot'),
                                  mode='lines+markers', marker=dict(size=8)))
        fig.add_vrect(x0=2019.5, x1=2020.5, fillcolor='rgba(239,68,68,0.08)', line_width=0,
                      annotation_text='Zona COVID', annotation_position='top left')
        fig.update_layout(xaxis=dict(tickmode='linear', dtick=1, title='Año'), yaxis_title='Monto ($)',
                          legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1), height=450)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("**¿Qué sectores fueron más golpeados y cuáles se recuperaron?**")
        gs = {}
        for y in [2019, 2020, 2023]:
            gs[y] = df[df['anio']==y].groupby('nombre_sector')['gastos_totales'].sum()
        dr = pd.DataFrame(gs).dropna()
        dr['caida_%'] = ((dr[2020] - dr[2019]) / dr[2019].replace(0, float('nan')) * 100).fillna(0).round(1)
        dr['recup_%'] = ((dr[2023] - dr[2020]) / dr[2020].replace(0, float('nan')) * 100).fillna(0).round(1)
        dr = dr.reset_index().nlargest(10, 2019)
        fig_r = go.Figure()
        fig_r.add_trace(go.Bar(x=dr['nombre_sector'], y=dr['caida_%'], name='Caída 20 vs 19', marker_color='#ef4444'))
        fig_r.add_trace(go.Bar(x=dr['nombre_sector'], y=dr['recup_%'], name='Recup 23 vs 20', marker_color='#10b981'))
        fig_r.update_layout(barmode='group', yaxis_title='Variación (%)', xaxis=dict(tickangle=-35),
                            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1), height=450)
        st.plotly_chart(fig_r, use_container_width=True)

    with tab3:
        st.markdown("**¿El COVID-19 frenó la adopción de prácticas ambientales?**")
        cols_inv = ['realiza_inv_red_emision_aire','realiza_inv_energia_limp','realiza_inv_ahorro_agua',
                    'realiza_inv_protec_suelo','realiza_inv_disp_desechos']
        noms = ['Emisiones','Energía Limpia','Ahorro Agua','Suelo','Desechos']
        rows = []
        for a in sorted(df['anio'].unique()):
            da = df[df['anio']==a]; n = len(da)
            for c, nm in zip(cols_inv, noms):
                pct = (da[c]==1).sum()/n*100 if c in da.columns and n > 0 else 0
                rows.append({'Año': a, 'Inversión': nm, '% Adopción': round(pct, 1)})
        fig_a = px.line(pd.DataFrame(rows), x='Año', y='% Adopción', color='Inversión', markers=True,
                        color_discrete_sequence=['#3b82f6','#10b981','#06b6d4','#f59e0b','#8b5cf6'])
        fig_a.add_vrect(x0=2019.5, x1=2020.5, fillcolor='rgba(239,68,68,0.08)', line_width=0)
        fig_a.update_layout(xaxis=dict(tickmode='linear', dtick=1), yaxis_title='% Empresas',
                            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1), height=420)
        st.plotly_chart(fig_a, use_container_width=True)

    with tab4:
        dc = df.groupby('anio').agg(Empresas=('id_empresa','nunique'), Gasto=('gastos_totales','sum'),
                                     Amb=('gasto_gestion_amb','sum'), Ingresos=('total_ingresos','sum'),
                                     Personal=('personal_ocupado_total','sum')).reset_index()
        dc['%_Amb'] = (dc['Amb']/dc['Gasto']*100).round(2)
        dc['Gasto_Emp'] = (dc['Gasto']/dc['Empresas']).round(0)
        st.dataframe(dc, use_container_width=True, hide_index=True)
        st.info("Compare **%_Amb** entre 2019 y 2020 para evaluar el impacto diferencial del COVID.")
else:
    st.warning("⚠️ Sin datos.")
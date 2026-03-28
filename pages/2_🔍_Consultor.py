"""Página 2 — Consultor Experto Analítico."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.components import cargar_datos, aplicar_tema, delta_pct

st.set_page_config(page_title="Consultor AI", page_icon="🔍", layout="wide")
aplicar_tema()

st.header("🔍 Consultor Experto Analítico")
st.caption("Diagnóstico integral por año: hallazgos cualitativos + métricas reales.")


CONOCIMIENTO = {
    2019: ("Pre-pandemia: baja priorización presupuestal para gestión ambiental.",
           "Incorporar indicadores de ecoeficiencia en los KPIs estratégicos."),
    2020: ("Caída del flujo de caja obligó a recortar CAPEX en rubros ecológicos.",
           "Aplicar a fondos de fomento e instrumentos financieros verdes."),
    2021: ("Quiebre logístico en suministros para energías renovables.",
           "Desarrollar red de proveedores de circularidad nacional."),
    2022: ("Incertidumbre regulatoria frenó la actualización tecnológica.",
           "Priorizar inversiones en eficiencia energética por retorno directo."),
    2023: ("Falta de talento en medición de Huella de Carbono (Alcance 1,2,3).",
           "Subcontratación de firmas Greentech o automatización digital."),
}

df = cargar_datos()
if not df.empty:
    anios = sorted(df['anio'].unique())

    # ── Filtro inline ──────────────────────────────────────────────────────
    with st.container(border=True):
        col_f, col_ctx = st.columns([1, 3])
        with col_f:
            anio = st.selectbox("📅 Año de consulta:", anios, index=len(anios)-1)
        with col_ctx:
            riesgo_prev, _ = CONOCIMIENTO.get(anio, ("—", "—"))
            st.caption(f"📌 Contexto **{anio}:** {riesgo_prev}")

    df_a = df[df['anio']==anio]
    df_p = df[df['anio']==anio-1] if (anio-1) in anios else pd.DataFrame()

    # 1. Hallazgos cualitativos
    st.subheader(f"1. Hallazgos — {anio}")
    riesgo, accion = CONOCIMIENTO.get(anio, ("Sin análisis cualitativo.", "Revise datos cuantitativos."))
    col1, col2 = st.columns(2)
    col1.error(f"⚠️ **Riesgo:** {riesgo}")
    col2.success(f"💡 **Acción:** {accion}")

    # 2. KPIs
    st.divider()
    st.subheader(f"2. Pulso Cuantitativo — {anio}")
    g = df_a['gastos_totales'].sum()
    ing = df_a['total_ingresos'].sum()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Gasto Total", f"${g/1e6:,.1f}M",
              f"{delta_pct(g, df_p['gastos_totales'].sum() if not df_p.empty else 0):+.1f}%")
    m2.metric("Ingresos", f"${ing/1e6:,.1f}M",
              f"{delta_pct(ing, df_p['total_ingresos'].sum() if not df_p.empty else 0):+.1f}%")
    m3.metric("Empresas", f"{df_a['id_empresa'].nunique():,}")
    m4.metric("Gasto Ambiental", f"${df_a['gasto_gestion_amb'].sum()/1e6:,.1f}M")

    # 3. Tabs
    st.divider()
    st.subheader(f"3. Análisis Profundo — {anio}")
    tab1, tab2, tab3 = st.tabs(["🏭 Top Sectores", "🌱 Inversiones", "📊 Comparativa"])

    with tab1:
        ds = df_a.groupby('nombre_sector')['gastos_totales'].sum().reset_index().nlargest(10, 'gastos_totales')
        fig = px.bar(ds, x='gastos_totales', y='nombre_sector', orientation='h', color='gastos_totales',
                     color_continuous_scale='Blues', labels={'gastos_totales':'Gasto ($)','nombre_sector':'Sector'})
        fig.update_layout(yaxis=dict(autorange='reversed'), showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        cols = ['realiza_inv_red_emision_aire','realiza_inv_evita_ruido_vibra','realiza_inv_energia_limp',
                'realiza_inv_ahorro_agua','realiza_inv_inst_med_agua','realiza_inv_protec_suelo','realiza_inv_disp_desechos']
        noms = ['Emisiones','Ruido','Energía Limpia','Ahorro Agua','Med. Agua','Suelo','Desechos']
        n = len(df_a)
        pcts = [(df_a[c]==1).sum()/n*100 if c in df_a.columns and n>0 else 0 for c in cols]
        di = pd.DataFrame({'Inversión': noms, 'Pct': pcts}).sort_values('Pct', ascending=True)
        fig_i = px.bar(di, x='Pct', y='Inversión', orientation='h', color='Pct', color_continuous_scale='Greens',
                       labels={'Pct':'% Empresas'})
        fig_i.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_i, use_container_width=True)
        st.info(f"En {anio}, **{sum(pcts)/len(pcts):.1f}%** promedio de empresas reporta inversión ambiental activa.")

    with tab3:
        dh = df.groupby('anio').agg(Gasto=('gastos_totales','sum'), Amb=('gasto_gestion_amb','sum'),
                                     Emp=('id_empresa','nunique')).reset_index()
        fig_c = go.Figure()
        fig_c.add_trace(go.Bar(x=dh['anio'], y=dh['Gasto'], name='Gasto Total', marker_color='#3b82f6'))
        fig_c.add_trace(go.Bar(x=dh['anio'], y=dh['Amb'], name='Gasto Ambiental', marker_color='#10b981'))
        fig_c.add_trace(go.Scatter(x=dh['anio'], y=dh['Emp']*1e4, name='Empresas (x10K)',
                                    mode='lines+markers', marker_color='#f59e0b', yaxis='y2'))
        fig_c.add_vrect(x0=anio-0.4, x1=anio+0.4, fillcolor='rgba(59,130,246,0.08)', line_width=2,
                        line_color='rgba(59,130,246,0.4)')
        fig_c.update_layout(barmode='group', xaxis=dict(tickmode='linear', dtick=1), yaxis_title='Monto ($)',
                            yaxis2=dict(title='Empresas', overlaying='y', side='right'),
                            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1), height=420)
        st.plotly_chart(fig_c, use_container_width=True)
else:
    st.warning("⚠️ Sin datos.")
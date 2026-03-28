"""Página 3 — Buscador Empresarial."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.components import cargar_datos, aplicar_tema

st.set_page_config(page_title="Empresarial", page_icon="🏢", layout="wide")
aplicar_tema()

st.header("🏢 Buscador Empresarial")
st.caption("Perfil financiero y esfuerzos ambientales por empresa.")

df = cargar_datos()
if not df.empty:
    empresas = sorted(df['id_empresa'].dropna().unique())
    id_sel = st.sidebar.selectbox("🔎 ID Empresa:", empresas, index=0)
    df_emp = df[df['id_empresa']==id_sel].sort_values('anio')
    sector = df_emp['nombre_sector'].iloc[0] if not df_emp.empty else "Desconocido"

    st.subheader(f"Empresa ID-{id_sel} | Sector: {sector.title()}")
    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Ingresos (Media)", f"${df_emp['total_ingresos'].mean()/1e6:,.1f}M")
    c2.metric("📉 Gastos (Media)", f"${df_emp['gastos_totales'].mean()/1e6:,.1f}M")
    c3.metric("🌱 Inv. Ambiental", f"${df_emp['gasto_gestion_amb'].mean()/1e3:,.1f}K")
    c4.metric("👥 Personal", f"{df_emp['personal_ocupado_total'].mean():,.0f}")

    tab1, tab2, tab3 = st.tabs(["📊 Evolución", "🎯 Radar Ambiental", "🗄️ Datos"])

    with tab1:
        df_fin = df_emp[['anio','total_ingresos','gastos_totales']].melt(id_vars='anio')
        df_fin['variable'] = df_fin['variable'].map({'total_ingresos':'Ingresos','gastos_totales':'Gastos'})
        fig = px.bar(df_fin, x='anio', y='value', color='variable', barmode='group',
                     labels={'value':'Monto ($)','anio':'Año','variable':'Concepto'},
                     color_discrete_sequence=['#3b82f6','#ef4444'])
        fig.update_layout(xaxis=dict(tickmode='linear', dtick=1))
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        cols_inv = ['realiza_inv_red_emision_aire','realiza_inv_evita_ruido_vibra','realiza_inv_energia_limp',
                    'realiza_inv_ahorro_agua','realiza_inv_inst_med_agua','realiza_inv_protec_suelo','realiza_inv_disp_desechos']
        dr = df_emp[cols_inv].sum().reset_index()
        dr.columns = ['area','frecuencia']
        dr['area'] = [c.replace('realiza_inv_','').replace('_',' ').title() for c in dr['area']]
        fig2 = go.Figure(data=go.Scatterpolar(r=dr['frecuencia'], theta=dr['area'],
                                               fill='toself', marker_color='#10b981'))
        fig2.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, df_emp['anio'].nunique()])),
                           showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        ds_export = df_emp[['anio','total_ingresos','gastos_totales','gasto_gestion_amb','personal_ocupado_total']]
        st.dataframe(ds_export, use_container_width=True, hide_index=True)
        csv_emp = ds_export.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Descargar datos empresa", csv_emp,
                           f"empresa_{id_sel}.csv", "text/csv")

else:
    st.warning("Datos no disponibles.")

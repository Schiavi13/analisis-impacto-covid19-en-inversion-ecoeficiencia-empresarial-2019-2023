"""Página 5 — Ciencia de Datos (ampliada)."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.components import cargar_datos, aplicar_tema
from src.analytics import (
    calcular_ratios_ecoeficiencia,
    calcular_cagr,
    clasificar_tamanio_empresa,
    generar_autodiagnostico,
)

st.set_page_config(page_title="Data Science", page_icon="🧬", layout="wide")
aplicar_tema()

st.header("🧬 Deep Data Science")
st.caption("Correlaciones, distribuciones, ecoeficiencia y tasas de crecimiento.")

df_raw = cargar_datos()

if not df_raw.empty:
    # Enriquecer con indicadores calculados
    df = calcular_ratios_ecoeficiencia(df_raw)
    df = clasificar_tamanio_empresa(df)

    COLS_NUM = ['total_ingresos', 'gastos_totales', 'gasto_gestion_amb', 'personal_ocupado_total']
    NOMS = ['Ingresos', 'Gastos Totales', 'Gasto Amb.', 'Personal']

    tab1, tab4, tab5 = st.tabs([
        "🔥 Correlación", "📈 CAGR Sectorial", "📊 Estadísticas",
    ])

    # ── TAB 1: Heatmap de correlación ────────────────────────────────────
    with tab1:
        st.markdown("**Inteligencia Relacional:** valores cercanos a ±1 = alta relación lineal.")
        corr = df[COLS_NUM].corr().round(2)
        fig = go.Figure(data=go.Heatmap(
            z=corr.values, x=NOMS, y=NOMS, colorscale='RdBu',
            zmid=0, text=corr.values, texttemplate='%{text}', showscale=True,
        ))
        fig.update_layout(height=450, margin=dict(t=30, b=30))
        st.plotly_chart(fig, use_container_width=True)

        # Autodiagnóstico basado en datos
        diag = generar_autodiagnostico(df)
        st.divider()
        st.subheader("🤖 Diagnóstico Automático")
        cols_diag = st.columns(2)
        with cols_diag[0]:
            st.info(diag.get('correlacion', ''))
            st.info(diag.get('sector_lider', ''))
        with cols_diag[1]:
            st.info(diag.get('tendencia_ecologia', ''))
            st.info(diag.get('ratio_eco_promedio', ''))
        if 'alerta' in diag:
            if '⚠️' in diag['alerta']:
                st.warning(diag['alerta'])
            else:
                st.success(diag['alerta'])

    # ── TAB 4: CAGR sectorial ────────────────────────────────────────────
    with tab4:
        st.markdown("**CAGR:** tasa de crecimiento anual compuesto entre el primer y último año disponible.")
        col_cagr = st.selectbox("Variable para CAGR:", ['gastos_totales', 'total_ingresos', 'gasto_gestion_amb'],
                                format_func=lambda c: {'gastos_totales': 'Gasto Total',
                                                        'total_ingresos': 'Ingresos',
                                                        'gasto_gestion_amb': 'Gasto Ambiental'}[c])
        cagr_df = calcular_cagr(df, col_cagr, 'nombre_sector').dropna(subset=['cagr_%']).sort_values('cagr_%', ascending=True)
        top_n = min(20, len(cagr_df))
        cagr_plot = cagr_df.tail(top_n)  # top positivos + negativos

        fig_cagr = px.bar(cagr_plot, x='cagr_%', y='nombre_sector', orientation='h',
                          color='cagr_%', color_continuous_scale='RdYlGn',
                          labels={'cagr_%': 'CAGR (%)', 'nombre_sector': 'Sector'},
                          title=f'Top {top_n} Sectores por CAGR — {col_cagr}')
        fig_cagr.add_vline(x=0, line_dash='dash', line_color='gray')
        fig_cagr.update_layout(showlegend=False, height=500, yaxis=dict(autorange='reversed'))
        st.plotly_chart(fig_cagr, use_container_width=True)

        with st.expander("📋 Ver tabla completa de CAGR"):
            st.dataframe(
                cagr_df.rename(columns={'nombre_sector': 'Sector', 'v_inicial': 'Valor Inicial ($)',
                                         'v_final': 'Valor Final ($)', 'n_anios': 'Años', 'cagr_%': 'CAGR (%)'}),
                use_container_width=True, hide_index=True,
            )
            csv = cagr_df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Descargar CAGR como CSV", csv, "cagr_sectorial.csv", "text/csv")

    # ── TAB 5: Estadísticas ──────────────────────────────────────────────
    with tab5:
        st.markdown("**Estadísticas descriptivas globales:**")
        st.dataframe(df[COLS_NUM].describe().T.rename(
            index=dict(zip(COLS_NUM, NOMS))), use_container_width=True)

        st.divider()
        st.markdown("**Dispersión Multidimensional (Log):** X=Ingresos, Y=Gastos, Tamaño=Personal.")
        anio_s = st.selectbox("Año:", sorted(df['anio'].unique(), reverse=True), key='scatter_anio')
        ds = df[(df['anio'] == anio_s) & (df['total_ingresos'] > 0) & (df['gastos_totales'] > 0)]
        if not ds.empty:
            fig_s = px.scatter(ds, x='total_ingresos', y='gastos_totales',
                               color='tamanio_empresa', size='personal_ocupado_total',
                               hover_name='id_empresa', log_x=True, log_y=True,
                               labels={'total_ingresos': 'Ingresos ($)', 'gastos_totales': 'Gastos ($)',
                                       'tamanio_empresa': 'Tamaño'},
                               title=f'Clústeres por Tamaño de Empresa (Log-Log) — {anio_s}',
                               color_discrete_sequence=px.colors.qualitative.Set2,
                               category_orders={'tamanio_empresa': ['Microempresa', 'Pequeña', 'Mediana', 'Grande']})
            st.plotly_chart(fig_s, use_container_width=True)

else:
    st.warning("Sin datos. Ejecute `python src/unificar_datos.py` primero.")

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

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔥 Correlación", "📉 Distribuciones", "🌱 Ecoeficiencia",
        "📈 CAGR Sectorial", "📊 Estadísticas",
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

    # ── TAB 2: Distribuciones ────────────────────────────────────────────
    with tab2:
        st.markdown("**Distribución y outliers** por variable y año.")
        col_sel = st.selectbox("Variable:", COLS_NUM,
                               format_func=lambda c: dict(zip(COLS_NUM, NOMS))[c])
        anios = sorted(df['anio'].unique(), reverse=True)
        anio_d = st.selectbox("Año:", anios, key='dist_anio')
        da = df[(df['anio'] == anio_d) & (df[col_sel] > 0)]

        c1, c2 = st.columns(2)
        with c1:
            fig_hist = px.histogram(da, x=col_sel, nbins=40, color='tamanio_empresa',
                                    color_discrete_sequence=px.colors.qualitative.Set2,
                                    labels={col_sel: dict(zip(COLS_NUM, NOMS))[col_sel]},
                                    title=f'Histograma — {anio_d}',
                                    barmode='overlay', opacity=0.7)
            fig_hist.update_layout(showlegend=True, legend_title='Tamaño')
            st.plotly_chart(fig_hist, use_container_width=True)

        with c2:
            fig_box = px.box(da, x='tamanio_empresa', y=col_sel, color='tamanio_empresa',
                             color_discrete_sequence=px.colors.qualitative.Set2,
                             labels={col_sel: dict(zip(COLS_NUM, NOMS))[col_sel],
                                     'tamanio_empresa': 'Tamaño'},
                             title=f'Boxplot por Tamaño — {anio_d}',
                             category_orders={'tamanio_empresa': ['Microempresa', 'Pequeña', 'Mediana', 'Grande']})
            fig_box.update_layout(showlegend=False)
            st.plotly_chart(fig_box, use_container_width=True)

        st.info(
            f"**Mediana:** ${da[col_sel].median()/1e6:,.2f}M  |  "
            f"**P75:** ${da[col_sel].quantile(0.75)/1e6:,.2f}M  |  "
            f"**P95:** ${da[col_sel].quantile(0.95)/1e6:,.2f}M  |  "
            f"**Outliers (>P95):** {(da[col_sel] > da[col_sel].quantile(0.95)).sum()} empresas"
        )

    # ── TAB 3: Ecoeficiencia ─────────────────────────────────────────────
    with tab3:
        st.markdown("**Indicadores de ecoeficiencia** calculados a partir de los datos reales.")

        kpi1, kpi2, kpi3 = st.columns(3)
        anio_rec = df['anio'].max()
        df_rec = df[df['anio'] == anio_rec]
        kpi1.metric("Ratio Eco/Ingreso (mediana)", f"{df_rec['ratio_eco_ingreso'].median():.3f}%")
        kpi2.metric("Eco per-cápita (mediana)", f"${df_rec['eco_per_capita'].median():,.0f}")
        kpi3.metric("Intensidad Gasto (mediana)", f"{df_rec['intensidad_gasto'].median():.1f}%")

        st.divider()
        # Evolución temporal de los 3 indicadores
        eco_anual = df.groupby('anio').agg(
            ratio_eco=('ratio_eco_ingreso', 'median'),
            eco_cap=('eco_per_capita', 'median'),
            intensidad=('intensidad_gasto', 'median'),
        ).reset_index()

        fig_eco = go.Figure()
        fig_eco.add_trace(go.Scatter(x=eco_anual['anio'], y=eco_anual['ratio_eco'],
                                      name='Eco/Ingreso (%)', mode='lines+markers',
                                      line=dict(color='#10b981', width=3)))
        fig_eco.add_vrect(x0=2019.5, x1=2020.5, fillcolor='rgba(239,68,68,0.08)', line_width=0,
                          annotation_text='COVID', annotation_position='top left')
        fig_eco.update_layout(xaxis=dict(tickmode='linear', dtick=1, title='Año'),
                              yaxis_title='Ratio Mediano (%)', title='Evolución del Ratio Eco/Ingreso',
                              legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                              height=380)
        st.plotly_chart(fig_eco, use_container_width=True)

        st.markdown("**Ecoeficiencia por tamaño de empresa:**")
        eco_tam = df.groupby(['tamanio_empresa', 'anio']).agg(
            ratio=('ratio_eco_ingreso', 'median')
        ).reset_index()
        cat_order = {'tamanio_empresa': ['Microempresa', 'Pequeña', 'Mediana', 'Grande']}
        fig_tam = px.line(eco_tam, x='anio', y='ratio', color='tamanio_empresa', markers=True,
                          labels={'ratio': 'Ratio Eco/Ingreso (%)', 'anio': 'Año',
                                  'tamanio_empresa': 'Tamaño'},
                          color_discrete_sequence=px.colors.qualitative.Set2,
                          category_orders=cat_order)
        fig_tam.update_layout(xaxis=dict(tickmode='linear', dtick=1),
                              legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                              height=350)
        st.plotly_chart(fig_tam, use_container_width=True)
        st.info("**Lectura:** Las empresas **Grandes** tienden a tener mayor ratio eco/ingreso. "
                "Una caída en 2020 refleja el impacto COVID en las inversiones ambientales.")

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

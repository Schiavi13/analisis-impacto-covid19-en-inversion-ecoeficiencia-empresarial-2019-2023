"""Página 3 — Buscador Empresarial con filtros inline en la parte superior."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.components import cargar_datos, aplicar_tema
from src.analytics import calcular_ratios_ecoeficiencia, clasificar_tamanio_empresa

# ─────────────────────── CONFIG ───────────────────────────────────────────────
st.set_page_config(page_title="Empresarial", page_icon="🏢", layout="wide")
aplicar_tema()

# ─────────────────────── DATOS ────────────────────────────────────────────────
df_raw = cargar_datos()
if df_raw.empty:
    st.warning("Datos no disponibles.")
    st.stop()

df_all = calcular_ratios_ecoeficiencia(df_raw)
df_all = clasificar_tamanio_empresa(df_all)

# ─────────────────────── ENCABEZADO + MODO ────────────────────────────────────
st.header("🏢 Módulo Empresarial")

# Selector de modo prominente justo bajo el header
col_modo, col_info = st.columns([2, 3])
with col_modo:
    modo = st.radio(
        "**Modo de consulta:**",
        ["🏷️ Por ID de empresa", "🔍 Por filtros"],
        index=0,
        horizontal=True,
    )
modo_id = modo.startswith("🏷️")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# MODO A — POR ID DE EMPRESA
# ═══════════════════════════════════════════════════════════════════════════════
if modo_id:
    # ── Barra de búsqueda inline ──────────────────────────────────────────────
    empresas = sorted(df_all["id_empresa"].dropna().unique())

    with st.container(border=True):
        st.markdown("#### 🔎 Seleccionar empresa")
        col_sel, col_n = st.columns([3, 1])
        with col_sel:
            id_sel = st.selectbox(
                "ID de empresa:",
                empresas,
                index=0,
                label_visibility="collapsed",
            )
        with col_n:
            st.metric("Total empresas disponibles", f"{len(empresas):,}")

    df_vista = df_all[df_all["id_empresa"] == id_sel].copy()
    df_emp = df_vista.sort_values("anio")

    if df_emp.empty:
        st.warning("Sin datos para esta empresa.")
        st.stop()

    sector  = df_emp["nombre_sector"].iloc[0]
    tamanio = df_emp["tamanio_empresa"].iloc[-1]
    anio_ini = df_emp["anio"].min()
    anio_fin = df_emp["anio"].max()
    n_anios  = df_emp["anio"].nunique()

    # ── Tarjeta de identidad ──────────────────────────────────────────────────
    col_info, col_badge = st.columns([4, 1])
    with col_info:
        st.subheader(f"🏷️ Empresa ID-{id_sel}")
        st.markdown(
            f"**Sector:** {sector.title()}  \n"
            f"**Tamaño:** {tamanio}  \n"
            f"**Período:** {anio_ini} – {anio_fin} ({n_anios} año{'s' if n_anios != 1 else ''})  \n"
            f"**Empleados promedio:** {df_emp['personal_ocupado_total'].mean():,.0f}"
        )
    with col_badge:
        ratio_eco = df_emp["ratio_eco_ingreso"].mean()
        if ratio_eco >= 1:
            st.success(f"🌿 Ratio eco\n**{ratio_eco:.2f}%**")
        elif ratio_eco >= 0.1:
            st.info(f"🌱 Ratio eco\n**{ratio_eco:.2f}%**")
        else:
            st.warning(f"⚠️ Ratio eco\n**{ratio_eco:.3f}%**")

    st.divider()

    # ── KPIs ──────────────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("💰 Ingresos (media)", f"${df_emp['total_ingresos'].mean()/1e6:,.1f}M",
              delta=f"${(df_emp['total_ingresos'].iloc[-1]-df_emp['total_ingresos'].iloc[0])/1e6:+,.1f}M vs inicio"
              if len(df_emp) > 1 else None)
    c2.metric("📉 Gastos (media)", f"${df_emp['gastos_totales'].mean()/1e6:,.1f}M")
    c3.metric("🌱 Inv. Ambiental", f"${df_emp['gasto_gestion_amb'].mean()/1e3:,.1f}K",
              delta=f"{(df_emp['gasto_gestion_amb'].iloc[-1]-df_emp['gasto_gestion_amb'].iloc[0])/1e3:+,.1f}K vs inicio"
              if len(df_emp) > 1 else None)
    c4.metric("👥 Empleados (media)", f"{df_emp['personal_ocupado_total'].mean():,.0f}")
    c5.metric("💚 Eco/empleado",      f"${df_emp['eco_per_capita'].mean():,.0f}")

    st.divider()

    # ── Pestañas analíticas ───────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Evolución Financiera", "🌿 Perfil Ambiental", "📈 Ecoeficiencia", "🗄️ Datos Completos"])

    with tab1:
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            df_fin = df_emp[["anio","total_ingresos","gastos_totales"]].melt(id_vars="anio")
            df_fin["variable"] = df_fin["variable"].map({"total_ingresos":"Ingresos","gastos_totales":"Gastos"})
            fig = px.bar(df_fin, x="anio", y="value", color="variable", barmode="group",
                         title="💰 Ingresos vs Gastos por Año",
                         labels={"value":"Monto ($)","anio":"Año","variable":"Concepto"},
                         color_discrete_sequence=["#3b82f6","#ef4444"])
            fig.update_layout(xaxis=dict(tickmode="linear", dtick=1), legend_title_text="")
            st.plotly_chart(fig, use_container_width=True)
        with col_g2:
            fig2 = px.line(df_emp, x="anio", y="intensidad_gasto",
                           title="📉 Intensidad del Gasto (Gastos/Ingresos %)",
                           labels={"intensidad_gasto":"Intensidad (%)","anio":"Año"},
                           markers=True, color_discrete_sequence=["#f59e0b"])
            fig2.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="Punto de equilibrio")
            fig2.update_layout(xaxis=dict(tickmode="linear", dtick=1))
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        col_r1, col_r2 = st.columns([1,1])
        with col_r1:
            inv_cols_presentes = {k: v for k, v in {
                "Emisiones aire": "realiza_inv_red_emision_aire",
                "Ruido/Vibración": "realiza_inv_evita_ruido_vibra",
                "Energía limpia": "realiza_inv_energia_limp",
                "Ahorro agua": "realiza_inv_ahorro_agua",
                "Medición agua": "realiza_inv_inst_med_agua",
                "Prot. suelo": "realiza_inv_protec_suelo",
                "Desechos": "realiza_inv_disp_desechos",
            }.items() if v in df_emp.columns}
            if inv_cols_presentes:
                dr = pd.DataFrame({"area": list(inv_cols_presentes.keys()),
                                   "frecuencia": [df_emp[c].sum() for c in inv_cols_presentes.values()]})
                fig3 = go.Figure(data=go.Scatterpolar(r=dr["frecuencia"], theta=dr["area"],
                                                       fill="toself", marker_color="#10b981"))
                fig3.update_layout(title="🌿 Áreas de Inversión Ambiental (años activos)",
                                   polar=dict(radialaxis=dict(visible=True, range=[0, n_anios])),
                                   showlegend=False)
                st.plotly_chart(fig3, use_container_width=True)
        with col_r2:
            fig4 = px.area(df_emp, x="anio", y="gasto_gestion_amb",
                           title="🌱 Gasto en Gestión Ambiental por Año",
                           labels={"gasto_gestion_amb":"Gasto ($)","anio":"Año"},
                           color_discrete_sequence=["#10b981"])
            fig4.update_layout(xaxis=dict(tickmode="linear", dtick=1))
            st.plotly_chart(fig4, use_container_width=True)
        if inv_cols_presentes:
            activas   = [k for k, v in inv_cols_presentes.items() if df_emp[v].sum() > 0]
            inactivas = [k for k, v in inv_cols_presentes.items() if df_emp[v].sum() == 0]
            if activas:   st.success(f"✅ **Invirtió en:** {', '.join(activas)}")
            if inactivas: st.error(f"❌ **Sin inversión en:** {', '.join(inactivas)}")

    with tab3:
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            fig5 = px.line(df_emp, x="anio", y="ratio_eco_ingreso",
                           title="📊 Ratio Eco-eficiencia vs Mediana Sectorial",
                           labels={"ratio_eco_ingreso":"Ratio (%)","anio":"Año"},
                           markers=True, color_discrete_sequence=["#8b5cf6"])
            bench = df_all[df_all["nombre_sector"] == sector].groupby("anio")["ratio_eco_ingreso"].median()
            fig5.add_scatter(x=bench.index, y=bench.values, mode="lines",
                             name=f"Mediana {sector.title()}", line=dict(dash="dash", color="#f97316"))
            fig5.update_layout(xaxis=dict(tickmode="linear", dtick=1))
            st.plotly_chart(fig5, use_container_width=True)
        with col_e2:
            fig6 = px.bar(df_emp, x="anio", y="eco_per_capita",
                          title="👤 Inversión Ambiental por Empleado ($)",
                          labels={"eco_per_capita":"$ por empleado","anio":"Año"},
                          color_discrete_sequence=["#06b6d4"])
            fig6.update_layout(xaxis=dict(tickmode="linear", dtick=1))
            st.plotly_chart(fig6, use_container_width=True)
        st.markdown("#### 📋 Indicadores por año")
        df_eco_tabla = df_emp[["anio","ratio_eco_ingreso","eco_per_capita","intensidad_gasto"]].copy()
        df_eco_tabla.columns = ["Año","Ratio eco/ingreso (%)","Eco por empleado ($)","Intensidad gasto (%)"]
        st.dataframe(df_eco_tabla.style.format({"Ratio eco/ingreso (%)":"{:.4f}",
                                                 "Eco por empleado ($)":"{:,.0f}",
                                                 "Intensidad gasto (%)":"{:.1f}"}),
                     use_container_width=True, hide_index=True)

    with tab4:
        cols_export = [c for c in ["anio","total_ingresos","gastos_totales","gasto_gestion_amb",
                                    "personal_ocupado_total","ratio_eco_ingreso","eco_per_capita",
                                    "intensidad_gasto","tamanio_empresa"] if c in df_emp.columns]
        ds_export = df_emp[cols_export]
        st.dataframe(ds_export, use_container_width=True, hide_index=True)
        st.download_button("⬇️ Descargar datos empresa",
                           ds_export.to_csv(index=False).encode("utf-8"),
                           f"empresa_{id_sel}.csv", "text/csv")


# ═══════════════════════════════════════════════════════════════════════════════
# MODO B — POR FILTROS (panel inline en la parte superior)
# ═══════════════════════════════════════════════════════════════════════════════
else:
    anios    = sorted(df_all["anio"].unique())
    sectores = sorted(df_all["nombre_sector"].dropna().unique())
    tamanios = ["Microempresa", "Pequeña", "Mediana", "Grande"]
    _inv_cols = {
        "Emisiones de aire": "realiza_inv_red_emision_aire",
        "Ruido/Vibración":   "realiza_inv_evita_ruido_vibra",
        "Energía limpia":    "realiza_inv_energia_limp",
        "Ahorro de agua":    "realiza_inv_ahorro_agua",
        "Medición agua":     "realiza_inv_inst_med_agua",
        "Protección suelo":  "realiza_inv_protec_suelo",
        "Disposición desechos": "realiza_inv_disp_desechos",
    }
    inv_existentes = {k: v for k, v in _inv_cols.items() if v in df_all.columns}

    # ── Panel de filtros inline ───────────────────────────────────────────────
    with st.container(border=True):
        st.markdown("#### 🔎 Filtros de búsqueda")

        # Fila 1: Año | Sector | Tamaño
        fc1, fc2, fc3 = st.columns([1, 2, 2])
        with fc1:
            rango_anio = st.select_slider(
                "📅 Rango de años",
                options=anios,
                value=(min(anios), max(anios)),
            )
        with fc2:
            sect_sel = st.multiselect(
                "🏭 Sector(es)",
                options=sectores,
                default=[],
                placeholder="Todos los sectores",
            )
        with fc3:
            tam_sel = st.multiselect(
                "📏 Tamaño de empresa",
                options=tamanios,
                default=[],
                placeholder="Todos los tamaños",
            )

        # Fila 2: Áreas de inversión ambiental (checkboxes en columnas)
        st.markdown("**🌿 Filtrar por área de inversión ambiental** *(marca las que debe cumplir la empresa)*")
        inv_cols_list = list(inv_existentes.items())
        n_inv = len(inv_cols_list)
        inv_cols_ui = st.columns(n_inv)
        inv_sel = {}
        for i, (label, col) in enumerate(inv_cols_list):
            inv_sel[col] = inv_cols_ui[i].checkbox(label, value=False, key=f"inv_{col}")

    # ── Aplicar filtros ───────────────────────────────────────────────────────
    mask = (df_all["anio"] >= rango_anio[0]) & (df_all["anio"] <= rango_anio[1])
    if sect_sel:
        mask &= df_all["nombre_sector"].isin(sect_sel)
    if tam_sel:
        mask &= df_all["tamanio_empresa"].isin(tam_sel)
    for col, activo in inv_sel.items():
        if activo:
            mask &= df_all[col] == 1

    df_vista = df_all[mask].copy()

    if df_vista.empty:
        st.warning("⚠️ No hay datos con los filtros seleccionados. Ajusta los criterios.")
        st.stop()

    # ── Banner de resultados ──────────────────────────────────────────────────
    n_empresas = df_vista["id_empresa"].nunique()
    n_anios_v  = df_vista["anio"].nunique()
    st.info(f"📊 Mostrando **{n_empresas:,} empresas** | **{len(df_vista):,} registros** | **{n_anios_v} año(s)**")

    # ── KPIs agregados ────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("💰 Ingresos Totales",      f"${df_vista['total_ingresos'].sum()/1e9:,.2f}B")
    c2.metric("📉 Gastos Totales",         f"${df_vista['gastos_totales'].sum()/1e9:,.2f}B")
    c3.metric("🌱 Inv. Ambiental Total",  f"${df_vista['gasto_gestion_amb'].sum()/1e6:,.1f}M")
    c4.metric("👥 Empleados (media)",     f"{df_vista['personal_ocupado_total'].mean():,.0f}")
    c5.metric("🏢 Empresas",              f"{n_empresas:,}")

    st.divider()

    # ── Pestañas ──────────────────────────────────────────────────────────────
    tab_a, tab_b, tab_c, tab_d = st.tabs([
        "📊 Distribución Financiera",
        "🌿 Inversión Ambiental",
        "📈 Ecoeficiencia Comparativa",
        "🗄️ Listado de Empresas",
    ])

    with tab_a:
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            agg = df_vista.groupby("anio")[["total_ingresos","gastos_totales"]].sum().reset_index()
            df_agg = agg.melt(id_vars="anio")
            df_agg["variable"] = df_agg["variable"].map({"total_ingresos":"Ingresos","gastos_totales":"Gastos"})
            fig = px.bar(df_agg, x="anio", y="value", color="variable", barmode="group",
                         title="💰 Ingresos vs Gastos agregados por Año",
                         labels={"value":"Monto ($)","anio":"Año","variable":"Concepto"},
                         color_discrete_sequence=["#3b82f6","#ef4444"])
            fig.update_layout(xaxis=dict(tickmode="linear", dtick=1))
            st.plotly_chart(fig, use_container_width=True)
        with col_a2:
            if "nombre_sector" in df_vista.columns:
                agg_s = df_vista.groupby("nombre_sector")["total_ingresos"].sum().reset_index()
                agg_s.columns = ["Sector","Ingresos"]
                agg_s["Sector"] = agg_s["Sector"].str.title()
                fig2 = px.pie(agg_s, names="Sector", values="Ingresos",
                              title="🏭 Participación de Ingresos por Sector",
                              color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig2, use_container_width=True)
        if "tamanio_empresa" in df_vista.columns:
            orden_tam = ["Microempresa","Pequeña","Mediana","Grande"]
            fig3 = px.box(df_vista[df_vista["tamanio_empresa"].isin(orden_tam)],
                          x="tamanio_empresa", y="total_ingresos",
                          category_orders={"tamanio_empresa": orden_tam},
                          title="📏 Distribución de Ingresos por Tamaño",
                          labels={"total_ingresos":"Ingresos ($)","tamanio_empresa":"Tamaño"},
                          color="tamanio_empresa",
                          color_discrete_sequence=["#6366f1","#3b82f6","#10b981","#f59e0b"])
            st.plotly_chart(fig3, use_container_width=True)

    with tab_b:
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            agg_amb = df_vista.groupby("anio")["gasto_gestion_amb"].sum().reset_index()
            fig4 = px.area(agg_amb, x="anio", y="gasto_gestion_amb",
                           title="🌱 Evolución Inversión Ambiental Agregada",
                           labels={"gasto_gestion_amb":"Gasto ($)","anio":"Año"},
                           color_discrete_sequence=["#10b981"])
            fig4.update_layout(xaxis=dict(tickmode="linear", dtick=1))
            st.plotly_chart(fig4, use_container_width=True)
        with col_b2:
            inv_f = {k: v for k, v in {
                "Emisiones aire": "realiza_inv_red_emision_aire",
                "Ruido/Vibración": "realiza_inv_evita_ruido_vibra",
                "Energía limpia": "realiza_inv_energia_limp",
                "Ahorro agua": "realiza_inv_ahorro_agua",
                "Medición agua": "realiza_inv_inst_med_agua",
                "Prot. suelo": "realiza_inv_protec_suelo",
                "Desechos": "realiza_inv_disp_desechos",
            }.items() if v in df_vista.columns}
            if inv_f:
                df_cont = pd.DataFrame({"Área": list(inv_f.keys()),
                                        "Empresas": [df_vista[v].sum() for v in inv_f.values()]})
                df_cont = df_cont.sort_values("Empresas", ascending=True)
                fig5 = px.bar(df_cont, y="Área", x="Empresas", orientation="h",
                              title="🌿 Empresas que invierten por área ambiental",
                              color_discrete_sequence=["#10b981"])
                st.plotly_chart(fig5, use_container_width=True)

    with tab_c:
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            agg_eco = df_vista.groupby("anio")["ratio_eco_ingreso"].median().reset_index()
            fig6 = px.line(agg_eco, x="anio", y="ratio_eco_ingreso", markers=True,
                           title="📊 Ratio Eco-eficiencia mediano por Año",
                           labels={"ratio_eco_ingreso":"Ratio (%)","anio":"Año"},
                           color_discrete_sequence=["#8b5cf6"])
            fig6.update_layout(xaxis=dict(tickmode="linear", dtick=1))
            st.plotly_chart(fig6, use_container_width=True)
        with col_c2:
            if "nombre_sector" in df_vista.columns:
                agg_se = df_vista.groupby("nombre_sector")["ratio_eco_ingreso"].median().reset_index()
                agg_se.columns = ["Sector","Ratio eco (%)"]
                agg_se["Sector"] = agg_se["Sector"].str.title()
                agg_se = agg_se.sort_values("Ratio eco (%)", ascending=True)
                fig7 = px.bar(agg_se, y="Sector", x="Ratio eco (%)", orientation="h",
                              title="🏭 Ratio Eco-eficiencia por Sector",
                              color="Ratio eco (%)", color_continuous_scale="Greens")
                st.plotly_chart(fig7, use_container_width=True)
        fig8 = px.scatter(
            df_vista.sample(min(2000, len(df_vista)), random_state=42),
            x="total_ingresos", y="gasto_gestion_amb",
            color="nombre_sector" if "nombre_sector" in df_vista.columns else None,
            size="personal_ocupado_total", hover_data=["id_empresa","anio"],
            title="🔵 Ingreso vs Inversión Ambiental (muestra representativa)",
            labels={"total_ingresos":"Ingresos ($)","gasto_gestion_amb":"Gasto ambiental ($)",
                    "nombre_sector":"Sector"}, opacity=0.7)
        st.plotly_chart(fig8, use_container_width=True)

    with tab_d:
        resumen_emp = (
            df_vista.groupby("id_empresa")
            .agg(Sector=("nombre_sector","first"), Tamanio=("tamanio_empresa","last"),
                 Años=("anio","nunique"), Ingresos=("total_ingresos","mean"),
                 Gastos=("gastos_totales","mean"), Inv_amb=("gasto_gestion_amb","mean"),
                 Ratio_eco=("ratio_eco_ingreso","mean"), Empleados=("personal_ocupado_total","mean"))
            .reset_index()
        )
        resumen_emp.columns = ["ID Empresa","Sector","Tamaño","Años",
                                "Ingresos Prom ($)","Gastos Prom ($)",
                                "Inv. Ambiental Prom ($)","Ratio Eco (%)","Empleados Prom"]
        resumen_emp["Sector"] = resumen_emp["Sector"].str.title()
        st.dataframe(
            resumen_emp.style.format({"Ingresos Prom ($)":"{:,.0f}","Gastos Prom ($)":"{:,.0f}",
                                       "Inv. Ambiental Prom ($)":"{:,.0f}",
                                       "Ratio Eco (%)":"{:.4f}","Empleados Prom":"{:,.0f}"}),
            use_container_width=True, hide_index=True)
        st.download_button("⬇️ Descargar listado",
                           resumen_emp.to_csv(index=False).encode("utf-8"),
                           "empresas_filtradas.csv", "text/csv")

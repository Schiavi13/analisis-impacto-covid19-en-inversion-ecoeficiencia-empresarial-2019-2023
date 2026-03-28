"""Página 3 — Buscador Empresarial con perfil completo y filtros avanzados."""
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

st.header("🏢 Módulo Empresarial")
st.caption("Perfil financiero, ambiental y operativo por empresa · Filtros avanzados disponibles en el panel lateral.")

# ─────────────────────── DATOS ────────────────────────────────────────────────
df_raw = cargar_datos()
if df_raw.empty:
    st.warning("Datos no disponibles.")
    st.stop()

# Calcular métricas derivadas una sola vez
df_all = calcular_ratios_ecoeficiencia(df_raw)
df_all = clasificar_tamanio_empresa(df_all)

# ─────────────────────── SIDEBAR — FILTROS ───────────────────────────────────
with st.sidebar:
    st.markdown("### 🔎 Filtros de búsqueda")
    st.divider()

    # 1. Modo de búsqueda
    modo = st.radio(
        "Modo de consulta",
        ["Por ID de empresa", "Por filtros"],
        index=0,
        horizontal=True,
    )
    st.divider()

    if modo == "Por ID de empresa":
        empresas = sorted(df_all["id_empresa"].dropna().unique())
        id_sel = st.selectbox("🏷️ ID Empresa:", empresas, index=0)
        df_vista = df_all[df_all["id_empresa"] == id_sel].copy()

    else:
        # Filtros combinados
        # Año
        anios = sorted(df_all["anio"].unique())
        rango_anio = st.select_slider(
            "📅 Rango de años:",
            options=anios,
            value=(min(anios), max(anios)),
        )

        # Sector
        sectores = sorted(df_all["nombre_sector"].dropna().unique())
        sect_sel = st.multiselect(
            "🏭 Sector(es):",
            options=sectores,
            default=[],
            placeholder="Todos los sectores",
        )

        # Tamaño de empresa
        tamanios = ["Microempresa", "Pequeña", "Mediana", "Grande"]
        tam_sel = st.multiselect(
            "📏 Tamaño (empleados):",
            options=tamanios,
            default=[],
            placeholder="Todos los tamaños",
        )

        # Áreas de inversión ambiental
        st.markdown("**🌿 Áreas de inversión ambiental:**")
        _inv_cols = {
            "Emisiones de aire": "realiza_inv_red_emision_aire",
            "Ruido/Vibración": "realiza_inv_evita_ruido_vibra",
            "Energía limpia": "realiza_inv_energia_limp",
            "Ahorro de agua": "realiza_inv_ahorro_agua",
            "Medición agua": "realiza_inv_inst_med_agua",
            "Protección suelo": "realiza_inv_protec_suelo",
            "Disposición desechos": "realiza_inv_disp_desechos",
        }
        inv_existentes = {k: v for k, v in _inv_cols.items() if v in df_all.columns}
        inv_sel = {}
        for label, col in inv_existentes.items():
            inv_sel[col] = st.checkbox(label, value=False)

        # Aplicar filtros
        mask = (
            (df_all["anio"] >= rango_anio[0]) &
            (df_all["anio"] <= rango_anio[1])
        )
        if sect_sel:
            mask &= df_all["nombre_sector"].isin(sect_sel)
        if tam_sel:
            mask &= df_all["tamanio_empresa"].isin(tam_sel)
        for col, activo in inv_sel.items():
            if activo:
                mask &= df_all[col] == 1

        df_vista = df_all[mask].copy()
        id_sel = None

    st.divider()
    n_sel = df_vista["id_empresa"].nunique() if not df_vista.empty else 0
    st.caption(f"📊 **{n_sel:,}** empresa(s) seleccionada(s)")

# ─────────────────────── VALIDACIÓN ──────────────────────────────────────────
if df_vista.empty:
    st.warning("⚠️ No hay datos con los filtros seleccionados. Ajusta los criterios en el panel lateral.")
    st.stop()

# ─────────────────────── PERFIL DE EMPRESA (modo ID) ─────────────────────────
if modo == "Por ID de empresa":
    df_emp = df_vista.sort_values("anio")
    sector = df_emp["nombre_sector"].iloc[0] if not df_emp.empty else "—"
    tamanio = df_emp["tamanio_empresa"].iloc[-1]
    anio_ini = df_emp["anio"].min()
    anio_fin = df_emp["anio"].max()
    n_anios = df_emp["anio"].nunique()

    # ── Tarjeta de identificación ──────────────────────────────────────────
    col_info, col_eco = st.columns([3, 1])
    with col_info:
        st.subheader(f"🏷️ Empresa ID-{id_sel}")
        st.markdown(
            f"**Sector:** {sector.title()}  \n"
            f"**Tamaño:** {tamanio}  \n"
            f"**Período cubierto:** {anio_ini} – {anio_fin} ({n_anios} año{'s' if n_anios != 1 else ''})  \n"
            f"**Promedio empleados:** {df_emp['personal_ocupado_total'].mean():,.0f}"
        )
    with col_eco:
        ratio_eco = df_emp["ratio_eco_ingreso"].mean()
        if ratio_eco >= 1:
            st.success(f"🌿 Ratio eco\n**{ratio_eco:.2f}%**")
        elif ratio_eco >= 0.1:
            st.info(f"🌱 Ratio eco\n**{ratio_eco:.2f}%**")
        else:
            st.warning(f"⚠️ Ratio eco\n**{ratio_eco:.3f}%**")

    st.divider()

    # ── KPIs financieros y ambientales ────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric(
        "💰 Ingresos (media)",
        f"${df_emp['total_ingresos'].mean()/1e6:,.1f}M",
        delta=f"${(df_emp['total_ingresos'].iloc[-1] - df_emp['total_ingresos'].iloc[0])/1e6:+,.1f}M vs inicio"
        if len(df_emp) > 1 else None,
    )
    c2.metric(
        "📉 Gastos (media)",
        f"${df_emp['gastos_totales'].mean()/1e6:,.1f}M",
    )
    c3.metric(
        "🌱 Inv. Ambiental",
        f"${df_emp['gasto_gestion_amb'].mean()/1e3:,.1f}K",
        delta=f"{(df_emp['gasto_gestion_amb'].iloc[-1] - df_emp['gasto_gestion_amb'].iloc[0])/1e3:+,.1f}K vs inicio"
        if len(df_emp) > 1 else None,
    )
    c4.metric(
        "👥 Empleados (media)",
        f"{df_emp['personal_ocupado_total'].mean():,.0f}",
    )
    c5.metric(
        "💚 Eco/empleado",
        f"${df_emp['eco_per_capita'].mean():,.0f}",
    )

    st.divider()

    # ── Pestañas de análisis ───────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Evolución Financiera", "🌿 Perfil Ambiental", "📈 Ecoeficiencia", "🗄️ Datos Completos"]
    )

    # TAB 1 — Evolución Financiera
    with tab1:
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            df_fin = df_emp[["anio", "total_ingresos", "gastos_totales"]].melt(id_vars="anio")
            df_fin["variable"] = df_fin["variable"].map(
                {"total_ingresos": "Ingresos", "gastos_totales": "Gastos"}
            )
            fig = px.bar(
                df_fin, x="anio", y="value", color="variable", barmode="group",
                title="💰 Ingresos vs Gastos por Año",
                labels={"value": "Monto ($)", "anio": "Año", "variable": "Concepto"},
                color_discrete_sequence=["#3b82f6", "#ef4444"],
            )
            fig.update_layout(xaxis=dict(tickmode="linear", dtick=1), legend_title_text="")
            st.plotly_chart(fig, use_container_width=True)

        with col_g2:
            fig2 = px.line(
                df_emp, x="anio", y="intensidad_gasto",
                title="📉 Intensidad del Gasto (Gastos/Ingresos %)",
                labels={"intensidad_gasto": "Intensidad (%)", "anio": "Año"},
                markers=True, color_discrete_sequence=["#f59e0b"],
            )
            fig2.add_hline(y=100, line_dash="dash", line_color="red",
                           annotation_text="Punto de equilibrio")
            fig2.update_layout(xaxis=dict(tickmode="linear", dtick=1))
            st.plotly_chart(fig2, use_container_width=True)

    # TAB 2 — Perfil Ambiental
    with tab2:
        col_r1, col_r2 = st.columns([1, 1])

        with col_r1:
            # Radar de tipos de inversión ambiental
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
                dr = pd.DataFrame({
                    "area": list(inv_cols_presentes.keys()),
                    "frecuencia": [df_emp[c].sum() for c in inv_cols_presentes.values()],
                })
                fig3 = go.Figure(data=go.Scatterpolar(
                    r=dr["frecuencia"], theta=dr["area"], fill="toself",
                    marker_color="#10b981", name="Inversión ambiental",
                ))
                fig3.update_layout(
                    title="🌿 Áreas de Inversión Ambiental (años activos)",
                    polar=dict(radialaxis=dict(visible=True, range=[0, n_anios])),
                    showlegend=False,
                )
                st.plotly_chart(fig3, use_container_width=True)

        with col_r2:
            # Gasto ambiental por año
            fig4 = px.area(
                df_emp, x="anio", y="gasto_gestion_amb",
                title="🌱 Gasto en Gestión Ambiental por Año",
                labels={"gasto_gestion_amb": "Gasto ($)", "anio": "Año"},
                color_discrete_sequence=["#10b981"],
            )
            fig4.update_layout(xaxis=dict(tickmode="linear", dtick=1))
            st.plotly_chart(fig4, use_container_width=True)

        # Resumen textual de áreas activas
        if inv_cols_presentes:
            activas = [k for k, v in inv_cols_presentes.items() if df_emp[v].sum() > 0]
            inactivas = [k for k, v in inv_cols_presentes.items() if df_emp[v].sum() == 0]
            if activas:
                st.success(f"✅ **Áreas donde invirtió:** {', '.join(activas)}")
            if inactivas:
                st.error(f"❌ **Sin inversión registrada en:** {', '.join(inactivas)}")

    # TAB 3 — Ecoeficiencia
    with tab3:
        col_e1, col_e2 = st.columns(2)

        with col_e1:
            fig5 = px.line(
                df_emp, x="anio", y="ratio_eco_ingreso",
                title="📊 Ratio Eco-eficiencia (Gasto Ambiental / Ingreso %)",
                labels={"ratio_eco_ingreso": "Ratio (%)", "anio": "Año"},
                markers=True, color_discrete_sequence=["#8b5cf6"],
            )
            fig5.update_layout(xaxis=dict(tickmode="linear", dtick=1))
            # Benchmark sectorial
            bench = df_all[df_all["nombre_sector"] == sector].groupby("anio")["ratio_eco_ingreso"].median()
            fig5.add_scatter(
                x=bench.index, y=bench.values,
                mode="lines", name=f"Mediana {sector.title()}",
                line=dict(dash="dash", color="#f97316"),
            )
            st.plotly_chart(fig5, use_container_width=True)

        with col_e2:
            fig6 = px.bar(
                df_emp, x="anio", y="eco_per_capita",
                title="👤 Inversión Ambiental por Empleado ($)",
                labels={"eco_per_capita": "$ por empleado", "anio": "Año"},
                color_discrete_sequence=["#06b6d4"],
            )
            fig6.update_layout(xaxis=dict(tickmode="linear", dtick=1))
            st.plotly_chart(fig6, use_container_width=True)

        # Tabla de indicadores de ecoeficiencia
        st.markdown("#### 📋 Indicadores de ecoeficiencia por año")
        cols_eco_tabla = ["anio", "ratio_eco_ingreso", "eco_per_capita", "intensidad_gasto"]
        df_eco_tabla = df_emp[cols_eco_tabla].copy()
        df_eco_tabla.columns = ["Año", "Ratio eco/ingreso (%)", "Eco por empleado ($)", "Intensidad gasto (%)"]
        st.dataframe(
            df_eco_tabla.style.format({
                "Ratio eco/ingreso (%)": "{:.4f}",
                "Eco por empleado ($)": "{:,.0f}",
                "Intensidad gasto (%)": "{:.1f}",
            }),
            use_container_width=True,
            hide_index=True,
        )

    # TAB 4 — Datos completos
    with tab4:
        cols_export = [
            "anio", "total_ingresos", "gastos_totales", "gasto_gestion_amb",
            "personal_ocupado_total", "ratio_eco_ingreso", "eco_per_capita",
            "intensidad_gasto", "tamanio_empresa",
        ]
        cols_export = [c for c in cols_export if c in df_emp.columns]
        ds_export = df_emp[cols_export]
        st.dataframe(ds_export, use_container_width=True, hide_index=True)
        csv_emp = ds_export.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Descargar datos empresa",
            csv_emp, f"empresa_{id_sel}.csv", "text/csv",
        )

# ─────────────────────── MODO FILTROS — VISTA MULTIVARIADA ────────────────────
else:
    n_empresas = df_vista["id_empresa"].nunique()
    n_anios_v = df_vista["anio"].nunique()
    st.info(
        f"📊 Mostrando **{n_empresas:,} empresas** | "
        f"**{len(df_vista):,} registros** | "
        f"**{n_anios_v} año(s)** con los filtros seleccionados"
    )
    st.divider()

    # ── KPIs agregados del conjunto filtrado ──────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("💰 Ingresos Totales", f"${df_vista['total_ingresos'].sum()/1e9:,.2f}B")
    c2.metric("📉 Gastos Totales", f"${df_vista['gastos_totales'].sum()/1e9:,.2f}B")
    c3.metric("🌱 Inv. Ambiental Total", f"${df_vista['gasto_gestion_amb'].sum()/1e6:,.1f}M")
    c4.metric("👥 Empleados (media)", f"{df_vista['personal_ocupado_total'].mean():,.0f}")
    c5.metric("🏢 Empresas", f"{n_empresas:,}")

    st.divider()

    tab_a, tab_b, tab_c, tab_d = st.tabs([
        "📊 Distribución Financiera",
        "🌿 Inversión Ambiental",
        "📈 Ecoeficiencia Comparativa",
        "🗄️ Listado de Empresas",
    ])

    # TAB A — Distribución financiera
    with tab_a:
        col_a1, col_a2 = st.columns(2)

        with col_a1:
            agg_anio = df_vista.groupby("anio")[["total_ingresos", "gastos_totales"]].sum().reset_index()
            df_agg = agg_anio.melt(id_vars="anio")
            df_agg["variable"] = df_agg["variable"].map({"total_ingresos": "Ingresos", "gastos_totales": "Gastos"})
            fig = px.bar(df_agg, x="anio", y="value", color="variable", barmode="group",
                         title="💰 Ingresos vs Gastos agregados por Año",
                         labels={"value": "Monto ($)", "anio": "Año", "variable": "Concepto"},
                         color_discrete_sequence=["#3b82f6", "#ef4444"])
            fig.update_layout(xaxis=dict(tickmode="linear", dtick=1))
            st.plotly_chart(fig, use_container_width=True)

        with col_a2:
            if "nombre_sector" in df_vista.columns:
                agg_sect = df_vista.groupby("nombre_sector")["total_ingresos"].sum().reset_index()
                agg_sect.columns = ["Sector", "Ingresos"]
                agg_sect["Sector"] = agg_sect["Sector"].str.title()
                fig2 = px.pie(agg_sect, names="Sector", values="Ingresos",
                              title="🏭 Participación de Ingresos por Sector",
                              color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig2, use_container_width=True)

        # Boxplot por tamaño
        if "tamanio_empresa" in df_vista.columns:
            orden_tam = ["Microempresa", "Pequeña", "Mediana", "Grande"]
            fig3 = px.box(
                df_vista[df_vista["tamanio_empresa"].isin(orden_tam)],
                x="tamanio_empresa", y="total_ingresos",
                category_orders={"tamanio_empresa": orden_tam},
                title="📏 Distribución de Ingresos por Tamaño de Empresa",
                labels={"total_ingresos": "Ingresos ($)", "tamanio_empresa": "Tamaño"},
                color="tamanio_empresa",
                color_discrete_sequence=["#6366f1", "#3b82f6", "#10b981", "#f59e0b"],
            )
            st.plotly_chart(fig3, use_container_width=True)

    # TAB B — Inversión ambiental
    with tab_b:
        col_b1, col_b2 = st.columns(2)

        with col_b1:
            agg_amb = df_vista.groupby("anio")["gasto_gestion_amb"].sum().reset_index()
            fig4 = px.area(agg_amb, x="anio", y="gasto_gestion_amb",
                           title="🌱 Evolución de la Inversión Ambiental Agregada",
                           labels={"gasto_gestion_amb": "Gasto ($)", "anio": "Año"},
                           color_discrete_sequence=["#10b981"])
            fig4.update_layout(xaxis=dict(tickmode="linear", dtick=1))
            st.plotly_chart(fig4, use_container_width=True)

        with col_b2:
            inv_cols_filtro = {
                "Emisiones aire": "realiza_inv_red_emision_aire",
                "Ruido/Vibración": "realiza_inv_evita_ruido_vibra",
                "Energía limpia": "realiza_inv_energia_limp",
                "Ahorro agua": "realiza_inv_ahorro_agua",
                "Medición agua": "realiza_inv_inst_med_agua",
                "Prot. suelo": "realiza_inv_protec_suelo",
                "Desechos": "realiza_inv_disp_desechos",
            }
            inv_existentes_f = {k: v for k, v in inv_cols_filtro.items() if v in df_vista.columns}
            if inv_existentes_f:
                conteos = {k: df_vista[v].sum() for k, v in inv_existentes_f.items()}
                df_cont = pd.DataFrame(list(conteos.items()), columns=["Área", "Empresas que invierten"])
                df_cont = df_cont.sort_values("Empresas que invierten", ascending=True)
                fig5 = px.bar(df_cont, y="Área", x="Empresas que invierten", orientation="h",
                              title="🌿 Nº de empresas que invierten por área ambiental",
                              color_discrete_sequence=["#10b981"])
                st.plotly_chart(fig5, use_container_width=True)

    # TAB C — Ecoeficiencia comparativa
    with tab_c:
        col_c1, col_c2 = st.columns(2)

        with col_c1:
            agg_eco = df_vista.groupby("anio")["ratio_eco_ingreso"].median().reset_index()
            fig6 = px.line(agg_eco, x="anio", y="ratio_eco_ingreso", markers=True,
                           title="📊 Ratio Eco-eficiencia mediano por Año",
                           labels={"ratio_eco_ingreso": "Ratio (%)", "anio": "Año"},
                           color_discrete_sequence=["#8b5cf6"])
            fig6.update_layout(xaxis=dict(tickmode="linear", dtick=1))
            st.plotly_chart(fig6, use_container_width=True)

        with col_c2:
            if "nombre_sector" in df_vista.columns:
                agg_sect_eco = df_vista.groupby("nombre_sector")["ratio_eco_ingreso"].median().reset_index()
                agg_sect_eco.columns = ["Sector", "Ratio eco (%)"]
                agg_sect_eco["Sector"] = agg_sect_eco["Sector"].str.title()
                agg_sect_eco = agg_sect_eco.sort_values("Ratio eco (%)", ascending=True)
                fig7 = px.bar(agg_sect_eco, y="Sector", x="Ratio eco (%)", orientation="h",
                              title="🏭 Ratio Eco-eficiencia mediano por Sector",
                              color="Ratio eco (%)",
                              color_continuous_scale="Greens")
                st.plotly_chart(fig7, use_container_width=True)

        # Scatter: ingresos vs gasto ambiental
        fig8 = px.scatter(
            df_vista.sample(min(2000, len(df_vista)), random_state=42),
            x="total_ingresos", y="gasto_gestion_amb",
            color="nombre_sector" if "nombre_sector" in df_vista.columns else None,
            size="personal_ocupado_total",
            hover_data=["id_empresa", "anio"],
            title="🔵 Ingreso vs Inversión Ambiental (muestra representativa)",
            labels={
                "total_ingresos": "Ingresos totales ($)",
                "gasto_gestion_amb": "Gasto ambiental ($)",
                "nombre_sector": "Sector",
            },
            opacity=0.7,
        )
        st.plotly_chart(fig8, use_container_width=True)

    # TAB D — Listado de empresas
    with tab_d:
        resumen_emp = (
            df_vista.groupby("id_empresa")
            .agg(
                Sector=("nombre_sector", "first"),
                Tamanio=("tamanio_empresa", "last"),
                Años=("anio", "nunique"),
                Ingresos_media=("total_ingresos", "mean"),
                Gastos_media=("gastos_totales", "mean"),
                Inv_ambiental_media=("gasto_gestion_amb", "mean"),
                Ratio_eco=("ratio_eco_ingreso", "mean"),
                Empleados_media=("personal_ocupado_total", "mean"),
            )
            .reset_index()
        )
        resumen_emp.columns = [
            "ID Empresa", "Sector", "Tamaño", "Años",
            "Ingresos Promedio ($)", "Gastos Promedio ($)",
            "Inv. Ambiental Promedio ($)", "Ratio Eco (%)", "Empleados Promedio",
        ]
        resumen_emp["Sector"] = resumen_emp["Sector"].str.title()
        st.dataframe(
            resumen_emp.style.format({
                "Ingresos Promedio ($)": "{:,.0f}",
                "Gastos Promedio ($)": "{:,.0f}",
                "Inv. Ambiental Promedio ($)": "{:,.0f}",
                "Ratio Eco (%)": "{:.4f}",
                "Empleados Promedio": "{:,.0f}",
            }),
            use_container_width=True,
            hide_index=True,
        )
        csv_filtro = resumen_emp.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Descargar listado filtrado",
            csv_filtro, "empresas_filtradas.csv", "text/csv",
        )

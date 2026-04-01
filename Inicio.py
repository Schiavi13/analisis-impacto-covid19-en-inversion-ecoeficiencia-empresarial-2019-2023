"""Página principal — Landing con resumen ejecutivo automático."""
import streamlit as st
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from components import cargar_datos, aplicar_tema
from analytics import resumen_ejecutivo

st.set_page_config(page_title="EcoAnalytics Pro", page_icon="⚡", layout="wide",
                   initial_sidebar_state="expanded")
aplicar_tema()

st.header("⚡ EcoAnalytics Dashboard")
st.caption("Ecoeficiencia Empresarial · Inteligencia de Datos · 2019-2023")
st.divider()

df = cargar_datos()
if not df.empty:
    # KPIs globales
    c1, c2, c3 = st.columns(3)
    c1.metric("💰 Inversión Acumulada", f"${df['gastos_totales'].sum() / 1e6:,.1f} M")
    c2.metric("🏢 Compañías Analizadas", f"{df['id_empresa'].nunique():,}")
    c3.metric("📈 Ingreso Promedio", f"${df['total_ingresos'].mean() / 1e6:,.1f} M")

    st.divider()

    # Resumen ejecutivo automático
    resumen = resumen_ejecutivo(df)
    if resumen:
        st.subheader(f"📋 Resumen Ejecutivo — {resumen.get('anio_reciente', '')}")

        col_r1, col_r2 = st.columns([2, 1])
        with col_r1:
            top3 = resumen.get('top3_sectores', [])
            cambio_amb = resumen.get('cambio_ambiental_pct', 0)
            ratio_eco = resumen.get('ratio_ambiental_mediano', 0)

            st.markdown(
                f"- 🏆 **Top 3 sectores** por gasto: {', '.join(s.title() for s in top3)}\n"
                f"- 🌱 **Gasto ambiental** vs año anterior: **{cambio_amb:+.1f}%**\n"
                f"- 📊 **Ratio eco/ingreso mediano:** {ratio_eco:.3f}% del ingreso total"
            )

        with col_r2:
            if cambio_amb >= 0:
                st.success(f"✅ Inversión ambiental creció {cambio_amb:+.1f}%")
            else:
                st.warning(f"⚠️ Inversión ambiental cayó {cambio_amb:.1f}%")

    st.divider()
    st.subheader("Módulos Analíticos")
    st.markdown(
        "- 🌳 **Diagnóstico** — Métricas macro por año y treemap sectorial\n"
        "- 🦠 **COVID-19** — Curva histórica de inversión ambiental\n"
        "- 🔍 **Consultor** — Riesgos y recomendaciones por periodo\n"
        "- 🏢 **Empresarial** — Perfil individual por ID de empresa\n"
        "- 🏭 **Sectorial** — Boxplots y benchmarking por sector\n"
        "- 🧬 **Data Science** — Correlaciones, distribuciones, ecoeficiencia y CAGR\n\n"
        "👈 *Utiliza el menú lateral para navegar.*"
    )
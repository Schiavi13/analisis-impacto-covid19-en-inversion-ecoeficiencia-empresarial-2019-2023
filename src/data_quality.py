"""
Módulo de validación de calidad de datos para EcoAnalytics Pro.
Se ejecuta silenciosamente al cargar datos; solo emite st.warning() si hay problemas.
"""
import pandas as pd
import streamlit as st


# Columnas mínimas que deben existir en datos_unificados.csv
COLUMNAS_REQUERIDAS = [
    'anio', 'id_empresa', 'nombre_sector',
    'total_ingresos', 'gastos_totales', 'gasto_gestion_amb',
    'personal_ocupado_total',
]

ANIOS_ESPERADOS = {2019, 2020, 2021, 2022, 2023}


def validar_datos(df: pd.DataFrame) -> dict:
    """
    Valida calidad del DataFrame cargado.

    Returns:
        dict con claves: 'ok' (bool), 'warnings' (list[str]), 'stats' (dict)
    """
    warnings: list[str] = []
    stats: dict = {}

    if df.empty:
        return {'ok': False, 'warnings': ['Dataset vacío.'], 'stats': {}}

    # 1. Columnas requeridas
    faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in df.columns]
    if faltantes:
        warnings.append(f"Columnas faltantes: {faltantes}")

    # 2. Años presentes
    anios_presentes = set(df['anio'].unique()) if 'anio' in df.columns else set()
    anios_faltantes = ANIOS_ESPERADOS - anios_presentes
    if anios_faltantes:
        warnings.append(f"Años sin datos: {sorted(anios_faltantes)}")
    stats['anios'] = sorted(anios_presentes)

    # 3. Nulos en columnas numéricas clave
    cols_num = [c for c in ['total_ingresos', 'gastos_totales', 'gasto_gestion_amb'] if c in df.columns]
    for col in cols_num:
        pct_nulo = df[col].isna().mean() * 100
        if pct_nulo > 20:
            warnings.append(f"'{col}' tiene {pct_nulo:.1f}% de nulos")
        stats[f'nulos_{col}_pct'] = round(pct_nulo, 1)

    # 4. Valores negativos en gastos/ingresos
    for col in cols_num:
        n_neg = (df[col] < 0).sum()
        if n_neg > 0:
            warnings.append(f"'{col}' tiene {n_neg} valores negativos")
        stats[f'negativos_{col}'] = int(n_neg)

    # 5. Completitud general
    stats['total_registros'] = len(df)
    stats['empresas_unicas'] = df['id_empresa'].nunique() if 'id_empresa' in df.columns else 0
    stats['sectores_unicos'] = df['nombre_sector'].nunique() if 'nombre_sector' in df.columns else 0

    return {
        'ok': len(warnings) == 0,
        'warnings': warnings,
        'stats': stats,
    }


def mostrar_alertas_calidad(df: pd.DataFrame) -> None:
    """
    Muestra st.warning() en Streamlit si hay problemas de calidad.
    Silencioso si todo está OK.
    """
    resultado = validar_datos(df)
    for w in resultado['warnings']:
        st.warning(f"⚠️ Calidad de datos: {w}")

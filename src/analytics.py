"""
Módulo de funciones analíticas reutilizables para EcoAnalytics Pro.
Contiene: indicadores de ecoeficiencia, CAGR, segmentación por tamaño,
distribuciones y autodiagnóstico basado en datos reales.
"""
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------------
# 1. INDICADORES DE ECOEFICIENCIA
# ---------------------------------------------------------------------------

def calcular_ratios_ecoeficiencia(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula indicadores de ecoeficiencia por empresa-año.

    Indicadores generados:
    - ratio_eco_ingreso: % del ingreso destinado a gestión ambiental
    - eco_per_capita: gasto ambiental por empleado ($)
    - intensidad_gasto: gastos totales / ingresos totales (eficiencia operativa)

    Returns:
        DataFrame original con 3 columnas adicionales.
    """
    df = df.copy()

    # Ratio eco / ingreso (%)
    df['ratio_eco_ingreso'] = np.where(
        df['total_ingresos'] > 0,
        df['gasto_gestion_amb'] / df['total_ingresos'] * 100,
        np.nan
    )

    # Inversión ambiental por empleado
    df['eco_per_capita'] = np.where(
        df['personal_ocupado_total'] > 0,
        df['gasto_gestion_amb'] / df['personal_ocupado_total'],
        np.nan
    )

    # Intensidad del gasto operativo
    df['intensidad_gasto'] = np.where(
        df['total_ingresos'] > 0,
        df['gastos_totales'] / df['total_ingresos'] * 100,
        np.nan
    )

    return df


# ---------------------------------------------------------------------------
# 2. CAGR — TASA DE CRECIMIENTO ANUAL COMPUESTA
# ---------------------------------------------------------------------------

def calcular_cagr(df: pd.DataFrame, col: str, grupo: str = 'nombre_sector') -> pd.DataFrame:
    """
    Calcula la CAGR (Compound Annual Growth Rate) de una columna numérica
    entre el año mínimo y máximo disponible, agrupado.

    Formula: CAGR = (V_final / V_inicial)^(1/n) - 1

    Args:
        df: DataFrame con columnas [anio, grupo, col]
        col: Columna numérica para calcular la tasa
        grupo: Columna de agrupamiento (default: 'nombre_sector')

    Returns:
        DataFrame con columnas [grupo, v_inicial, v_final, n_anios, cagr_%]
    """
    agg = (
        df.groupby([grupo, 'anio'])[col]
        .sum()
        .reset_index()
    )
    primero = agg.groupby(grupo).first().rename(columns={col: 'v_inicial', 'anio': 'anio_ini'})
    ultimo = agg.groupby(grupo).last().rename(columns={col: 'v_final', 'anio': 'anio_fin'})
    result = primero.join(ultimo)
    result['n_anios'] = result['anio_fin'] - result['anio_ini']

    def cagr_safe(row):
        if row['n_anios'] <= 0 or row['v_inicial'] <= 0 or row['v_final'] < 0:
            return np.nan
        return ((row['v_final'] / row['v_inicial']) ** (1 / row['n_anios']) - 1) * 100

    result['cagr_%'] = result.apply(cagr_safe, axis=1).round(2)
    return result.reset_index()[[grupo, 'v_inicial', 'v_final', 'n_anios', 'cagr_%']]


# ---------------------------------------------------------------------------
# 3. SEGMENTACIÓN POR TAMAÑO DE EMPRESA
# ---------------------------------------------------------------------------

_RANGOS_PERSONAL = {
    'Microempresa': (0, 10),
    'Pequeña': (10, 50),
    'Mediana': (50, 200),
    'Grande': (200, float('inf')),
}


def clasificar_tamanio_empresa(df: pd.DataFrame,
                                col: str = 'personal_ocupado_total') -> pd.DataFrame:
    """
    Agrega columna 'tamanio_empresa' basada en personal ocupado total.
    Clasificación estándar colombiana (Ley 905 de 2004).

    Args:
        df: DataFrame con columna de personal
        col: Nombre de la columna de personal (default: 'personal_ocupado_total')

    Returns:
        DataFrame con columna 'tamanio_empresa' adicional.
    """
    df = df.copy()
    condiciones = []
    etiquetas = []
    for nombre, (low, high) in _RANGOS_PERSONAL.items():
        condiciones.append((df[col] >= low) & (df[col] < high))
        etiquetas.append(nombre)

    df['tamanio_empresa'] = np.select(condiciones, etiquetas, default='Sin datos')
    return df


# ---------------------------------------------------------------------------
# 4. AUTODIAGNÓSTICO BASADO EN DATOS REALES
# ---------------------------------------------------------------------------

def generar_autodiagnostico(df: pd.DataFrame) -> dict:
    """
    Genera un diccionario con observaciones automáticas sobre el dataset.

    Returns:
        dict con claves: 'correlacion', 'tendencia_ecologia', 'sector_lider',
                         'ratio_eco_promedio', 'alerta'
    """
    resultado = {}
    cols_num = ['total_ingresos', 'gastos_totales', 'gasto_gestion_amb', 'personal_ocupado_total']
    cols_ok = [c for c in cols_num if c in df.columns]

    # Correlación más alta con gasto ambiental
    if len(cols_ok) >= 2 and 'gasto_gestion_amb' in cols_ok:
        corr = df[cols_ok].corr()['gasto_gestion_amb'].drop('gasto_gestion_amb').sort_values(ascending=False)
        resultado['correlacion'] = f"El gasto ambiental correlaciona más con **{corr.index[0]}** (r={corr.iloc[0]:.2f})."

    # Tendencia ecológica
    if 'anio' in df.columns and 'ratio_eco_ingreso' in df.columns:
        eco_anual = df.groupby('anio')['ratio_eco_ingreso'].median()
        primer, ultimo = eco_anual.iloc[0], eco_anual.iloc[-1]
        delta = ultimo - primer
        dir_str = "aumentó" if delta > 0 else "disminuyó"
        resultado['tendencia_ecologia'] = (
            f"El ratio de inversión ambiental / ingreso {dir_str} "
            f"{abs(delta):.2f}pp entre {eco_anual.index[0]} y {eco_anual.index[-1]}."
        )

    # Sector líder en ecoeficiencia
    if 'nombre_sector' in df.columns and 'ratio_eco_ingreso' in df.columns:
        lider = df.groupby('nombre_sector')['ratio_eco_ingreso'].median().idxmax()
        resultado['sector_lider'] = f"El sector con mayor ratio ambiental/ingreso es **{lider}**."

    # Ratio eco promedio del año más reciente
    if 'anio' in df.columns and 'ratio_eco_ingreso' in df.columns:
        anio_rec = df['anio'].max()
        ratio_rec = df[df['anio'] == anio_rec]['ratio_eco_ingreso'].median()
        resultado['ratio_eco_promedio'] = (
            f"En {anio_rec}, la mediana de inversión ambiental fue "
            f"**{ratio_rec:.3f}%** del ingreso total."
        )

    # Alerta si ratio cayó
    if 'tendencia_ecologia' in resultado and 'disminuyó' in resultado['tendencia_ecologia']:
        resultado['alerta'] = "⚠️ La inversión ambiental proporcional al ingreso ha caído — señal de presión financiera."
    else:
        resultado['alerta'] = "✅ La inversión ambiental proporcional muestra tendencia estable o positiva."

    return resultado


# ---------------------------------------------------------------------------
# 5. RESUMEN EJECUTIVO PARA PÁGINA INICIO
# ---------------------------------------------------------------------------

def resumen_ejecutivo(df: pd.DataFrame) -> dict:
    """
    Genera un resumen ejecutivo para la página de inicio.

    Returns:
        dict con: anio_reciente, top3_sectores, cambio_ambiental_pct, total_empresas
    """
    if df.empty:
        return {}

    anio_max = df['anio'].max()
    anio_prev = anio_max - 1
    df_rec = df[df['anio'] == anio_max]
    df_ant = df[df['anio'] == anio_prev]

    top3 = (
        df_rec.groupby('nombre_sector')['gastos_totales']
        .sum()
        .nlargest(3)
        .index.tolist()
    )

    amb_rec = df_rec['gasto_gestion_amb'].sum()
    amb_ant = df_ant['gasto_gestion_amb'].sum() if not df_ant.empty else 0
    cambio_amb = ((amb_rec - amb_ant) / amb_ant * 100) if amb_ant > 0 else 0

    return {
        'anio_reciente': anio_max,
        'top3_sectores': top3,
        'cambio_ambiental_pct': round(cambio_amb, 1),
        'total_empresas': df_rec['id_empresa'].nunique(),
        'ratio_ambiental_mediano': round(
            (df_rec['gasto_gestion_amb'] / df_rec['total_ingresos'].replace(0, np.nan) * 100).median(), 3
        ),
    }
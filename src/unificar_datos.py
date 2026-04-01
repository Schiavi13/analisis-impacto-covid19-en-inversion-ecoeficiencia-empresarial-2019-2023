"""
Script de unificación de datos.
Lee todos los CSV de la carpeta `db/`, mapea columnas a la estructura de `db.txt`
y genera `datos_unificados.csv` para consumo del dashboard Streamlit.
"""
import pandas as pd
import numpy as np
import os

# mysql y dotenv son opcionales — sólo se usan si hay una BD activa
try:
    import mysql.connector  # noqa: F401
    from mysql.connector import Error as MySQLError
except ImportError:
    mysql = None
    MySQLError = Exception

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def conectar_mysql():
    """Intenta conectar a MySQL usando variables de entorno. Retorna None si falla."""
    if mysql is None:
        print("⚠️ mysql-connector-python no instalado. Saltando conexión a BD.")
        return None
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "encuesta_anual_servicios_db"),
        )
        return conn
    except MySQLError as e:
        print(f"⚠️ Nota DB: {e}")
        return None


def unificar_y_cargar_datos():
    """Lee CSVs de db/, mapea columnas según db.txt y exporta datos_unificados.csv."""
    carpeta_db = "db"
    print(f"🔄 Leyendo datos de la carpeta '{carpeta_db}'...")

    archivos_db = [f for f in os.listdir(carpeta_db) if f.endswith(".csv")]
    if not archivos_db:
        print("❌ No se encontraron archivos CSV en la carpeta 'db'.")
        return

    # --- Carga ---
    dfs: list[pd.DataFrame] = []
    for archivo in archivos_db:
        ruta = os.path.join(carpeta_db, archivo)
        try:
            try:
                df = pd.read_csv(ruta, encoding='utf-8', low_memory=False)
            except UnicodeDecodeError:
                df = pd.read_csv(ruta, encoding='latin1', low_memory=False)
            dfs.append(df)
            print(f"   -> {archivo} cargado ({len(df)} registros)")
        except Exception as e:
            print(f"⚠️ Error leyendo {archivo}: {e}")

    df_raw = pd.concat(dfs, ignore_index=True)
    df_raw.columns = [str(c).strip().replace('"', '').lower() for c in df_raw.columns]

    # --- Filtrar 2019-2023 ---
    if 'periodo' in df_raw.columns:
        df_raw['periodo'] = pd.to_numeric(df_raw['periodo'], errors='coerce')
        df_raw = df_raw[df_raw['periodo'].between(2019, 2023)].copy()

    # --- Mapeo de columnas (db.txt) ---
    mapeo_directo = {
        'anio': 'periodo',
        'id_empresa': 'id_empresa',
        'id_sector': 'id_sector',
        'nombre_sector': 'sector_desc',
        'anio_inicio': 'anio_inicio',
        'total_ingresos': 'total_ingresos',
        'personal_ocupado_total': 'personal_ocupado',
        'personal_remunerado': 'personal_remunerado',
        'contrata_personal_amb': 'contrata_personal_amb',
        'personal_mujeres': 'personal_mujeres',
        'personal_hombres': 'personal_hombres',
        'gastos_totales': 'gastos_totales',
        'gasto_gestion_amb': 'gasto_gestion_amb',
        'gasto_personal_total': 'gasto_personal_total',
        'imp_ind_com': 'imp_ind_com',
        'imp_otros': 'imp_otros',
        'gasto_remuneracion_personal': 'gasto_remuneracion_personal',
        'gasto_servicios_publicos': 'gasto_servicios_publicos',
        'gasto_energia_electrica': 'gasto_energia_electrica',
        'gasto_gas_natural': 'gasto_gas_natural',
    }

    df_uni = pd.DataFrame()
    for dest, origen in mapeo_directo.items():
        df_uni[dest] = df_raw[origen] if origen in df_raw.columns else np.nan

    # Valores por defecto
    df_uni['nombre_sector'] = df_uni['nombre_sector'].fillna('Sin identificar')
    df_uni['id_pais'] = 1
    df_uni['nombre_pais'] = "Colombia"

    # --- Columnas booleanas de inversión/gasto ambiental ---
    boolean_cols = [
        'realiza_inv_red_emision_aire', 'realiza_inv_evita_ruido_vibra',
        'realiza_inv_energia_limp', 'realiza_inv_ahorro_agua',
        'realiza_inv_inst_med_agua', 'realiza_inv_protec_suelo',
        'realiza_inv_disp_desechos', 'realiza_otras_inv_amb',
        'realiza_gasto_red_emision_aire', 'realiza_gasto_evita_ruido_vibra',
        'realiza_gasto_energia_limp', 'realiza_gasto_ahorro_agua',
        'realiza_gasto_terceros_amb', 'realiza_gasto_inst_med_agua',
        'realiza_gasto_protec_suelo', 'realiza_gasto_disp_desechos',
        'realiza_otros_gastos_amb',
    ]
    for col in boolean_cols:
        if col in df_raw.columns:
            valores = pd.to_numeric(df_raw[col], errors='coerce')
            df_uni[col] = valores.apply(
                lambda x: 1 if x == 1 else (0 if pd.notnull(x) else np.nan)
            )
        else:
            df_uni[col] = np.nan

    # --- Exportar ---
    ruta_salida = "datos_unificados.csv"
    df_uni.to_csv(ruta_salida, index=False)
    print(f"✅ '{ruta_salida}' generado ({len(df_uni)} registros, años 2019-2023).")


if __name__ == "__main__":
    unificar_y_cargar_datos()

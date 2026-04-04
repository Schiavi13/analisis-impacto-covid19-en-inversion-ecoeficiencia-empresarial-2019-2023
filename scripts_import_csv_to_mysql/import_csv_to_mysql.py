import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import sys

# 1. Configuración de entorno y conexión
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "proyecto")

csv_path = "data/clean/datos_unificados.csv"

def get_engine():
    connection_string = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(connection_string)

def import_data():
    if not os.path.exists(csv_path):
        print(f"❌ Error: No se encuentra el archivo {csv_path}")
        return

    print(f"📖 Cargando {csv_path}...")
    df = pd.read_csv(csv_path)
    df = df.replace({pd.NA: None})
    
    engine = get_engine()
    
    # Función auxiliar para insertar con IGNORE
    def to_sql_ignore(dataframe, table_name, connection):
        # Crear tabla temporal
        tmp_table = f"tmp_{table_name}"
        dataframe.to_sql(tmp_table, con=connection, if_exists='replace', index=False)
        
        # Insertar ignorando duplicados
        cols = ", ".join([f"`{c}`" for c in dataframe.columns])
        connection.execute(text(f"INSERT IGNORE INTO `{table_name}` ({cols}) SELECT {cols} FROM `{tmp_table}`"))
        
        # Borrar temporal
        connection.execute(text(f"DROP TABLE `{tmp_table}`"))

    try:
        with engine.begin() as conn:
            conn.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
            print("🚀 Iniciando importación normalizada e idempotente...")

            # 1. Tabla: sector_economico
            print("- Cargando sector_economico...")
            to_sql_ignore(df[['id_sector', 'nombre_sector']].drop_duplicates(), 'sector_economico', conn)

            # 2. Tabla: pais
            print("- Cargando pais...")
            to_sql_ignore(df[['id_pais', 'nombre_pais']].drop_duplicates(), 'pais', conn)

            # 3. Tabla: empresa
            print("- Cargando empresa...")
            to_sql_ignore(df[['id_empresa', 'id_sector', 'anio_inicio']].drop_duplicates(), 'empresa', conn)

            # 4. Tabla: empresa_opera_pais
            print("- Cargando empresa_opera_pais...")
            to_sql_ignore(df[['id_empresa', 'id_pais']].drop_duplicates(), 'empresa_opera_pais', conn)

            # 5. Tabla: ingresos
            print("- Cargando ingresos...")
            to_sql_ignore(df[['anio', 'id_empresa', 'total_ingresos']], 'ingresos', conn)

            # 6. Tabla: personal
            print("- Cargando personal...")
            personal_cols = ['anio', 'id_empresa', 'personal_ocupado_total', 'personal_remunerado', 
                             'contrata_personal_amb', 'personal_mujeres', 'personal_hombres']
            to_sql_ignore(df[personal_cols], 'personal', conn)

            # 7. Tabla: inversiones
            print("- Cargando inversiones...")
            inv_cols = ['anio', 'id_empresa', 'realiza_inv_red_emision_aire', 'realiza_inv_evita_ruido_vibra', 
                        'realiza_inv_energia_limp', 'realiza_inv_ahorro_agua', 'realiza_inv_inst_med_agua', 
                        'realiza_inv_protec_suelo', 'realiza_inv_disp_desechos', 'realiza_otras_inv_amb']
            to_sql_ignore(df[inv_cols], 'inversiones', conn)

            # 8. Tabla: gastos
            print("- Cargando gastos...")
            gastos_cols = ['anio', 'id_empresa', 'gasto_gestion_amb', 'gastos_totales', 'imp_ind_com', 'imp_otros', 
                           'gasto_personal_total', 'gasto_remuneracion_personal', 'gasto_servicios_publicos', 
                           'gasto_energia_electrica', 'gasto_gas_natural', 'realiza_gasto_red_emision_aire', 
                           'realiza_gasto_evita_ruido_vibra', 'realiza_gasto_energia_limp', 'realiza_gasto_ahorro_agua', 
                           'realiza_gasto_terceros_amb', 'realiza_gasto_inst_med_agua', 'realiza_gasto_protec_suelo', 
                           'realiza_gasto_disp_desechos', 'realiza_otros_gastos_amb']
            to_sql_ignore(df[gastos_cols], 'gastos', conn)

            conn.execute(text("SET FOREIGN_KEY_CHECKS=1;"))
            
        print("✅ ¡IMPORTACIÓN COMPLETADA EXITOSAMENTE (con manejo de duplicados)!")
        
    except Exception as e:
        print(f"❌ Error crítico durante la importación: {e}")

if __name__ == "__main__":
    import_data()

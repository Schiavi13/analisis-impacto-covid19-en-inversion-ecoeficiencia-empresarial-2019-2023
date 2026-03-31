import pandas as pd
from sqlalchemy import create_engine

# ==========================================
# 1. CONFIGURACIÓN DE LA BASE DE DATOS
# ==========================================
usuario = 'root'            
contrasena = 'tu_password'  # Cambia por tu contraseña
host = 'localhost'          
base_datos = 'encuesta_anual_servicios_db'

# Crear el motor de conexión
conexion_url = f"mysql+pymysql://{usuario}:{contrasena}@{host}/{base_datos}"
engine = create_engine(conexion_url)

# ==========================================
# 2. LEER EL ARCHIVO UNIFICADO
# ==========================================
ruta_archivo = 'datos_unificados.csv' # Asegúrate que esté en la misma carpeta que este script
print(f"Leyendo el archivo {ruta_archivo}...")
df_total = pd.read_csv(ruta_archivo)

# ==========================================
# 3. EXTRAER Y PREPARAR DATOS POR TABLA
# ==========================================
print("Procesando y dividiendo los datos...")

# 3.1. sector_economico
df_sector = df_total[['id_sector', 'nombre_sector']].drop_duplicates().dropna(subset=['id_sector'])

# 3.2. pais
df_pais = df_total[['id_pais', 'nombre_pais']].drop_duplicates().dropna(subset=['id_pais'])

# 3.3. empresa
df_empresa = df_total[['id_empresa', 'id_sector', 'anio_inicio']].drop_duplicates().dropna(subset=['id_empresa'])

# 3.4. empresa_opera_pais
df_empresa_pais = df_total[['id_empresa', 'id_pais']].drop_duplicates().dropna(subset=['id_empresa', 'id_pais'])

# 3.5. ingresos
df_ingresos = df_total[['anio', 'id_empresa', 'total_ingresos']].drop_duplicates().dropna(subset=['anio', 'id_empresa'])

# 3.6. personal
cols_personal = ['anio', 'id_empresa', 'personal_ocupado_total', 'personal_remunerado', 
                 'contrata_personal_amb', 'personal_mujeres', 'personal_hombres']
df_personal = df_total[cols_personal].drop_duplicates().dropna(subset=['anio', 'id_empresa'])

# 3.7. inversiones
cols_inversiones = ['anio', 'id_empresa', 'realiza_inv_red_emision_aire', 'realiza_inv_evita_ruido_vibra',
                    'realiza_inv_energia_limp', 'realiza_inv_ahorro_agua', 'realiza_inv_inst_med_agua',
                    'realiza_inv_protec_suelo', 'realiza_inv_disp_desechos', 'realiza_otras_inv_amb']
df_inversiones = df_total[cols_inversiones].drop_duplicates().dropna(subset=['anio', 'id_empresa'])

# 3.8. gastos
cols_gastos = ['anio', 'id_empresa', 'gasto_gestion_amb', 'gastos_totales', 'imp_ind_com', 'imp_otros',
               'gasto_personal_total', 'gasto_remuneracion_personal', 'gasto_servicios_publicos',
               'gasto_energia_electrica', 'gasto_gas_natural', 'realiza_gasto_red_emision_aire',
               'realiza_gasto_evita_ruido_vibra', 'realiza_gasto_energia_limp', 'realiza_gasto_ahorro_agua',
               'realiza_gasto_terceros_amb', 'realiza_gasto_inst_med_agua', 'realiza_gasto_protec_suelo',
               'realiza_gasto_disp_desechos', 'realiza_otros_gastos_amb']
df_gastos = df_total[cols_gastos].drop_duplicates().dropna(subset=['anio', 'id_empresa'])

# ==========================================
# 4. INSERTAR EN MYSQL (EN ORDEN ESTRICTO)
# ==========================================
# Diccionario con el orden de subida y sus respectivos DataFrames
tablas_a_subir = {
    'sector_economico': df_sector,
    'pais': df_pais,
    'empresa': df_empresa,
    'empresa_opera_pais': df_empresa_pais,
    'ingresos': df_ingresos,
    'personal': df_personal,
    'inversiones': df_inversiones,
    'gastos': df_gastos
}

for nombre_tabla, dataframe in tablas_a_subir.items():
    print(f"Subiendo {len(dataframe)} registros a la tabla '{nombre_tabla}'...")
    try:
        # Subir a la base de datos
        dataframe.to_sql(name=nombre_tabla, con=engine, if_exists='append', index=False)
        print(f"  -> ¡Éxito en {nombre_tabla}!")
    except Exception as e:
        print(f"  -> ERROR al subir {nombre_tabla}: {e}")
        print("  -> Se detuvo la carga para evitar inconsistencias.")
        break

print("\n¡Proceso finalizado!")
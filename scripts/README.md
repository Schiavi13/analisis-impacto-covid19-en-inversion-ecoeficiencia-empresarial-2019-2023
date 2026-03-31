# Guía de Importación: CSV a MySQL (Normalizado)

Este script (`import_csv_to_mysql.py`) automatiza la carga y normalización de los datos contenidos en el archivo `datos_unificados.csv` hacia un servidor MySQL.

## 🚀 Propósito
El archivo CSV original contiene datos denormalizados (planos). Este script transforma esa estructura única en **8 tablas relacionales** para cumplir con las mejores prácticas de bases de datos y garantizar la integridad referencial.

## 📋 Requisitos
1.  **Archivo de datos**: Debe existir el archivo `datos_unificados.csv` en la raíz del proyecto.
2.  **Configuración (.env)**: El script lee las credenciales (Host, Usuario, Password, Database) directamente de tu archivo `.env`.
3.  **Esquema de Base de Datos**: Las tablas deben estar creadas previamente (usando el archivo `db.txt`).
4.  **Librerías**: Tener instaladas `sqlalchemy`, `pandas`, `mysql-connector-python` y `python-dotenv`.

## ⚙️ Cómo Funciona
El script realiza un proceso de **ETL (Extractor, Transform, Load)**:

1.  **Extractor**: Lee los ~30,000 registros del CSV usando Pandas.
2.  **Transform (Normalización)**: 
    *   Identifica sectores económicos únicos.
    *   Identifica empresas únicas (basado en `id_empresa`).
    *   Relaciona empresas con países.
    *   Separa las métricas anuales en tablas temáticas: `ingresos`, `personal`, `inversiones` y `gastos`.
3.  **Load**: Inserta los datos en MySQL.
    *   Utiliza una lógica de **Insert Ignore** para que puedas correr el script varias veces sin generar errores por registros duplicados.
    *   Desactiva temporalmente las `FOREIGN_KEY_CHECKS` durante la carga masiva para ganar velocidad.

## 🛠️ Ejecución
Para ejecutar el proceso, corre el siguiente comando desde la terminal en la raíz del proyecto:

```bash
python scripts/import_csv_to_mysql.py
```

## 📊 Tablas Resultantes
Tras la ejecución exitosa, la base de datos contendrá:
*   `sector_economico`: Catálogo de sectores.
*   `pais`: Catálogo de países.
*   `empresa`: Maestros de cada empresa.
*   `empresa_opera_pais`: Tabla intermedia de ubicación.
*   `gastos`: Datos históricos de gastos (repetidos por año por empresa).
*   `personal`: Datos históricos de empleados.
*   `inversiones`: Datos históricos de inversión ambiental.
*   `ingresos`: Datos históricos de ingresos totales.

---
> [!TIP]
> Si deseas limpiar los datos y empezar de cero, borra el contenido de las tablas en MySQL antes de ejecutar este script.

# Integración y Población de Base de Datos (unir.py)

Este directorio contiene el script `unir.py`, el cual tiene como objetivo principal transformar el conjunto de datos masivo a un formato relacional de base de datos MySQL.

## 📝 Descripción del Script
El script `unir.py` realiza las siguientes funciones:
1.  **Lectura**: Carga el archivo maestro `datos_unificados.csv`.
2.  **Segmentación**: Divide las 39 columnas del CSV en 8 estructuras lógicas (DataFrames de Pandas).
3.  **Normalización**: Elimina duplicados en tablas maestras (como Empresas y Sectores) para mantener la integridad.
4.  **Carga Secuencial**: Inserta los datos en MySQL siguiendo un orden estricto para satisfacer las llaves foráneas:
    *   Primero: Catálogos (`sector_economico`, `pais`).
    *   Segundo: Entidades base (`empresa`, `empresa_opera_pais`).
    *   Tercero: Transacciones métricas (`ingresos`, `personal`, `inversiones`, `gastos`).

## ⚠️ Consideraciones de Uso
*   **Credenciales**: A diferencia de la versión en la carpeta `scripts/`, este archivo tiene las credenciales de base de datos escritas directamente en el código (líneas 7-10). **Debes actualizarlas** antes de ejecutarlo.
*   **Driver**: Utiliza `pymysql`. Asegúrate de tenerlo instalado.

## 🛠️ Instalación de Dependencias
Para usar este script específicamente, instala las librerías necesarias:

```bash
pip install -r unir/requirements.txt
```

---
> [!NOTE]
> Se recomienda usar preferiblemente el script ubicado en la carpeta central `scripts/import_csv_to_mysql.py`, ya que está automatizado mediante variables de entorno `.env` y es más robusto ante errores de duplicación.

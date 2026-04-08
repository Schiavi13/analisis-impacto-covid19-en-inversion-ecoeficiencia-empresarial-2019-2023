# 📊 EcoAnalytics Pro - Dashboard de Ecoeficiencia Empresarial

Plataforma analítica que evalúa el impacto del COVID-19 en la inversión ambiental empresarial colombiana (2019-2023), utilizando datos del **DANE** (Encuesta Ambiental Industrial).

# Colaboradores
- Melissa González López  
- Luis Fernando Martínez  
- Erika Osorio Foronda 
- Wilder Salas  
- Bernardo Saldarriaga 

## 🚀 Inicio Rápido

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Unificar datos (genera datos_unificados.csv)
python src/unificar_datos.py

# 3. Ejecutar el dashboard
streamlit run Inicio.py
```

## 📁 Estructura del Proyecto

```
├── .streamlit/
│   └── config.toml
├── comandos sql/
│   ├── consultas_analisis.sql
│   └── crear_tablas.sql
├── data/
│   ├── clean/
│   │   └── datos_unificados.csv
│   ├── procesados/
│   │   ├── ambiental/
│   │   │   ├── 2019_eas_ambiental.csv
│   │   │   ├── 2020_eas_ambiental.csv
│   │   │   ├── 2021_eas_ambiental.csv
│   │   │   ├── 2022_eas_ambiental.csv
│   │   │   └── 2023_eas_ambiental.csv
│   │   ├── covid/
│   │   │   └── colombia_casos_covid19_diarios.csv
│   │   ├── general/
│   │   │   ├── 2019_eas_general.csv
│   │   │   ├── 2020_eas_general.csv
│   │   │   ├── 2021_eas_general.csv
│   │   │   ├── 2022_eas_general.csv
│   │   │   └── 2023_eas_general.csv
│   │   └── unificados/
│   │       ├── 2019_eas_unificado.csv
│   │       ├── 2020_eas_unificado.csv
│   │       ├── 2021_eas_unificado.csv
│   │       ├── 2022_eas_unificado.csv
│   │       └── 2023_eas_unificado.csv
│   └── raw/
│       ├── ambiental/
│       │   ├── BasesDatos-MA-EAS-2019.csv
│       │   ├── BasesDatos-MA-EAS-2020.csv
│       │   ├── BasesDatos-MA-EAS-2021.csv
│       │   ├── MA_EAS_ANONIMA_2022_02022026.csv
│       │   └── MA_EAS_ANONIMA_2023_02022026.csv
│       ├── covid/
│       │   └── Colombia_COVID19_Coronavirus_casos_diarios.csv
│       └── general/
│           ├── EAS_2019.csv
│           ├── EAS_2020.csv
│           ├── EAS_2021.csv
│           ├── EAS_2022.csv
│           └── EAS_2023.csv
├── db/
│   ├── 2019_eas_unificado.csv
│   ├── 2020_eas_unificado.csv
│   ├── 2021_eas_unificado.csv
│   ├── 2022_eas_unificado.csv
│   ├── 2023_eas_unificado.csv
│   └── README.md
├── proyecto/
│   ├── diagramas/
│   │   ├── diagrama_modelo_entidad_relacion.png
│   │   └── diagrama_modelo_relacional.png
│   ├── metadatos/
│   │   ├── mapeo_de_datos.md
│   │   ├── mapeo_de_datos.xlsx
│   │   ├── reporte_2019.html
│   │   ├── reporte_2020.html
│   │   ├── reporte_2021.html
│   │   ├── reporte_2022.html
│   │   └── reporte_2023.html
│   ├── changelog.md
│   └── semantica_bd
├── mockups/
│   ├── estrategia_maquetacion.md
│   ├── mockup_consultor.png
│   ├── mockup_covid19.png
│   ├── mockup_data_science.png
│   ├── mockup_diagnostico.png
│   ├── mockup_empresarial.png
│   ├── mockup_inicio.png
│   ├── mockup_sectorial.png
│   └── README.md
├── notebooks/
│   └── analisis_metadatos.ipynb
├── pages/
│   ├── 0_🌳_Diagnostico.py
│   ├── 1_🦠_COVID-19.py
│   ├── 3_🏢_Empresarial.py
│   ├── 4_🏭_Sectorial.py
│   └── 5_🧬_Data_Science.py
├── scripts_import_csv_to_mysql/
│   ├── import_csv_to_mysql.py
│   └── README.md
├── src/
│   ├── analytics.py
│   ├── components.py
│   ├── connection.py
│   ├── data_quality.py
│   ├── ETL.ipynb
│   ├── interface.py
│   ├── merge_datasets_ambiental_general_2019.ipynb
│   ├── merge_datasets_ambiental_general_2020.ipynb
│   ├── merge_datasets_ambiental_general_2021.ipynb
│   ├── merge_datasets_ambiental_general_2022.ipynb
│   ├── merge_datasets_ambiental_general_2023.ipynb
│   ├── queries.py
│   ├── reports.py
│   ├── simulator.py
│   └── unificar_datos.py
├── unir_archivos_db/
│   ├── README.md
│   ├── requirements.txt
│   └── unir.py
├── .gitignore
├── Inicio.py
├── README.md
└── requirements.txt

```

## 🔧 Pipeline de Datos

1. **Fuente**: Departamento Administrativo Nacional de Estadística — www.dane.gov.co
2. **Datasets crudos**: Se encuentran en la ruta `data/raw`.
3. **Datasets procesados**: Se encuentran en la ruta `data/procesados`.
4. **Unificación:** `src/unificar_datos.py` lee todos los CSVs, normaliza columnas según `db.txt`, filtra años 2019-2023, y exporta `data/clean/datos_unificados.csv`.
5. **Carga:** `src/components.py` provee `cargar_datos()` con `@st.cache_data` para carga cacheada y limpieza de tipos.
6. **Carga a base de datos host remoto**: El notebook de colab `src/ETL.ipynb` realiza la carga a la base de datos en un host remoto.

## 📊 Módulos Analíticos

| Módulo | Funcionalidad |
|--------|---------------|
| **Diagnóstico** | KPIs con variación YoY, treemap sectorial, donut chart, tendencia multi-línea, tabla por sector con % ambiental |
| **COVID-19** | Contraste pre/post pandemia, curva de área con zona COVID, resiliencia sectorial, adopción de inversiones ambientales |
| **Empresarial** | Búsqueda por ID, KPIs individuales, evolución financiera, radar de inversiones ambientales |
| **Sectorial** | Distribución por boxplot, benchmarking vs promedio nacional |
| **Data Science** | Matriz de correlación (heatmap), dispersión logarítmica multidimensional, estadísticas descriptivas |

## 📋 Requisitos

- Python 3.9+
- Paquetes: `streamlit`, `pandas`, `plotly`, `numpy`

## 🎨 Prompt Optimizado para Mejoras Futuras

> **Rol:** Actúa como Data Scientist Senior y Frontend Engineer experto en Streamlit.
>
> **Contexto:** Dashboard analítico multi-página (Streamlit) alimentado por `data/clean/datos_unificados.csv` (>30K registros, 2019-2023, DANE Colombia). Arquitectura: `src/components.py` (datos + CSS), `pages/` (5 módulos), `.streamlit/config.toml` (tema).
>
> **Objetivo:** [DESCRIBIR MEJORA ESPECÍFICA]
>
> **Restricciones técnicas:**
> - NO usar CDNs externos (causan FOUC/parpadeo en Streamlit).
> - Usar `st.metric()`, `st.info()`, `st.error()` nativos de Streamlit.
> - CSS inline mínimo solo en `components.py` (variable `_CSS`).
> - Plotly con `template="plotly"` (compatible light/dark).
> - `@st.cache_data` para toda carga de datos.
> - Mantener estructura modular: `src/` para lógica, `pages/` para presentación.
>
> **Prácticas de ciencia de datos a seguir:**
> - Toda visualización debe tener ejes etiquetados y título descriptivo.
> - Comparaciones deben estar normalizadas (%, per cápita, YoY).
> - Usar escalas logarítmicas para datos con alta varianza.
> - Incluir contexto interpretativo junto a cada gráfico.
> - Separar análisis exploratorio (distribuciones) de confirmatorio (correlaciones).

## 📜 Licencia

Proyecto académico - Análisis de Impacto COVID-19 en Inversión de Ecoeficiencia Empresarial.

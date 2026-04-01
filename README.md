# 📊 EcoAnalytics Pro — Dashboard de Ecoeficiencia Empresarial

Plataforma analítica que evalúa el impacto del COVID-19 en la inversión ambiental empresarial colombiana (2019-2023), utilizando datos del **DANE** (Encuesta Ambiental Industrial).

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
├── Inicio.py                    # Página principal (landing + KPIs globales)
├── datos_unificados.csv         # Dataset consolidado (generado automáticamente)
├── requirements.txt             # Dependencias Python
├── .streamlit/
│   └── config.toml              # Tema visual de Streamlit (colores, fuente)
├── db/                          # Archivos CSV fuente del DANE (por año)
├── src/
│   ├── components.py            # Módulo centralizado: carga de datos, CSS, KPIs
│   └── unificar_datos.py        # Script ETL: une CSVs de db/ → datos_unificados.csv
└── pages/
    ├── 0_🌳_Diagnostico.py      # Treemap sectorial, tendencia, tabla detallada
    ├── 1_🦠_COVID-19.py         # Impacto pandémico: curva, resiliencia, adopción
    ├── 2_🔍_Consultor.py        # Riesgos/recomendaciones + análisis cuantitativo
    ├── 3_🏢_Empresarial.py      # Buscador por ID: perfil financiero + radar ambiental
    ├── 4_🏭_Sectorial.py        # Boxplots + benchmarking vs promedio nacional
    └── 5_🧬_Data_Science.py     # Heatmap de correlación, scatter log, estadísticas
```

## 🔧 Pipeline de Datos

1. **Fuentes:** Archivos CSV en `db/` (Encuesta Ambiental Industrial del DANE, 2019-2023).
2. **Unificación:** `src/unificar_datos.py` lee todos los CSVs, normaliza columnas según `db.txt`, filtra años 2019-2023, y exporta `datos_unificados.csv`.
3. **Carga:** `src/components.py` provee `cargar_datos()` con `@st.cache_data` para carga cacheada y limpieza de tipos.

## 📊 Módulos Analíticos

| Módulo | Funcionalidad |
|--------|---------------|
| **Diagnóstico** | KPIs con variación YoY, treemap sectorial, donut chart, tendencia multi-línea, tabla por sector con % ambiental |
| **COVID-19** | Contraste pre/post pandemia, curva de área con zona COVID, resiliencia sectorial, adopción de inversiones ambientales |
| **Consultor** | Hallazgos cualitativos por año + métricas cuantitativas + top sectores + mapa de inversiones |
| **Empresarial** | Búsqueda por ID, KPIs individuales, evolución financiera, radar de inversiones ambientales |
| **Sectorial** | Distribución por boxplot, benchmarking vs promedio nacional |
| **Data Science** | Matriz de correlación (heatmap), dispersión logarítmica multidimensional, estadísticas descriptivas |

## 🏗️ Buenas Prácticas Aplicadas

- **Separación de responsabilidades:** Lógica de datos en `src/`, presentación en `pages/`.
- **Caché de datos:** `@st.cache_data` evita recargar el CSV en cada interacción.
- **Sin CDNs externos:** CSS ligero inline en lugar de Tailwind CDN (elimina parpadeo/FOUC).
- **Tema nativo:** `.streamlit/config.toml` para colores base, sin CSS agresivo.
- **Imports guardados:** `mysql-connector` y `dotenv` son opcionales (try/except).
- **Constantes en mayúsculas:** CONOCIMIENTO, COLS, NOMS.
- **Type hints y docstrings** en funciones del módulo compartido.

## 📋 Requisitos

- Python 3.9+
- Paquetes: `streamlit`, `pandas`, `plotly`, `numpy`

## 🎨 Prompt Optimizado para Mejoras Futuras

> **Rol:** Actúa como Data Scientist Senior y Frontend Engineer experto en Streamlit.
>
> **Contexto:** Dashboard analítico multi-página (Streamlit) alimentado por `datos_unificados.csv` (>30K registros, 2019-2023, DANE Colombia). Arquitectura: `src/components.py` (datos + CSS), `pages/` (6 módulos), `.streamlit/config.toml` (tema).
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

Proyecto académico — Análisis de Impacto COVID-19 en Inversión de Ecoeficiencia Empresarial.
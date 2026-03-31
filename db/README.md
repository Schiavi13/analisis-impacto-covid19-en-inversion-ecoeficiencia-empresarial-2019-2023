# Origen y Propósito de los Datos (Carpeta db)

Esta carpeta contiene los archivos fuente de la investigación **"Análisis de Impacto COVID-19 en Inversión Ecoeficiencia Empresarial 2019-2023"**.

## 📊 Fuente de los Datos
Los archivos contenidos aquí (`2019_eas_unificado.csv` hasta `2023_eas_unificado.csv`) provienen de la **Encuesta Anual de Servicios (EAS)**. Esta es una operación estadística oficial que recopila información económica y ambiental de las empresas en Colombia.

## 🎯 Objetivo de estos Datos
Estos archivos fueron usados para:
1.  **Benchmarking Histórico**: Comparar el estado de la inversión ambiental antes (2019), durante (2020-2022) y después (2023) de la pandemia de COVID-19.
2.  **Análisis de Ecoeficiencia**: Evaluar si las empresas mantuvieron, redujeron o aumentaron sus gastos en gestión ambiental (aire, agua, ruido, energía limpia) frente a sus ingresos totales.
3.  **Normalización de Variables**: Servir como base para la creación del archivo maestro `datos_unificados.csv` y la posterior arquitectura de base de datos MySQL.

## 📁 Estructura de los Archivos
Cada archivo anual contiene campos críticos para la ciencia de datos, tales como:
*   **Identificación**: `id_empresa`, `id_sector`.
*   **Métricas Económicas**: `total_ingresos`, `gastos_totales`.
*   **Variables Ambientales**: Gastos en protección del suelo, medición de agua, reducción de emisiones y uso de energías limpias.
*   **Talento Humano**: Personal ambiental especializado y personal remunerado total.

---
**Nota de Uso**: Estos archivos representan el "Raw Data" (datos en bruto) balanceado y listo para ser consultado mediante el dashboard de Streamlit o directamente vía SQL tras el proceso de normalización.

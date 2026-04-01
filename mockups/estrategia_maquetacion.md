# Estrategia de Maquetación UI/UX - EcoAnalytics Pro

Basado en el análisis de los 7 mockups generados, presento la arquitectura visual estandarizada para garantizar coherencia en todo el aplicativo Streamlit. Esta guía asegura que el código coincida exactamente con las directrices de interfaz diseñadas.

## 1. Patrón Arquitectónico Base (Layout Estándar)

Todas las páginas (excepto Inicio) deben suscribirse estrictamente a este esqueleto visual de arriba hacia abajo:

1.  **Sidebar (Navegación pura):** Menú lateral nativo de Streamlit, sin widgets interactivos ni filtros. Solo enlaces de página. Fondo gris claro estándar.
2.  **Encabezado (Header):**
    *   `st.header("Icono + Título de la Página")`
    *   `st.caption("Descripción breve de 1 línea del propósito de la vista.")`
3.  **Contenedor de Filtros Inline (Acción Principal):**
    *   Obligatorio usar `with st.container(border=True):`
    *   Distribución en columnas (`st.columns`) para posicionar selectores (Año, Sector) a la izquierda y métricas de contexto o descripciones a la derecha.
4.  **Métricas Clave (KPIs):**
    *   Fila de 3 a 5 `st.metric()` agrupados lógicamente justo debajo del filtro o de la información principal.
5.  **Divisor Horizontal:**
    *   `st.divider()` para separar el área de "Contexto" del área de "Análisis Profundo".
6.  **Panel Analítico Interactivo (Tabs):**
    *   Uso extensivo de `st.tabs()` para organizar gráficos sin obligar al usuario a hacer scroll infinito verticalmente.
    *   Los gráficos deben usar `use_container_width=True` para adaptarse responsivamente.

---

## 2. Paleta Semántica y Estética de Datos (Data-Ink)

Para lograr la estética corporativa y analítica vista en los mockups, los gráficos generados con Plotly deben usar paletas intencionales:

| Concepto | Color Principal | Hexadecimal Sugerido | Uso |
| :--- | :---: | :--- | :--- |
| **Gasto Total / Riesgo / Caída** | Rojo / Naranja | `#ef4444`, `#f59e0b` | Impacto negativo, salidas de caja, caída COVID. |
| **Gasto Ambiental / Recuperación** | Verde Esmeralda | `#10b981`, `#059669` | Señales positivas, inversiones ecoeficientes. |
| **Ingresos / Benchmarks** | Azul Corporativo | `#3b82f6`, `#2563eb` | Datos financieros base, promedios nacionales. |
| **Fondos Analíticos (Heatmap/Polar)**| Escalas Continuas | `RdBu`, `Tealgrn` | Mapas de calor de correlación (rojo=inverso, azul=directo). |

**Reglas de Plotly:**
*   Eliminar fondos de gráficos (transparentes).
*   Mover las leyendas a la parte superior horizontal (`orientation='h', y=1.02`).
*   Usar bordes suaves y fuentes sin serifas modernas.

---

## 3. Estrategias por Tipología de Vista

### A. Vista Ejecutiva (Inicio)
Rompe el layout estándar. No tiene pestañas. Es un dashboard de "vistazo rápido" (Glanceable). Utiliza múltiples `st.columns` para agrupar métricas agregadas del ecosistema de manera asimétrica (sección de resumen a la izquierda, medallas a la derecha).

### B. Vistas Exploratorias (Diagnóstico, Sectorial)
Se enfocan en desgloses (Composición). El `st.selectbox` inline es vital aquí. En `Sectorial`, el uso de boxplots requiere paletas categóricas consistentes a lo largo de los años. En `Diagnóstico`, el uso de gráficos de área superpuestos para mostrar Gasto vs Ingresos es mandatario.

### C. Vistas Perfiladas (Empresarial)
Usa un patrón de maestro-detalle. La parte superior es una *Tarjeta de Identidad* de la empresa (Nombre, Sector, Tamaño) que ancla visualmente al usuario antes de mostrar los gráficos. El ratio de ecoeficiencia se destaca como un *Badge* o `st.success/info/warning` según su puntaje.

### D. Vistas Consultivas y Expertas (Consultor, Data Science)
Priorizan el texto generado y el diagnóstico sobre los gráficos interactivos.
*   **Consultor:** Patrón de alertas duales (Riesgo en rojo vs Acción en verde) ocupando el ancho completo de la pantalla.
*   **Data Science:** Requiere el ancho completo para el *Heatmap*. Las conclusiones textuales del autodiagnóstico (`st.info`) se renderizan *debajo* de las correlaciones numéricas.

---

## 4. Implementación Técnica en Streamlit

Este análisis confirma que **el refactor realizado previamente** (mover los filtros del sidebar a contenedores inline bordeados) fue el paso crítico fundamental para alcanzar el nivel de los mockups. 

Actualmente, el código de la aplicación **ya cumple** arquitectónicamente con esta estrategia de maquetación en las 7 vistas, garantizando que el diseño "UI Mockup" y la implementación "Frontend Streamlit" operen bajo el mismo paradigma visual.

# Mockups UI - EcoAnalytics Dashboard

Esta carpeta contiene los prototipos de alta fidelidad (mockups) para cada una de las 7 vistas principales del aplicativo **EcoAnalytics Pro**. Los diseños han sido generados siguiendo principios de experiencia de usuario (UX) e interfaces modernas de visualización de datos.

## Vistas Disponibles

| Archivo | Vista | Descripción del Diseño |
|---|---|---|
| `mockup_inicio.png` | **Inicio** | Layout ejecutivo, tarjetas de KPI consolidadas, medallas de progreso y resumen de los módulos disponibles. Estética "Data-forward" y profesional. |
| `mockup_diagnostico.png` | **Diagnóstico** | Presenta un Treemap dominante para visualización de desglose sectorial. Muestra filtros "inline" limpios en la parte superior y métricas de alto nivel. |
| `mockup_covid19.png` | **COVID-19** | Diseño centrado en series temporales duales, resaltando con una banda vertical de peligro la "Zona COVID". Tarjetas de caída y recuperación evidencian el impacto del choque. |
| `mockup_consultor.png` | **Consultor** | Interfaz consultiva de dos paneles: alertas cualitativas ("Riesgo" y "Acción") dominan la narrativa, acompañadas de gráficos de soporte en pestañas inferiores. |
| `mockup_empresarial.png` | **Empresarial** | Perfil detallado con layout de "tarjeta de identidad" empresarial, incluyendo ratios de desempeño en la esquina superior. Doble modo (búsqueda ID o filtros) claramente visible al tope. |
| `mockup_sectorial.png` | **Sectorial** | Visualización técnica comparativa. Layout centrado en diagramas de caja (Boxplots) limpios para análisis de distribución frente a benchmarks nacionales. |
| `mockup_data_science.png` | **Data Science** | Vista experta dominada por una matriz de correlación (Heatmap) de 4x4. Panel inferior de "Diagnóstico Automático" con lecturas interpretativas automatizadas. |

### Principios de Diseño Aplicados (UX/UI)
1. **Consistencia de Navegación:** Todos los prototipos muestran el sidebar dedicado estrictamente a la navegación de módulos.
2. **Jerarquía Visual:** Uso claro de `Headers`, Divisores (`<hr>`) y `Tabs` (pestañas) para estructurar la complejidad de la información sin saturar el lienzo.
3. **Filtros Inline:** Los controles de filtrado (año, sector, modo) se extrajeron a contenedores bordeados en el área principal para máxima visibilidad, evitando el uso del menú lateral.
4. **Data-Ink Ratio:** Gráficos minimalistas con la menor cantidad de "ruido" visual posible, colores semánticos (Verde=Positivo/Ecológico, Rojo=Gasto/Peligro/COVID).
5. **Legibilidad:** Tipografía Sans-serif moderna, amplios márgenes y sistema de grilla que respeta áreas de respiración (whitespace).

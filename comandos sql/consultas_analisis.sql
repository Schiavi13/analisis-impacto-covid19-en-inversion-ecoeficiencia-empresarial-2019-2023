-- =========================================================================
-- CONSULTAS SQL PARA ANÁLISIS DE DATOS (NIVEL: SIMPLE Y AVANZADO)
-- Proyecto: Impacto COVID-19 en Inversión Ecoeficiencia (2019-2023)
-- =========================================================================

USE encuesta_anual_servicios_db;

-- #########################################################################
-- PARTE 1: CONSULTAS SIMPLES (Exploración Básica)
-- #########################################################################

-- 1.1. Ver todos los sectores disponibles
SELECT * FROM sector_economico;

-- 1.2. Contar cuántas empresas hay registradas en total
SELECT COUNT(*) AS total_empresas FROM empresa;

-- 1.3. Ver los ingresos de los primeros 10 registros del año 2023
SELECT id_empresa, total_ingresos 
FROM ingresos 
WHERE anio = 2023 
LIMIT 10;

-- 1.4. Listar empresas que iniciaron operación después del año 2010
SELECT id_empresa, id_sector, anio_inicio 
FROM empresa 
WHERE anio_inicio > 2010;

-- 1.5. Sumatoria total de gastos ambientales en toda la historia
SELECT SUM(gasto_gestion_amb) AS gasto_ambiental_acumulado FROM gastos;


-- #########################################################################
-- PARTE 2: CONSULTAS AVANZADAS (Ciencia de Datos y Business Intelligence)
-- #########################################################################

-- 2.1. ANÁLISIS DE CRECIMIENTO ANUAL (YOY)
-- Calcula el crecimiento porcentual del gasto ambiental año tras año.
SELECT 
    anio, 
    SUM(gasto_gestion_amb) as total_amb,
    LAG(SUM(gasto_gestion_amb)) OVER (ORDER BY anio) as año_anterior,
    (SUM(gasto_gestion_amb) - LAG(SUM(gasto_gestion_amb)) OVER (ORDER BY anio)) / LAG(SUM(gasto_gestion_amb)) OVER (ORDER BY anio) * 100 as crecimiento_pct
FROM gastos
GROUP BY anio;

-- 2.2. RANKING DE SECTORES POR ECOEFICIENCIA (Normalizado)
-- Calcula qué sectores son más eficientes: Gasto Ambiental dividido por Ingreso Total.
SELECT 
    s.nombre_sector,
    COUNT(e.id_empresa) as num_empresas,
    AVG(g.gasto_gestion_amb / i.total_ingresos) * 100 as ratio_ecoeficiencia_pct
FROM gastos g
JOIN ingresos i ON g.id_empresa = i.id_empresa AND g.anio = i.anio
JOIN empresa e ON g.id_empresa = e.id_empresa
JOIN sector_economico s ON e.id_sector = s.id_sector
WHERE i.total_ingresos > 0
GROUP BY s.nombre_sector
HAVING num_empresas > 5
ORDER BY ratio_ecoeficiencia_pct DESC;

-- 2.3. PARADOJA DE INVERSIÓN (ANÁLISIS DE COMPORTAMIENTO)
-- Identifica empresas que AUMENTARON su gasto ambiental en 2020 a pesar de tener MENOS ingresos (Compromiso ambiental).
SELECT 
    i.id_empresa,
    i.total_ingresos as ingresos_2020,
    g.gasto_gestion_amb as gasto_amb_2020
FROM ingresos i
JOIN gastos g ON i.id_empresa = g.id_empresa AND i.anio = g.anio
WHERE i.anio = 2020 
AND i.total_ingresos < (SELECT AVG(total_ingresos) FROM ingresos WHERE anio = 2019)
AND g.gasto_gestion_amb > (SELECT AVG(gasto_gestion_amb) FROM gastos WHERE anio = 2019)
LIMIT 20;

-- 2.4. CORRELACIÓN: TALENTO VS EFICIENCIA ENERGÉTICA
-- Compara el gasto promedio en energía entre empresas que tienen personal ambiental vs las que no.
SELECT 
    p.contrata_personal_amb,
    AVG(g.gasto_energia_electrica) as avg_energia,
    AVG(g.gasto_servicios_publicos) as avg_servicios_totales
FROM personal p
JOIN gastos g ON p.id_empresa = g.id_empresa AND p.anio = g.anio
GROUP BY p.contrata_personal_amb;

-- 2.5. MATRIZ DE ADOPCIÓN TECNOLÓGICA (MACHINE LEARNING READINESS)
-- Crea una tabla con flags de inversión para ver qué sectores adoptan más tecnologías limpias.
SELECT 
    s.nombre_sector,
    SUM(inv.realiza_inv_energia_limp) as cont_energia_limpia,
    SUM(inv.realiza_inv_ahorro_agua) as cont_ahorro_agua,
    SUM(inv.realiza_inv_red_emision_aire) as cont_emisiones
FROM inversiones inv
JOIN empresa e ON inv.id_empresa = e.id_empresa
JOIN sector_economico s ON e.id_sector = s.id_sector
GROUP BY s.nombre_sector
ORDER BY cont_energia_limpia DESC;

-- 2.6. CONSULTA MAESTRA (VISTA DE MINERÍA DE DATOS)
-- Une todas las tablas en una sola para exportar directamente a Python.
SELECT 
    e.id_empresa, 
    s.nombre_sector, 
    g.anio, 
    i.total_ingresos, 
    g.gastos_totales, 
    g.gasto_gestion_amb, 
    p.personal_ocupado_total,
    inv.realiza_inv_energia_limp,
    inv.realiza_inv_ahorro_agua
FROM empresa e
JOIN sector_economico s ON e.id_sector = s.id_sector
JOIN gastos g ON e.id_empresa = g.id_empresa
JOIN ingresos i ON g.id_empresa = i.id_empresa AND g.anio = i.anio
JOIN personal p ON g.id_empresa = p.id_empresa AND g.anio = p.anio
JOIN inversiones inv ON g.id_empresa = inv.id_empresa AND g.anio = inv.anio;

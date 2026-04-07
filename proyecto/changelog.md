# Changelog
Este archivo contiene los cambios realizados a los datos

---

## 2026-03-13

### Luis:
**Nuevo**
* Se crea columna ID_SECTOR en dataset 2022, sacando el id de la SECCION
* Se crea columna SECTOR_DESC en dataset 2022, sacando la descripción de la SECCION

**Cambia**
* Se reemplazan las tildes en columna SECTOR_DESC en dataset 2022
* Se transforma a minúscula la columna SECTOR_DESC en dataset 2022
* Se reemplaza “ñ” por “ni” en columna SECTOR_DESC en dataset 2022
* Se remueven espacios sobrantes en columna ID_SECTOR en dataset 2022
* Se remueven espacios sobrantes en columna SECTOR_DESC en dataset 2022
* Se remueve columna SECCION en dataset 2022
* Se transforma el formato del campo GASPROGESAMB a decimal en dataset 2022
* Se transforma el formato del campo gastos_tot a decimal en dataset 2022

### Wilder:
**Nuevo**
* se crea la columna ID_SECCION en dataset 2023, sacando el id de la SECCION
* se crea la columna SECCION_DESC, sacando la descripción de la SECCION
* se crea la columna ACTNOM

**Cambia**
* se verifica la existencia o no de archivos duplicados en la columna IDNOREMPAN
* se transforma a minuscula las columnas SECCION_DESC y ACTMON
* se eliminan tildes y las ñ en las columnas SECCION_DESC y ACTMON
* se eliminan espacios en blanco en la columna ID_SECCION
* se actualiza la columna ACTNOM dejando los datos en minuscula, sin tildes y sin ñ.

---

## 2026-03-14

### Luis:
**Nuevo**
* Se crea columna reemplazo ACTNOM en dataset 2022

**Cambia**
* Se transforma a minúsculas la columna nueva ACTNOM en dataset 2022
* Se reemplazan las tildes en columna nueva ACTNOM en dataset 2022
* Se reemplaza “ñ” por “ni” en columna nueva ACTNOM en dataset 2022
* Se remueve columna original ACTNOM en dataset 2022
* Se remueven espacios adicionales de columna SECCION_DESC en dataset 2020
* Se remueve columna SECCION en dataset 2020
* Se remueve columna ciuu4 en dataset 2020
* Se remueve columna idact en dataset 2020
* Se remueve columna ciiu4 en dataset 2021
* Se transforma el formato del campo GASPROGESAMB a decimal en dataset 2020
* Se transforma el formato del campo gasto_total_EAS a decimal en dataset 2020
* Se transforma el formato del campo gastos_tot a decimal en dataset 2021
* Se transforma el formato del campo GASPROGESAMB a decimal en dataset 2021

**Nuevo**
* Se crea columna ID_SECTOR en dataset 2021, con el id de Seccion
* Se crea columna SECTOR_DESC en dataset 2021, con la descripción de Seccion
* Se crea columna reemplazo ACTNOM en dataset 2021

**Cambia**
* Se remueve columna original ACTNOM en dataset 2021
* Se remueve columna Seccion en dataset 2021

**Nuevo**
* Se crea columna FECHA en dataset covid-19, extrayendo fecha de FECHA_ACTUALIZACION

**Cambia**
* Remueve columna FECHA_ACTUALIZACION en dataset covid-19
* Remueve columna GlobalID en dataset covid-19
* Remueve columna TOTAL_MUERTES en dataset covid-19
* Remueve columna TOTAL_RECUPERADO en dataset covid-19
* Remueve columna NUEVOS_MUERTOS en dataset covid-19
* Remueve columna NUEVO_RECUPERADOS en dataset covid-19
* Remueve columna OBJECTID en dataset covid-19
* Reemplaza nombre de columna idnorempan por id_empresa en dataset 2022
* Reemplaza nombre de columna PERIODO por periodo en dataset 2022
* Reemplaza nombre de columna GASPROGESAMB por gasto_gestion_amb en dataset 2022
* Reemplaza nombre de columna gastos_tot por gastos_totales en dataset 2022
* Reemplaza nombre de columna ACTINV1 por inv_emisiones_aire en dataset 2022
* Reemplaza nombre de columna ACTINV2 por inv_ahorro_agua en dataset 2022
* Reemplaza nombre de columna ACTINV3 por inv_medicion_agua en dataset 2022
* Reemplaza nombre de columna ACTINV4 por inv_desechos en dataset 2022
* Reemplaza nombre de columna ACTINV5 por inv_protec_suelo en dataset 2022

---

## 2026-03-16

### Luis:
**Cambia**
* Reemplaza nombre de columna ACTINV6 por inv_ruido_vibra en dataset 2022
* Reemplaza nombre de columna ACTINV7 por inv_energia_limpia en dataset 2022
* Reemplaza nombre de columna ACTINV8 por inv_otras_amb en dataset 2022
* Reemplaza nombre de columna ACTGAST1 por gasto_emisiones en dataset 2022
* Reemplaza nombre de columna ACTGAST2 por gasto_ahorro_agua en dataset 2022
* Reemplaza nombre de columna ACTGAST3 por gasto_medicion_ag en dataset 2022
* Reemplaza nombre de columna ACTGAST4 por gasto_desechos en dataset 2022
* Reemplaza nombre de columna ACTGAST5 por gasto_protec_suel en dataset 2022
* Reemplaza nombre de columna ACTGAST6 por gasto_ruido_vibra en dataset 2022
* Reemplaza nombre de columna ACTGAST7 por gasto_terceros_amb en dataset 2022
* Reemplaza nombre de columna ACTGAST8 por gasto_energia_limp en dataset 2022
* Reemplaza nombre de columna ACTGAST9 por gasto_otros_amb en dataset 2022
* Reemplaza nombre de columna PERSAMB por personal_ambiental en dataset 2022
* Reemplaza nombre de columna ID_SECCION por id_seccion en dataset 2022
* Reemplaza nombre de columna SECION_DESC por seccion_desc en dataset 2022
* Reemplaza nombre de columna Periodo por periodo en dataset 2020
* Reemplaza nombre de columna idnoremp por id_empresa en dataset 2020
* Reemplaza nombre de columna gasto_total_EAS por gastos_totales en dataset 2020
* Reemplaza nombre de columna GASPROGESAMB por gasto_gestion_amb en dataset 2020
* Reemplaza nombre de columna ACTINV1 por inv_emisiones_aire en dataset 2020
* Reemplaza nombre de columna ACTINV2 por inv_ahorro_agua en dataset 2020
* Reemplaza nombre de columna ACTINV3 por inv_medicion_agua en dataset 2020
* Reemplaza nombre de columna ACTINV4 por inv_desechos en dataset 2020
* Reemplaza nombre de columna ACTINV5 por inv_protec_suelo en dataset 2020
* Reemplaza nombre de columna ACTINV6 por inv_ruido_vibra en dataset 2020
* Reemplaza nombre de columna ACTINV7 por inv_energia_limpia en dataset 2020
* Reemplaza nombre de columna ACTINV8 por inv_otras_amb en dataset 2020
* Reemplaza nombre de columna ACTGAST1 por gasto_emisiones en dataset 2020
* Reemplaza nombre de columna ACTGAST2 por gasto_ahorro_agua en dataset 2020
* Reemplaza nombre de columna ACTGAST3 por gasto_medicion_ag en dataset 2020
* Reemplaza nombre de columna ACTGAST4 por gasto_desechos en dataset 2020
* Reemplaza nombre de columna ACTGAST5 por gasto_protec_suel en dataset 2020
* Reemplaza nombre de columna ACTGAST6 por gasto_ruido_vibra en dataset 2020
* Reemplaza nombre de columna ACTGAST7 por gasto_terceros_amb en dataset 2020
* Reemplaza nombre de columna ACTGAST8 por gasto_energia_limp en dataset 2020
* Reemplaza nombre de columna ACTGAST9 por gasto_otros_amb en dataset 2020
* Reemplaza nombre de columna ID_SECCION por id_seccion en dataset 2020
* Reemplaza nombre de columna SECCION_DESC por seccion_desc en dataset 2020

---

## 2026-03-18

### Luis:
**Cambia:**
* Transforma nombres de columnas a minúsculas en dataset covid-19

---

## 2026-03-19

### Luis:
**Cambia**
* Reemplaza nombres de columnas por nombres sugeridos en mapeo de datos en dataset 2022
* Remueve columna ACTNOM en dataset 2022
* Reemplaza nombres de columnas por nombres sugeridos en mapeo de datos en dataset 2020
* Remueve columna ACTNOM en dataset 2021
* Reemplaza nombres de columnas por nombres sugeridos en mapeo de datos en dataset 2021
* Reemplaza nombre de columna ID_SECTOR por id_sector en dataset 2021
* Reemplaza nombre de columna SECTOR_DESC por sector_desc en dataset 2021
* Remueve columna CIUU4 en dataset 2019
* Remueve columna IDACT en dataset 2019
* Remueve espacios sobrantes en columna SECTOR_DESC en dataset 2019
* Remueve columna INGREVEN en dataset 2019

**Nuevo**
* Crea la columna realiza_otras_inv_amb en dataset 2019, con un OR lógico entre ACTINV7 y ACTINV9

**Cambia**
* Remueve columna PUEAA en dataset 2019
* Remueve columna SEPRRSSC en dataset 2019
* Remueve columna REUTRECI en dataset 2019
* Remueve columna TRATRECI en dataset 2019
* Remueve columna COMRE1D en dataset 2019
* Remueve columna COMPMPS en dataset 2019
* Remueve columna intio en dataset 2019
* Remueve columna SECCION en dataset 2019
* Reemplaza nombre de columna ID_SECTOR por id_sector en dataset 2019
* Reemplaza nombre de columna SECTOR_DESC por sector_desc en dataset 2019
* Remueve columna ACTINV7 en dataset 2019
* Remueve columna ACTINV9 en dataset 2019
* Reemplaza nombres de columnas por nombres sugeridos en mapeo de datos en dataset 2019
* Remueve espacios sobrantes en columna SECCION_DESC en dataset 2023
* Remueve columna SECCION en dataset 2023
* Remueve columna ACTNOM en dataset 2023
* Remueve columna FUEN_AG_TOT en dataset 2023
* Remueve columna WTOTECONSUM en dataset 2023
* Transforma el formato de la columna GASPROGESAMB a decimal
* Transforma el formato de la columna gastos_tot a decimal
* Reemplaza el nombre de columna ID_SECCION por id_sector
* Reemplaza el nombre de columna SECCION_DESC por sector_desc
* Reordena columnas en dataset 2019
* Reemplaza el nombre de columna id_seccion por id_sector en dataset 2020
* Reemplaza el nombre de columna seccion_desc por sector_desc en dataset 2020
* Reordena columnas en dataset 2020
* Reordena columnas en dataset 2021
* Reemplaza nombre de columna id_seccion por id_sector en dataset 2022
* Reemplaza nombre de columna seccion_desc por sector_desc en dataset 2022
* Reordena columnas en dataset 2022
* Reordena columnas en dataset 2023
* Reemplaza nombre de archivo BasesDatos-MA-EAS-2019.csv por 2019_eas_ambiental.csv
* Reemplaza nombre de archivo BasesDatos-MA-EAS-2020.csv por 2020_eas_ambiental.csv
* Reemplaza nombre de archivo BasesDatos-MA-EAS-2021.csv por 2021_eas_ambiental.csv
* Reemplaza nombre de archivo MA_EAS_ANONIMA_2022_02022026.csv por 2022_eas_ambiental.csv
* Reemplaza nombre de archivo MA_EAS_ANONIMA_2023_02022026 por 2023_eas_ambiental
* Reemplaza nombre de archivo Colombia_COVID19_Coronavirus_casos_diarios.csv por colombia_casos_covid19_diarios.csv
* Reemplaza nombre de archivo EAS_2019.csv por 2019_eas_general.csv
* Reemplaza nombre de archivo EAS_2020.csv por 2020_eas_general.csv
* Reemplaza nombre de archivo EAS_2021.csv por 2021_eas_general.csv
* Reemplaza nombre de archivo EAS_2022.csv por 2022_eas_general.csv
* Reemplaza nombre de archivo EAS_2023.csv por 2023_eas_general.csv
* Remueve columna de índices del dataset general de 2019
* Remueve columna Division del dataset general de 2019
* Remueve columnas no seleccionadas en el mapeo de datos del dataset general de 2019
* Reemplaza nombre de columna Seccion19 por id_sector en dataset general de 2019
* Remueve columna ocgtot de dataset general de 2019
* Reemplaza nombres de columnas por nombres sugeridos en mapeo de datos en dataset general de 2019
* Transforma columna total_ingresos a decimal en dataset general de 2019
* Transforma columna gasto_remuneracion_personal a decimal en dataset general de 2019
* Transforma columna gasto_personal_total a decimal en dataset general de 2019
* Transforma columna imp_ind_com a decimal en dataset general de 2019
* Transforma columna imp_renta_equidad a decimal en dataset general de 2019
* Transforma columna imp_otros a decimal en dataset general de 2019
* Transforma columna gasto_servicios_publicos a decimal en dataset general de 2019
* Transforma columna gasto_energia_electrica a decimal en dataset general de 2019
* Transforma columna gasto_gas_natural a decimal en dataset general de 2019
* Reordena columnas en dataset general de 2019

### Wilder:
**Nuevo**
* Se hace INNER JOIN en los 2020_eas_ambiental y 2020_eas_general creando un nuevo archivo 2020_unificado.xlsx
* Se deja solo una columna periodo,
* Se crearon 6111 registros
* Se eliminan 68 columnas que no contienen registros.
* Se dejan las columnas idaho (con 1 registro vacio), prottmoe, pohtmoe y pmision (estas últimas con 158 registros vacíos),
* Se carga documento al drive (pendiente eliminar registros vacíos)

---

## 2026-03-21

### Luis:
**Cambio**
* Transforma el tipo de dato de columnas en decimal por automático debido a problemas con pandas.

**Nuevo**
* Crea dataset 2019_eas_unificado.csv haciendo inner join de 2019_eas_ambiental.csv y 2019_eas_general.csv por columna id_empresa

**Cambio**
* Remueve columnas no seleccionadas en el mapeo de datos del dataset general de 2022
* Reemplaza nombres de columnas por nombres sugeridos en mapeo de datos en dataset general de 2022
* Reordena columnas en dataset general de 2022
* Transforma tipo de dato de columnas que estaban en decimal a automático por problemas con pandas en dataset ambiental 2022

**Nuevo**
* Crea dataset 2022_eas_unificado.csv haciendo inner join de 2022_eas_ambiental.csv y 2022_eas_general.csv por columna id_empresa

---

## 2026-03-23

### Luis:
**Cambio**
* Remueve columnas no seleccionadas en el mapeo de datos del dataset general de 2023
* Reemplaza nombres de columnas por nombres sugeridos en mapeo de datos en dataset general de 2023
* Reordena columnas en dataset general de 2023
* Transforma tipo de dato de columnas que estaban en decimal a automático por problemas con pandas en dataset ambiental 2023

**Nuevo**
* Crea dataset 2023_eas_unificado.csv haciendo inner join de 2023_eas_ambiental.csv y 2023_eas_general.csv por columna id_empresa

**Cambio**
* Remueve columnas no seleccionadas en el mapeo de datos del dataset general de 2021
* Reemplaza nombres de columnas por nombres sugeridos en mapeo de datos en dataset general de 2021
* Reordena columnas en dataset general de 2021
* Transforma tipo de dato de columnas que estaban en decimal a automático por problemas con pandas en dataset ambiental 2021

**Nuevo**
* Crea dataset 2021_eas_unificado.csv haciendo inner join de 2021_eas_ambiental.csv y 2021_eas_general.csv por columna id_empresa

**Cambia**
* Remueve columna imp_renta_equidad en dataset general de 2019
* Remueve columna imp_renta_equidad en dataset unificado de 2019

---

## 2026-03-24

### Luis:
**Cambia**
* Remueve columnas no seleccionadas en el mapeo de datos del dataset general de 2020
* Reemplaza nombres de columnas por nombres sugeridos en mapeo de datos en dataset general de 2020
* Reordena columnas en dataset general de 2020
* Transforma tipo de dato de columnas que estaban en decimal a automático por problemas con pandas en dataset ambiental 2020
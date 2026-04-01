-- 1. Crear la base de datos
CREATE DATABASE IF NOT EXISTS encuesta_anual_servicios_db;
USE encuesta_anual_servicios_db;

-- 2. Desactivar revisión de llaves foráneas temporalmente
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;

-- 3. Tabla: sector_economico
DROP TABLE IF EXISTS `sector_economico`;
CREATE TABLE `sector_economico` (
  `id_sector` varchar(3) NOT NULL,
  `nombre_sector` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id_sector`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 4. Tabla: pais
DROP TABLE IF EXISTS `pais`;
CREATE TABLE `pais` (
  `id_pais` int NOT NULL AUTO_INCREMENT,
  `nombre_pais` varchar(100) NOT NULL,
  PRIMARY KEY (`id_pais`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 5. Tabla: empresa
DROP TABLE IF EXISTS `empresa`;
CREATE TABLE `empresa` (
  `id_empresa` int NOT NULL,
  `id_sector` varchar(250) NOT NULL,
  `anio_inicio` int DEFAULT NULL,
  PRIMARY KEY (`id_empresa`),
  KEY `fk_sector_economico` (`id_sector`),
  CONSTRAINT `fk_sector_economico` FOREIGN KEY (`id_sector`) REFERENCES `sector_economico` (`id_sector`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_anio_greater_zero` CHECK ((`anio_inicio` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 6. Tabla: empresa_opera_pais
DROP TABLE IF EXISTS `empresa_opera_pais`;
CREATE TABLE `empresa_opera_pais` (
  `id_empresa` int NOT NULL,
  `id_pais` int NOT NULL,
  PRIMARY KEY (`id_empresa`,`id_pais`),
  KEY `fk_pais_opera` (`id_pais`),
  CONSTRAINT `fk_empresa` FOREIGN KEY (`id_empresa`) REFERENCES `empresa` (`id_empresa`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_pais_opera` FOREIGN KEY (`id_pais`) REFERENCES `pais` (`id_pais`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 7. Tabla: casos_covid
DROP TABLE IF EXISTS `casos_covid`;
CREATE TABLE `casos_covid` (
  `fecha_caso` date NOT NULL,
  `id_pais` int NOT NULL,
  PRIMARY KEY (`fecha_caso`,`id_pais`),
  KEY `fk_pais` (`id_pais`),
  CONSTRAINT `fk_pais` FOREIGN KEY (`id_pais`) REFERENCES `pais` (`id_pais`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 8. Tabla: ingresos
DROP TABLE IF EXISTS `ingresos`;
CREATE TABLE `ingresos` (
  `anio` int NOT NULL,
  `id_empresa` int NOT NULL,
  `total_ingresos` decimal(16,4) DEFAULT NULL,
  PRIMARY KEY (`anio`,`id_empresa`),
  KEY `fk_empresa_ingresos` (`id_empresa`),
  CONSTRAINT `fk_empresa_ingresos` FOREIGN KEY (`id_empresa`) REFERENCES `empresa` (`id_empresa`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 9. Tabla: personal
DROP TABLE IF EXISTS `personal`;
CREATE TABLE `personal` (
  `anio` int NOT NULL,
  `id_empresa` int NOT NULL,
  `personal_ocupado_total` int DEFAULT NULL,
  `personal_remunerado` int DEFAULT NULL,
  `contrata_personal_amb` tinyint DEFAULT NULL,
  `personal_mujeres` int DEFAULT NULL,
  `personal_hombres` int DEFAULT NULL,
  PRIMARY KEY (`anio`,`id_empresa`),
  KEY `fk_empresa_personal` (`id_empresa`),
  CONSTRAINT `fk_empresa_personal` FOREIGN KEY (`id_empresa`) REFERENCES `empresa` (`id_empresa`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_contrata_personal_amb_bool` CHECK (((`contrata_personal_amb` is null) or (`contrata_personal_amb` = 1) or (`contrata_personal_amb` = 0))),
  CONSTRAINT `chk_personal_hombres_greater_equal_zero` CHECK ((`personal_hombres` >= 0)),
  CONSTRAINT `chk_personal_mujeres_greater_equal_zero` CHECK ((`personal_mujeres` >= 0)),
  CONSTRAINT `chk_personal_ocupado_total_greater_zero` CHECK ((`personal_ocupado_total` > 0)),
  CONSTRAINT `chk_personal_remunerado_greater_equal_zero` CHECK ((`personal_remunerado` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 10. Tabla: inversiones
DROP TABLE IF EXISTS `inversiones`;
CREATE TABLE `inversiones` (
  `anio` int NOT NULL,
  `id_empresa` int NOT NULL,
  `realiza_inv_red_emision_aire` tinyint DEFAULT NULL,
  `realiza_inv_evita_ruido_vibra` tinyint DEFAULT NULL,
  `realiza_inv_energia_limp` tinyint DEFAULT NULL,
  `realiza_inv_ahorro_agua` tinyint DEFAULT NULL,
  `realiza_inv_inst_med_agua` tinyint DEFAULT NULL,
  `realiza_inv_protec_suelo` tinyint DEFAULT NULL,
  `realiza_inv_disp_desechos` tinyint DEFAULT NULL,
  `realiza_otras_inv_amb` tinyint DEFAULT NULL,
  PRIMARY KEY (`anio`,`id_empresa`),
  KEY `fk_empresa_inversiones` (`id_empresa`),
  CONSTRAINT `fk_empresa_inversiones` FOREIGN KEY (`id_empresa`) REFERENCES `empresa` (`id_empresa`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_realiza_inv_ahorro_agua_bool` CHECK (((`realiza_inv_ahorro_agua` is null) or (`realiza_inv_ahorro_agua` = 1) or (`realiza_inv_ahorro_agua` = 0))),
  CONSTRAINT `chk_realiza_inv_disp_desechos_bool` CHECK (((`realiza_inv_disp_desechos` is null) or (`realiza_inv_disp_desechos` = 1) or (`realiza_inv_disp_desechos` = 0))),
  CONSTRAINT `chk_realiza_inv_energia_limp_bool` CHECK (((`realiza_inv_energia_limp` is null) or (`realiza_inv_energia_limp` = 1) or (`realiza_inv_energia_limp` = 0))),
  CONSTRAINT `chk_realiza_inv_evita_ruido_vibra_bool` CHECK (((`realiza_inv_evita_ruido_vibra` is null) or (`realiza_inv_evita_ruido_vibra` = 1) or (`realiza_inv_evita_ruido_vibra` = 0))),
  CONSTRAINT `chk_realiza_inv_inst_med_agua_bool` CHECK (((`realiza_inv_inst_med_agua` is null) or (`realiza_inv_inst_med_agua` = 1) or (`realiza_inv_inst_med_agua) = 0))),
  CONSTRAINT `chk_realiza_inv_protec_suelo_bool` CHECK (((`realiza_inv_protec_suelo` is null) or (`realiza_inv_protec_suelo` = 1) or (`realiza_inv_protec_suelo` = 0))),
  CONSTRAINT `chk_realiza_inv_red_emision_aire_bool` CHECK (((`realiza_inv_red_emision_aire` is null) or (`realiza_inv_red_emision_aire` = 1) or (`realiza_inv_red_emision_aire` = 0))),
  CONSTRAINT `chk_realiza_otras_inv_amb_bool` CHECK (((`realiza_otras_inv_amb` is null) or (`realiza_otras_inv_amb` = 1) or (`realiza_otras_inv_amb` = 0)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 11. Tabla: gastos
DROP TABLE IF EXISTS `gastos`;
CREATE TABLE `gastos` (
  `anio` int NOT NULL,
  `id_empresa` int NOT NULL,
  `gasto_gestion_amb` decimal(16,4) DEFAULT NULL,
  `gastos_totales` decimal(16,4) DEFAULT NULL,
  `imp_ind_com` decimal(16,4) DEFAULT NULL,
  `imp_otros` decimal(16,4) DEFAULT NULL,
  `gasto_personal_total` decimal(16,4) DEFAULT NULL,
  `gasto_remuneracion_personal` decimal(16,4) DEFAULT NULL,
  `gasto_servicios_publicos` decimal(16,4) DEFAULT NULL,
  `gasto_energia_electrica` decimal(16,4) DEFAULT NULL,
  `gasto_gas_natural` decimal(16,4) DEFAULT NULL,
  `realiza_gasto_red_emision_aire` tinyint DEFAULT NULL,
  `realiza_gasto_evita_ruido_vibra` tinyint DEFAULT NULL,
  `realiza_gasto_energia_limp` tinyint DEFAULT NULL,
  `realiza_gasto_ahorro_agua` tinyint DEFAULT NULL,
  `realiza_gasto_terceros_amb` tinyint DEFAULT NULL,
  `realiza_gasto_inst_med_agua` tinyint DEFAULT NULL,
  `realiza_gasto_protec_suelo` tinyint DEFAULT NULL,
  `realiza_gasto_disp_desechos` tinyint DEFAULT NULL,
  `realiza_otros_gastos_amb` tinyint DEFAULT NULL,
  PRIMARY KEY (`anio`,`id_empresa`),
  KEY `fk_empresa_gastos` (`id_empresa`),
  CONSTRAINT `fk_empresa_gastos` FOREIGN KEY (`id_empresa`) REFERENCES `empresa` (`id_empresa`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_gasto_energia_electrica_equal_zero` CHECK (((`gasto_energia_electrica` is null) or (`gasto_energia_electrica` >= 0))),
  CONSTRAINT `chk_gasto_gas_natural_equal_zero` CHECK (((`gasto_gas_natural` is null) or (`gasto_gas_natural` >= 0))),
  CONSTRAINT `chk_gasto_gestion_amb_greater_equal_zero` CHECK (((`gasto_gestion_amb` is null) or (`gasto_gestion_amb` >= 0))),
  CONSTRAINT `chk_gasto_personal_total_equal_zero` CHECK (((`gasto_personal_total` is null) or (`gasto_personal_total` >= 0))),
  CONSTRAINT `chk_gasto_remuneracion_personal_equal_zero` CHECK (((`gasto_remuneracion_personal` is null) or (`gasto_remuneracion_personal` >= 0))),
  CONSTRAINT `chk_gasto_servicios_publicos_equal_zero` CHECK (((`gasto_servicios_publicos` is null) or (`gasto_servicios_publicos` >= 0))),
  CONSTRAINT `chk_gastos_totales_equal_zero` CHECK (((`gastos_totales` is null) or (`gastos_totales` >= 0))),
  CONSTRAINT `chk_realiza_gasto_ahorro_agua_bool` CHECK (((`realiza_gasto_ahorro_agua` is null) or (`realiza_gasto_ahorro_agua` = 1) or (`realiza_gasto_ahorro_agua` = 0))),
  CONSTRAINT `chk_realiza_gasto_disp_desechos_bool` CHECK (((`realiza_gasto_disp_desechos` is null) or (`realiza_gasto_disp_desechos` = 1) or (`realiza_gasto_disp_desechos` = 0))),
  CONSTRAINT `chk_realiza_gasto_energia_limp_bool` CHECK (((`realiza_gasto_energia_limp` is null) or (`realiza_gasto_energia_limp` = 1) or (`realiza_gasto_energia_limp` = 0))),
  CONSTRAINT `chk_realiza_gasto_evita_ruido_vibra_bool` CHECK (((`realiza_gasto_evita_ruido_vibra` is null) or (`realiza_gasto_evita_ruido_vibra` = 1) or (`realiza_gasto_evita_ruido_vibra` = 0))),
  CONSTRAINT `chk_realiza_gasto_inst_med_agua_bool` CHECK (((`realiza_gasto_inst_med_agua` is null) or (`realiza_gasto_inst_med_agua` = 1) or (`realiza_gasto_inst_med_agua` = 0))),
  CONSTRAINT `chk_realiza_gasto_protec_suelo_bool` CHECK (((`realiza_gasto_protec_suelo` is null) or (`realiza_gasto_protec_suelo` = 1) or (`realiza_gasto_protec_suelo` = 0))),
  CONSTRAINT `chk_realiza_gasto_red_emision_aire_bool` CHECK (((`realiza_gasto_red_emision_aire` is null) or (`realiza_gasto_red_emision_aire` = 1) or (`realiza_gasto_red_emision_aire` = 0))),
  CONSTRAINT `chk_realiza_gasto_terceros_amb_bool` CHECK (((`realiza_gasto_terceros_amb` is null) or (`realiza_gasto_terceros_amb` = 1) or (`realiza_gasto_terceros_amb` = 0))),
  CONSTRAINT `chk_realiza_otros_gastos_amb_bool` CHECK (((`realiza_otros_gastos_amb` is null) or (`realiza_otros_gastos_amb` = 1) or (`realiza_otros_gastos_amb` = 0)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 12. Restaurar revisión de llaves foráneas
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;

-- MySQL dump 10.13  Distrib 8.0.32, for macos12.6 (arm64)
--
-- Host: ipolistingdb.civxowlytnik.ap-northeast-2.rds.amazonaws.com    Database: test_trustinv
-- ------------------------------------------------------
-- Server version	5.5.5-10.6.10-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_calendar`
--

DROP TABLE IF EXISTS `app_calendar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_calendar` (
  `ac_idx` int(11) NOT NULL AUTO_INCREMENT,
  `ci_idx` int(11) NOT NULL DEFAULT 0 COMMENT '기업id',
  `ac_sdate` varchar(50) CHARACTER SET utf8mb3 DEFAULT NULL COMMENT '일정 시작일자 (yyyy-mm-dd)',
  `ac_edate` varchar(50) CHARACTER SET utf8mb3 DEFAULT NULL COMMENT '일정 종료일자 (yyyy-mm-dd)',
  `ac_category` int(11) DEFAULT NULL COMMENT '1:청약일, 2:상장일, 3:환불일, 4:수요예측',
  `ac_category_name` varchar(50) CHARACTER SET utf8mb3 DEFAULT NULL COMMENT '구분명',
  `ac_company_name` varchar(50) CHARACTER SET utf8mb3 DEFAULT NULL COMMENT '회사명',
  `ac_vitalize` varchar(50) CHARACTER SET utf8mb3 DEFAULT NULL COMMENT 'Y:활성화, N:비활성화',
  `ac_datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`ac_idx`)
) ENGINE=InnoDB AUTO_INCREMENT=1021 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

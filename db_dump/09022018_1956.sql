CREATE DATABASE  IF NOT EXISTS `lhsmachines` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `lhsmachines`;
-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: db01.home.snowdenlabs.co.uk    Database: lhsmachines
-- ------------------------------------------------------
-- Server version	5.7.18-0ubuntu0.16.10.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `log`
--

DROP TABLE IF EXISTS `log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `useruid` varchar(45) DEFAULT NULL,
  `machineuid` varchar(45) DEFAULT NULL,
  `starttime` datetime DEFAULT NULL,
  `endtime` datetime DEFAULT NULL,
  `notes` varchar(254) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Logs for usage';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log`
--

LOCK TABLES `log` WRITE;
/*!40000 ALTER TABLE `log` DISABLE KEYS */;
/*!40000 ALTER TABLE `log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `machine`
--

DROP TABLE IF EXISTS `machine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `machine` (
  `machineuid` varchar(45) NOT NULL,
  `machinename` varchar(45) NOT NULL,
  `creator` varchar(45) NOT NULL,
  `status` tinyint(4) DEFAULT '1',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `machineuid_UNIQUE` (`machineuid`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COMMENT='Machines in the space';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `machine`
--

LOCK TABLES `machine` WRITE;
/*!40000 ALTER TABLE `machine` DISABLE KEYS */;
INSERT INTO `machine` VALUES ('5508fdbe-6dcf-4461-ab6d-3d966e888f47','test_1','API',1,1),('92fdf225-56f8-4edb-a80e-7e0c1294998c','test_0','API',1,2),('f35ebefe-b8ae-457e-8f62-a48a5266f3ae','test_2','API',1,3),('af607c7b-2a66-49c4-b8bd-555846d93ebc','laser cutter','API',1,4);
/*!40000 ALTER TABLE `machine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `canuse` tinyint(4) DEFAULT '0',
  `caninduct` tinyint(4) DEFAULT '0',
  `creator` varchar(45) DEFAULT NULL,
  `machineuid` varchar(45) NOT NULL,
  `useruid` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `machineuid_idx` (`machineuid`),
  KEY `useruid_idx` (`useruid`),
  CONSTRAINT `machineuid` FOREIGN KEY (`machineuid`) REFERENCES `machine` (`machineuid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `useruid` FOREIGN KEY (`useruid`) REFERENCES `user` (`useruid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1 COMMENT='Correlate many users to many machines';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission`
--

LOCK TABLES `permission` WRITE;
/*!40000 ALTER TABLE `permission` DISABLE KEYS */;
INSERT INTO `permission` VALUES (1,1,1,'API','92fdf225-56f8-4edb-a80e-7e0c1294998c','e2602845-df21-4e22-b15c-4eac0df9f405'),(2,1,1,'API','5508fdbe-6dcf-4461-ab6d-3d966e888f47','b9772cb7-82f3-46c9-8bcf-ddda5c1bbcd6'),(3,1,1,'API','5508fdbe-6dcf-4461-ab6d-3d966e888f47','8449974c-0884-48d7-a529-f87cf0b8d37e'),(4,0,0,'API','f35ebefe-b8ae-457e-8f62-a48a5266f3ae','b9772cb7-82f3-46c9-8bcf-ddda5c1bbcd6'),(5,0,0,'API','92fdf225-56f8-4edb-a80e-7e0c1294998c','e2602845-df21-4e22-b15c-4eac0df9f405'),(6,1,1,'API','92fdf225-56f8-4edb-a80e-7e0c1294998c','b9772cb7-82f3-46c9-8bcf-ddda5c1bbcd6'),(7,1,0,'API','af607c7b-2a66-49c4-b8bd-555846d93ebc','8449974c-0884-48d7-a529-f87cf0b8d37e'),(10,1,0,'API','5508fdbe-6dcf-4461-ab6d-3d966e888f47','06bf54a3-dd90-4dfd-9ec9-c4c279c03ab5');
/*!40000 ALTER TABLE `permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `useruid` varchar(45) DEFAULT NULL,
  `carduid` varchar(45) DEFAULT NULL,
  `username` varchar(45) DEFAULT NULL,
  `valid` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `usuerid_UNIQUE` (`useruid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COMMENT='Users of machines.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'e2602845-df21-4e22-b15c-4eac0df9f405','test_0','test_u_0',1),(2,'8449974c-0884-48d7-a529-f87cf0b8d37e','test_1','test_u_1',1),(3,'b9772cb7-82f3-46c9-8bcf-ddda5c1bbcd6','fiuoifjoiewfowofeewfj','test_u_2',1),(4,'06bf54a3-dd90-4dfd-9ec9-c4c279c03ab5','6422D29A','AD',1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-02-09 19:56:40

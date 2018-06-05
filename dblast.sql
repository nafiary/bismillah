-- MySQL dump 10.15  Distrib 10.0.34-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	10.0.34-MariaDB-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `devices`
--

DROP TABLE IF EXISTS `devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `devices` (
  `id` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices`
--

LOCK TABLES `devices` WRITE;
/*!40000 ALTER TABLE `devices` DISABLE KEYS */;
INSERT INTO `devices` VALUES ('109cd43383a24da59aab7dc69974ada2','routeros','routeros','localhost','172.28.128.3'),('3db4a9fc54a24771bfd2da7882d6b5c9','mikrotik AJK','Switch','Lab. AJK Dept. Informatika ITS','10.151.36.3');
/*!40000 ALTER TABLE `devices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oid`
--

DROP TABLE IF EXISTS `oid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oid` (
  `id` varchar(255) NOT NULL,
  `oid` varchar(255) DEFAULT NULL,
  `oidname` varchar(255) DEFAULT NULL,
  `devices_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_devices_has_oid_idx` (`devices_id`),
  CONSTRAINT `fk_devices_has_oid` FOREIGN KEY (`devices_id`) REFERENCES `devices` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oid`
--

LOCK TABLES `oid` WRITE;
/*!40000 ALTER TABLE `oid` DISABLE KEYS */;
INSERT INTO `oid` VALUES ('00376f6d3df0467ead0fcb1b82a8ac8b','.1.3.6.1.4.1.14988.1.1.7.6.0','build-time','109cd43383a24da59aab7dc69974ada2'),('1fc175a7b1fe49709d4f617aad9d17dc','.1.3.6.1.4.1.14988.1.1.3.10.0','temperature:','3db4a9fc54a24771bfd2da7882d6b5c9'),('28d637470d854abd87175f33fe9bac03','.1.3.6.1.4.1.14988.1.1.3.11.0','processor-temperature:','3db4a9fc54a24771bfd2da7882d6b5c9'),('2d468d3824484afcadf9526aff43ff0b','.1.3.6.1.2.1.25.2.3.1.6.65536','used-memory','109cd43383a24da59aab7dc69974ada2'),('78580753482b4489b74dda4cc3ea641e','.1.3.6.1.2.1.25.2.3.1.6.65536','used-memory','3db4a9fc54a24771bfd2da7882d6b5c9'),('78fb767fe14f4c0b86031d68cb256654','.1.3.6.1.4.1.14988.1.1.3.8.0','voltage:','3db4a9fc54a24771bfd2da7882d6b5c9'),('7c50bcec2c1b4b329374fe74a536e303','.1.3.6.1.4.1.14988.1.1.3.15.0','psu1-state:','3db4a9fc54a24771bfd2da7882d6b5c9'),('94198653980c42a6a2ae7d54037d9de1','.1.3.6.1.2.1.25.2.3.1.5.65536','total-memory','3db4a9fc54a24771bfd2da7882d6b5c9'),('980da17241d54050bc54c75af1fc19e9','.1.3.6.1.2.1.1.3.0','uptime','3db4a9fc54a24771bfd2da7882d6b5c9'),('a7c8ffa56ef0448582dbaba5d7b952ae','.1.3.6.1.2.1.1.3.0','uptime','109cd43383a24da59aab7dc69974ada2'),('b7729bcdc1ec4844995ded00e4f06811','.1.3.6.1.4.1.14988.1.1.7.6.0','build-time','3db4a9fc54a24771bfd2da7882d6b5c9'),('be0f90beac084e0ca0dc0ec769c3fb8a','.1.3.6.1.4.1.14988.1.1.3.13.0','current:','3db4a9fc54a24771bfd2da7882d6b5c9'),('c1cf4ceac8ef4e778ce8cc20e4dc2cff','.1.3.6.1.4.1.14988.1.1.3.12.0','power-consumption:','3db4a9fc54a24771bfd2da7882d6b5c9'),('cac0dbb3ce0644ae95f0aa7e36dc6e19','.1.3.6.1.4.1.14988.1.1.3.14.0','cpu-frequency','109cd43383a24da59aab7dc69974ada2'),('d263f066fa5c4038b6cfe151dc110fe5','.1.3.6.1.4.1.14988.1.1.3.9.0','active-fan:','3db4a9fc54a24771bfd2da7882d6b5c9'),('eec3c8f8bf97419cbb657fd9886ec50e','.1.3.6.1.2.1.25.2.3.1.5.65536','total-memory','109cd43383a24da59aab7dc69974ada2'),('f88da32c351c4cfe84a8b73a954a4db6','.1.3.6.1.4.1.14988.1.1.3.16.0','psu2-state:','3db4a9fc54a24771bfd2da7882d6b5c9'),('ffba24063c03487c881d9a352a2b289d','.1.3.6.1.4.1.14988.1.1.3.14.0','cpu-frequency','3db4a9fc54a24771bfd2da7882d6b5c9');
/*!40000 ALTER TABLE `oid` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subscribe`
--

DROP TABLE IF EXISTS `subscribe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subscribe` (
  `users_id` varchar(255) NOT NULL,
  `devices_id` varchar(255) NOT NULL,
  PRIMARY KEY (`users_id`,`devices_id`),
  KEY `fk_users_has_devices_devices1_idx` (`devices_id`),
  KEY `fk_users_has_devices_users_idx` (`users_id`),
  CONSTRAINT `fk_users_has_devices_devices1` FOREIGN KEY (`devices_id`) REFERENCES `devices` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_devices_users` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subscribe`
--

LOCK TABLES `subscribe` WRITE;
/*!40000 ALTER TABLE `subscribe` DISABLE KEYS */;
INSERT INTO `subscribe` VALUES ('fe22164846b44cf7a754daba587797bb','109cd43383a24da59aab7dc69974ada2'),('fe22164846b44cf7a754daba587797bb','3db4a9fc54a24771bfd2da7882d6b5c9');
/*!40000 ALTER TABLE `subscribe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subscribeoid`
--

DROP TABLE IF EXISTS `subscribeoid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subscribeoid` (
  `users_id` varchar(255) NOT NULL,
  `oid_id` varchar(255) NOT NULL,
  PRIMARY KEY (`users_id`,`oid_id`),
  KEY `fk_users_has_oid_oid1_idx` (`oid_id`),
  CONSTRAINT `fk_users_has_oid_oid1` FOREIGN KEY (`oid_id`) REFERENCES `oid` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_oid_users` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subscribeoid`
--

LOCK TABLES `subscribeoid` WRITE;
/*!40000 ALTER TABLE `subscribeoid` DISABLE KEYS */;
INSERT INTO `subscribeoid` VALUES ('fe22164846b44cf7a754daba587797bb','00376f6d3df0467ead0fcb1b82a8ac8b'),('fe22164846b44cf7a754daba587797bb','2d468d3824484afcadf9526aff43ff0b'),('fe22164846b44cf7a754daba587797bb','94198653980c42a6a2ae7d54037d9de1'),('fe22164846b44cf7a754daba587797bb','980da17241d54050bc54c75af1fc19e9'),('fe22164846b44cf7a754daba587797bb','a7c8ffa56ef0448582dbaba5d7b952ae'),('fe22164846b44cf7a754daba587797bb','c1cf4ceac8ef4e778ce8cc20e4dc2cff'),('fe22164846b44cf7a754daba587797bb','cac0dbb3ce0644ae95f0aa7e36dc6e19'),('fe22164846b44cf7a754daba587797bb','eec3c8f8bf97419cbb657fd9886ec50e'),('fe22164846b44cf7a754daba587797bb','ffba24063c03487c881d9a352a2b289d');
/*!40000 ALTER TABLE `subscribeoid` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('6492b35ad39844b5849718e987f0a9d5','afif2@afif.com','afif2','testuser2','58dd024d49e1d1b83a5d307f09f32734','user'),('fe22164846b44cf7a754daba587797bb','afif@afif.com','afif','testuser','5d9c68c6c50ed3d02a2fcf54f63993b6','admin');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-05 14:34:24

-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: vibecheck
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$600000$aZOmwEyitufQeCdvnBEB8y$e+0y/cVzmtZEuujWKcCrEEJU+KOHsWm1kf13Qr0GcL0=','2025-10-14 12:08:50.713124',0,'masa','','','masa@gmail.com',0,1,'2025-10-12 20:26:43.105950'),(2,'pbkdf2_sha256$600000$H1SFEiqdgYTp21jrZtQGdx$14Y/h5V1U+Iv8UVJP+4L93t0CH8pnZLXZxvZz2XnvLY=','2025-10-14 12:12:49.425882',0,'dusan','','','dusan@gmail.com',0,1,'2025-10-12 20:26:54.547400'),(3,'pbkdf2_sha256$600000$uQNsnS0pzaNLdPHWqI8FtT$/4SaU8DYk2bpIa2jp/80OBsrF+WnqZy5ozK8qYwC7v0=','2025-10-13 14:46:05.199395',0,'nikola','','','nikola@gmail.com',0,1,'2025-10-12 20:27:05.328772'),(4,'pbkdf2_sha256$600000$pPo5s9HnZqgzCva44YUn6u$28ZM6KaLUoWGESYcpd1zGZuz+IpyljnAgb8Tho4B0Xg=','2025-10-14 01:29:04.122784',0,'ana','','','ana@gmail.com',0,1,'2025-10-12 20:27:15.927068'),(5,'pbkdf2_sha256$600000$zBvjfRcnxfyKSre497913r$FrnMlu6upQ6O406OyqcaPljqYNUFy2apaHux80OIzZI=','2025-10-14 01:29:33.355959',0,'luka','','','luka@gmail.com',0,1,'2025-10-12 20:27:27.866635'),(6,'pbkdf2_sha256$600000$Uq9z1ovqjgumu8Be6X4Jo9$EKDtFmCLCqBOJh8gCR7Qn25mpqHljENdlB7gfg5Phic=','2025-10-12 23:05:36.912907',0,'zika','','','zika@gmail.com',0,1,'2025-10-12 23:05:36.029182'),(7,'pbkdf2_sha256$600000$qRLhNDgkusAYryER1vXw6X$bM+CsqmD4BlXqPOSF327NkfeG164w5hJQt/BDEn7Fxw=','2025-10-14 01:30:04.115875',0,'moderator','','','moderator@gmail.com',0,1,'2025-10-12 23:23:06.668672'),(8,'pbkdf2_sha256$600000$rAZDk1lkaWd6fwhE77h2QU$U0RuZ8ttaTvp37TpTVrUv9ICjdiUifs5wW0Wry7V9AE=','2025-10-13 01:04:22.864191',0,'admin','','','admin@gmail.com',0,1,'2025-10-13 01:03:59.239570');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-14 14:31:23

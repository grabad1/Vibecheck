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
-- Table structure for table `collab`
--

DROP TABLE IF EXISTS `collab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `collab` (
  `idcollab` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `iduser` int NOT NULL,
  `idplaylist` int DEFAULT NULL,
  `status` varchar(45) NOT NULL,
  PRIMARY KEY (`idcollab`),
  KEY `collab_ibfk_1` (`iduser`),
  KEY `collab_ibfk_2` (`idplaylist`),
  CONSTRAINT `collab_ibfk_1` FOREIGN KEY (`iduser`) REFERENCES `user` (`idUser`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `collab_ibfk_2` FOREIGN KEY (`idplaylist`) REFERENCES `playlist` (`idplaylist`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `collab`
--

LOCK TABLES `collab` WRITE;
/*!40000 ALTER TABLE `collab` DISABLE KEYS */;
INSERT INTO `collab` VALUES (1,'Summer mix',1,1,'active'),(2,'Collab',2,2,'active'),(3,'Zdravko Colic mix',7,3,'active'),(4,'Cola mix',2,4,'active'),(5,'Summer mix',7,5,'active'),(6,'Svadba mix',7,6,'active'),(7,'Mnogo jak mix',2,7,'active'),(8,'VibeCheck mix',3,8,'active'),(9,'ETF collab',2,9,'active'),(10,'Study playlist',7,10,'active'),(11,'Summer 2016',7,11,'active');
/*!40000 ALTER TABLE `collab` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-14 14:31:19

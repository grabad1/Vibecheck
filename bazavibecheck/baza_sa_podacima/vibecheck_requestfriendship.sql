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
-- Table structure for table `requestfriendship`
--

DROP TABLE IF EXISTS `requestfriendship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `requestfriendship` (
  `idrf` int NOT NULL AUTO_INCREMENT,
  `idusersend` int NOT NULL,
  `iduserrecieve` int NOT NULL,
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`idrf`),
  UNIQUE KEY `unique_friend_request` (`idusersend`,`iduserrecieve`),
  KEY `requestfriendship_ibfk_2` (`iduserrecieve`),
  CONSTRAINT `requestfriendship_ibfk_1` FOREIGN KEY (`idusersend`) REFERENCES `user` (`idUser`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `requestfriendship_ibfk_2` FOREIGN KEY (`iduserrecieve`) REFERENCES `user` (`idUser`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `requestfriendship`
--

LOCK TABLES `requestfriendship` WRITE;
/*!40000 ALTER TABLE `requestfriendship` DISABLE KEYS */;
INSERT INTO `requestfriendship` VALUES (1,5,1,'2025-10-13 16:42:35'),(2,5,2,'2025-10-13 16:42:35'),(3,2,1,'2025-10-13 16:42:35'),(4,1,3,'2025-10-13 16:42:35'),(5,1,4,'2025-10-13 16:42:35'),(6,4,2,'2025-10-13 16:42:35'),(7,3,2,'2025-10-13 14:46:17');
/*!40000 ALTER TABLE `requestfriendship` ENABLE KEYS */;
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

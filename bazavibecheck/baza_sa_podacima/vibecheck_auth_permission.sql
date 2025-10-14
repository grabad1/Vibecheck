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
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add collab',7,'add_collab'),(26,'Can change collab',7,'change_collab'),(27,'Can delete collab',7,'delete_collab'),(28,'Can view collab',7,'view_collab'),(29,'Can add contains',8,'add_contains'),(30,'Can change contains',8,'change_contains'),(31,'Can delete contains',8,'delete_contains'),(32,'Can view contains',8,'view_contains'),(33,'Can add created',9,'add_created'),(34,'Can change created',9,'change_created'),(35,'Can delete created',9,'delete_created'),(36,'Can view created',9,'view_created'),(37,'Can add friendship',10,'add_friendship'),(38,'Can change friendship',10,'change_friendship'),(39,'Can delete friendship',10,'delete_friendship'),(40,'Can view friendship',10,'view_friendship'),(41,'Can add liked',11,'add_liked'),(42,'Can change liked',11,'change_liked'),(43,'Can delete liked',11,'delete_liked'),(44,'Can view liked',11,'view_liked'),(45,'Can add participated',12,'add_participated'),(46,'Can change participated',12,'change_participated'),(47,'Can delete participated',12,'delete_participated'),(48,'Can view participated',12,'view_participated'),(49,'Can add playlist',13,'add_playlist'),(50,'Can change playlist',13,'change_playlist'),(51,'Can delete playlist',13,'delete_playlist'),(52,'Can view playlist',13,'view_playlist'),(53,'Can add purchased',14,'add_purchased'),(54,'Can change purchased',14,'change_purchased'),(55,'Can delete purchased',14,'delete_purchased'),(56,'Can view purchased',14,'view_purchased'),(57,'Can add rated',15,'add_rated'),(58,'Can change rated',15,'change_rated'),(59,'Can delete rated',15,'delete_rated'),(60,'Can view rated',15,'view_rated'),(61,'Can add requestcollab',16,'add_requestcollab'),(62,'Can change requestcollab',16,'change_requestcollab'),(63,'Can delete requestcollab',16,'delete_requestcollab'),(64,'Can view requestcollab',16,'view_requestcollab'),(65,'Can add requestfriendship',17,'add_requestfriendship'),(66,'Can change requestfriendship',17,'change_requestfriendship'),(67,'Can delete requestfriendship',17,'delete_requestfriendship'),(68,'Can view requestfriendship',17,'view_requestfriendship'),(69,'Can add user',18,'add_user'),(70,'Can change user',18,'change_user'),(71,'Can delete user',18,'delete_user'),(72,'Can view user',18,'view_user'),(73,'Can add song',19,'add_song'),(74,'Can change song',19,'change_song'),(75,'Can delete song',19,'delete_song'),(76,'Can view song',19,'view_song'),(77,'Can add auth user',20,'add_authuser'),(78,'Can change auth user',20,'change_authuser'),(79,'Can delete auth user',20,'delete_authuser'),(80,'Can view auth user',20,'view_authuser');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-14 14:31:22

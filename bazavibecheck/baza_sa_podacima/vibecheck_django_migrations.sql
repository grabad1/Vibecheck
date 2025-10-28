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
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-10-12 20:26:24.484290'),(2,'auth','0001_initial','2025-10-12 20:26:25.509215'),(3,'admin','0001_initial','2025-10-12 20:26:25.758806'),(4,'admin','0002_logentry_remove_auto_add','2025-10-12 20:26:25.770815'),(5,'admin','0003_logentry_add_action_flag_choices','2025-10-12 20:26:25.779885'),(6,'app','0001_initial','2025-10-12 20:26:25.821362'),(7,'contenttypes','0002_remove_content_type_name','2025-10-12 20:26:25.959235'),(8,'auth','0002_alter_permission_name_max_length','2025-10-12 20:26:26.073869'),(9,'auth','0003_alter_user_email_max_length','2025-10-12 20:26:26.138884'),(10,'auth','0004_alter_user_username_opts','2025-10-12 20:26:26.160833'),(11,'auth','0005_alter_user_last_login_null','2025-10-12 20:26:26.263860'),(12,'auth','0006_require_contenttypes_0002','2025-10-12 20:26:26.275062'),(13,'auth','0007_alter_validators_add_error_messages','2025-10-12 20:26:26.275062'),(14,'auth','0008_alter_user_username_max_length','2025-10-12 20:26:26.430194'),(15,'auth','0009_alter_user_last_name_max_length','2025-10-12 20:26:26.565507'),(16,'auth','0010_alter_group_name_max_length','2025-10-12 20:26:26.597351'),(17,'auth','0011_update_proxy_permissions','2025-10-12 20:26:26.614138'),(18,'auth','0012_alter_user_first_name_max_length','2025-10-12 20:26:26.729581'),(19,'sessions','0001_initial','2025-10-12 20:26:26.780847'),(20,'app','0002_alter_song_options','2025-10-12 20:36:33.944604'),(21,'app','0003_authuser_alter_song_table','2025-10-12 20:42:06.149764'),(22,'app','0003_alter_collab_options_alter_contains_options_and_more','2025-10-12 20:53:29.811572');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-14 14:31:21

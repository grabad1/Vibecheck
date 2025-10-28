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
-- Table structure for table `song`
--

DROP TABLE IF EXISTS `song`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `song` (
  `idsong` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `link` varchar(150) NOT NULL,
  `artist` varchar(45) DEFAULT NULL,
  `imagelink` varchar(150) DEFAULT NULL,
  `duration` int DEFAULT NULL,
  `spotify_id` varchar(50) NOT NULL,
  `duration_string` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idsong`),
  UNIQUE KEY `spotify_id` (`spotify_id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `song`
--

LOCK TABLES `song` WRITE;
/*!40000 ALTER TABLE `song` DISABLE KEYS */;
INSERT INTO `song` VALUES (1,'Amsterdam','https://open.spotify.com/track/101Ld2iuMawwXn7UxRLpPB','Devito','https://i.scdn.co/image/ab67616d0000b2736c1e36348c017ee52b46b016',165000,'101Ld2iuMawwXn7UxRLpPB','2:45'),(2,'Leto je','https://open.spotify.com/track/5I6Uk4mipkEYGPRs2BAqeX','Coby','https://i.scdn.co/image/ab67616d0000b27337f1918c67efa361f535bf4d',196097,'5I6Uk4mipkEYGPRs2BAqeX','3:16'),(3,'Mangio Pasta','https://open.spotify.com/track/51oT6N6dMwTnBfhpmIAsb1','Peki','https://i.scdn.co/image/ab67616d0000b273aa84d9ff9dec6159a45beaa5',170909,'51oT6N6dMwTnBfhpmIAsb1','2:50'),(4,'Mjerkam te, mjerkam','https://open.spotify.com/track/0UD3FJrTmTrUSx2mH6TeOi','Zdravko Čolić','https://i.scdn.co/image/ab67616d0000b2736963869516694dcbe2f6165b',311013,'0UD3FJrTmTrUSx2mH6TeOi','5:11'),(5,'Juznjaci','https://open.spotify.com/track/4Ol7EQZWm9jGK8nr0VViZG','Zdravko Čolić','https://i.scdn.co/image/ab67616d0000b27378bdc249759a8313ec27f77a',226716,'4Ol7EQZWm9jGK8nr0VViZG','3:46'),(6,'Tebe cuvam za kraj','https://open.spotify.com/track/3t2gJRsUpF3Ip9sn5yvpAd','Zdravko Čolić','https://i.scdn.co/image/ab67616d0000b273d7d4c42b6b6c78fd6b58d478',245586,'3t2gJRsUpF3Ip9sn5yvpAd','4:05'),(7,'Noć Mi Te Duguje','https://open.spotify.com/track/2WylXcEyRT6NjT128RrZyW','Zdravko Čolić','https://i.scdn.co/image/ab67616d0000b273ce6c8a5c513d76df700c13c4',293920,'2WylXcEyRT6NjT128RrZyW','4:53'),(8,'Živiš U Oblacima','https://open.spotify.com/track/6EkUNTYAHGyaCIK0P64XAA','Zdravko Čolić','https://i.scdn.co/image/ab67616d0000b273ce6c8a5c513d76df700c13c4',236773,'6EkUNTYAHGyaCIK0P64XAA','3:56'),(9,'Prolaze neke slike','https://open.spotify.com/track/5nOMF3Ia4GNZAgvsCL2GDP','Zdravko Čolić','https://i.scdn.co/image/ab67616d0000b273c9cf052fc0d614c0f6bc118f',253866,'5nOMF3Ia4GNZAgvsCL2GDP','4:13'),(10,'Pisaću Joj Pisma Duga','https://open.spotify.com/track/3AbUaLGttiWrtIrsdZUq5R','Zdravko Čolić','https://i.scdn.co/image/ab67616d0000b273ce6c8a5c513d76df700c13c4',207093,'3AbUaLGttiWrtIrsdZUq5R','3:27'),(11,'Sto puta','https://open.spotify.com/track/2k3duoPFZ2Yjfr4OANtSA4','Zdravko Čolić','https://i.scdn.co/image/ab67616d0000b27300d8309b2a18f8eccf128909',278973,'2k3duoPFZ2Yjfr4OANtSA4','4:38'),(12,'Ego','https://open.spotify.com/track/52ntJFD36hYDcdIUFpWPSR','Devito','https://i.scdn.co/image/ab67616d0000b2736c1e36348c017ee52b46b016',222500,'52ntJFD36hYDcdIUFpWPSR','3:42'),(13,'Svadbarskim sokakom','https://open.spotify.com/track/2RTDW0auwq7Idop7CgAQDv','Zdravko Čolić','https://i.scdn.co/image/ab67616d0000b27300d8309b2a18f8eccf128909',308440,'2RTDW0auwq7Idop7CgAQDv','5:08'),(14,'Svadba, Svadba','https://open.spotify.com/track/1GQWGVhQ3led9KvOyjjQQa','Kanarinac','https://i.scdn.co/image/ab67616d0000b27304d97004b926d0b657171757',197851,'1GQWGVhQ3led9KvOyjjQQa','3:17'),(15,'Anđeo - From \"Sram\"','https://open.spotify.com/track/4w6fEGrluheE0MtiPUe0hJ','Miach','https://i.scdn.co/image/ab67616d0000b273b6927fe0569d67f110057837',175714,'4w6fEGrluheE0MtiPUe0hJ','2:55'),(16,'Led','https://open.spotify.com/track/0qfXdlT31rZqueog9ztqZu','Miach','https://i.scdn.co/image/ab67616d0000b2736247c20a5200937876b3f543',210461,'0qfXdlT31rZqueog9ztqZu','3:30'),(17,'Reci mi da znam','https://open.spotify.com/track/3KzTUtfq82dkVOTqMyy2xM','Vlado Georgiev','https://i.scdn.co/image/ab67616d0000b273aaa6cc447839dc9ed7437f5e',307386,'3KzTUtfq82dkVOTqMyy2xM','5:07'),(18,'Zbogom ljubavi','https://open.spotify.com/track/2EWejibEQ8aAYTKwqJCZ4k','Vlado Georgiev','https://i.scdn.co/image/ab67616d0000b273aaa6cc447839dc9ed7437f5e',275506,'2EWejibEQ8aAYTKwqJCZ4k','4:35'),(19,'Blago Onom Tko Te Ima','https://open.spotify.com/track/4ysRdCUZEloDWTZ6v0s9BE','Tony Cetinski','https://i.scdn.co/image/ab67616d0000b2734c5b5b7985891d1165f2618b',205101,'4ysRdCUZEloDWTZ6v0s9BE','3:25'),(20,'Mozart : Requiem K. 626 - Lacrimosa','https://open.spotify.com/track/3hj6jHDmZfoQdukMi6bWF6','Wolfgang Amadeus Mozart','https://i.scdn.co/image/ab67616d0000b2738ea6e00ea3edc44ffe6e20d1',183813,'3hj6jHDmZfoQdukMi6bWF6','3:03'),(21,'Study Focus Loop Noise (Loopable no fade)','https://open.spotify.com/track/5avw86fNvFagKYJBz9l91v','Dream Supplier','https://i.scdn.co/image/ab67616d0000b273185ca0219b7b5bc54ba23640',142222,'5avw86fNvFagKYJBz9l91v','2:22'),(22,'Study Space','https://open.spotify.com/track/6m5h70i2No4eOlhbTgW9m0','Brainy','https://i.scdn.co/image/ab67616d0000b273b40fc8c2c5206a21d744f0b0',148000,'6m5h70i2No4eOlhbTgW9m0','2:28'),(23,'Study Frequency','https://open.spotify.com/track/0eDwatRumjwh9mlGhAMzPs','Hz Frequency Zone','https://i.scdn.co/image/ab67616d0000b2737c87ee5e14ffd98838b8aa3f',222203,'0eDwatRumjwh9mlGhAMzPs','3:42'),(24,'Study Music','https://open.spotify.com/track/1UIIAv5BBLLYuXbk1DzipG','Study Music & Sounds','https://i.scdn.co/image/ab67616d0000b2736f9b00223f610abc43fa95db',125592,'1UIIAv5BBLLYuXbk1DzipG','2:05'),(25,'Despacito','https://open.spotify.com/track/6habFhsOp2NvshLv26DqMb','Luis Fonsi','https://i.scdn.co/image/ab67616d0000b273ef0d4234e1a645740f77d59c',229360,'6habFhsOp2NvshLv26DqMb','3:49'),(26,'Shape of You','https://open.spotify.com/track/7qiZfU4dY1lWllzX7mPBI3','Ed Sheeran','https://i.scdn.co/image/ab67616d0000b273ba5db46f4b838ef6027e6f96',233712,'7qiZfU4dY1lWllzX7mPBI3','3:53');
/*!40000 ALTER TABLE `song` ENABLE KEYS */;
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

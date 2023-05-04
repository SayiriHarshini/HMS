-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: hostel
-- ------------------------------------------------------
-- Server version	8.0.32

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
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `Userid` varchar(7) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `conformpassword` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES ('5154','harpuj','har@7','har@7'),('5154','harpuj','har@7','har@7');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `records`
--

DROP TABLE IF EXISTS `records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `records` (
  `id` int NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `Course` varchar(50) DEFAULT NULL,
  `Roomno` int DEFAULT NULL,
  `Mobileno` bigint DEFAULT NULL,
  `checkin` datetime DEFAULT NULL,
  `checkout` datetime DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Studentid` (`id`),
  CONSTRAINT `records_ibfk_1` FOREIGN KEY (`id`) REFERENCES `student` (`Studentid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `records`
--

LOCK TABLES `records` WRITE;
/*!40000 ALTER TABLE `records` DISABLE KEYS */;
INSERT INTO `records` VALUES (506,'mahi','PG',6,80008727276,'2023-04-27 17:01:54','2023-04-27 17:08:57','2023-04-27'),(1020,'sayiri','b.sc[mscs]',4,7993691445,'2023-04-27 16:51:22','2023-04-27 17:10:50','2023-04-27'),(6789,'puji','mtech',5,6558794578,'2023-04-27 17:10:39','2023-04-29 09:30:06','2023-04-27'),(19992,'sandhya','btech',1,7337237554,'2023-04-27 16:39:54',NULL,'2023-04-27'),(206137,'B.Prasanna','b.sc',10,9014495554,'2023-04-27 16:31:45',NULL,'2023-04-27'),(206150,'rocky','mtech',12,9553784236,NULL,NULL,'2023-04-27'),(206151,'R.Pujitha','b.sc',11,99499147365,NULL,NULL,'2023-04-27'),(206153,'R.Santhoshi','b.sc',1,2567568456,NULL,NULL,'2023-04-27'),(206154,'s.harshini','b.sc',12,6305000625,NULL,NULL,'2023-04-27');
/*!40000 ALTER TABLE `records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `Studentid` int NOT NULL,
  `Studentname` varchar(50) DEFAULT NULL,
  `Course` varchar(20) DEFAULT NULL,
  `Roomno` int DEFAULT NULL,
  `Mobileno` bigint DEFAULT NULL,
  `Email` varchar(150) DEFAULT NULL,
  `Address` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`Studentid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (506,'mahi','PG',6,80008727276,'mahi@gmail.com','vij'),(1020,'sayiri','b.sc[mscs]',4,7993691445,'sayiri@gmail.com','viz'),(6789,'puji','mtech',5,6558794578,'puji@gmail.com','vij'),(19992,'sandhya','btech',1,7337237554,'sandhya@gamil.com','hyb'),(206137,'B.Prasanna','b.sc',10,9014495554,'prasanna@gmail.com','IBM'),(206150,'rocky','mtech',12,9553784236,'rocky@gmail.com','kondapalli'),(206151,'R.Pujitha','b.sc',11,99499147365,'pujitharella@gmail.com','vij'),(206153,'R.Santhoshi','b.sc',1,2567568456,'sayiriharshini@gmail.com','hffj'),(206154,'s.harshini','b.sc',12,6305000625,'sayiriharshini@gmail.com','kondapalli');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `visitor`
--

DROP TABLE IF EXISTS `visitor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `visitor` (
  `name` varchar(50) DEFAULT NULL,
  `Studentid` int DEFAULT NULL,
  `checkin` timestamp NULL DEFAULT NULL,
  `checkout` timestamp NULL DEFAULT NULL,
  `mobilenumber` varchar(10) DEFAULT NULL,
  KEY `Id` (`Studentid`),
  CONSTRAINT `visitor_ibfk_1` FOREIGN KEY (`Studentid`) REFERENCES `student` (`Studentid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `visitor`
--

LOCK TABLES `visitor` WRITE;
/*!40000 ALTER TABLE `visitor` DISABLE KEYS */;
INSERT INTO `visitor` VALUES ('rama',206151,'2023-04-27 13:57:28','2023-04-27 13:57:25','994961768'),('s.Rambabu',206154,NULL,NULL,'8008727176'),('srinu',206151,'2023-04-27 13:57:28','2023-04-27 13:57:25','6706578956');
/*!40000 ALTER TABLE `visitor` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-29 19:42:59

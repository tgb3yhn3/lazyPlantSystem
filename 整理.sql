DROP TABLE IF EXISTS `sensor`;
DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensor` (
  `no` int NOT NULL AUTO_INCREMENT,
  `humidity` varchar(45) COLLATE utf8mb4_bin DEFAULT NULL,
  `temperature` varchar(45) COLLATE utf8mb4_bin DEFAULT NULL,
  `soilHumidity` varchar(45) COLLATE utf8mb4_bin DEFAULT 'CURRENT_TIMESTAMP',
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`no`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='for IOTclass';
CREATE TABLE `event` (
  `no` int NOT NULL AUTO_INCREMENT,
  `event` varchar(45) COLLATE utf8mb4_bin DEFAULT NULL,
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`no`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='for IOTclass';
ALTER TABLE sensor AUTO_INCREMENT = 1;
select * from sensor;
select * from event;
 select * from sensor where time='2022-05-30 20:59:00';
 select * from sensor where time between CONVERT( '2022-05-30 20:55:33',DATETIME
        )and CONVERT( '2022-05-30 21:00:33',DATETIME
        ) ;
         
       
        
CREATE TABLE `ticket` (
  `ticket_id` int NOT NULL AUTO_INCREMENT,
  `subject` varchar(255) NOT NULL,
  `description` text,
  `status` enum('Open','In Progress','Closed') DEFAULT 'Open',
  `priority` enum('Low','Medium','High') DEFAULT 'Medium',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` int DEFAULT NULL COMMENT 'this user is who receive ticket first',
  `read_at` timestamp NULL DEFAULT NULL COMMENT 'it shows which date and time this ticket opened and read',
  `note` varchar(255) DEFAULT NULL COMMENT 'paraph shows which command follow with this ticket by supervisor or holder of this ticket',
  `topic` varchar(80) DEFAULT NULL COMMENT 'group for receiver group department when sender knows respond group',
  `attachment` tinyint(1) DEFAULT NULL COMMENT 'it shows this ticket has attachment or not',
  `type_id` int DEFAULT NULL COMMENT 'this shows which category this ticket belongs',
  `end_date` timestamp NULL DEFAULT NULL COMMENT 'due date to respond ticket ',
  `score` int DEFAULT NULL,
  PRIMARY KEY (`ticket_id`,`subject`),
  KEY `user_id` (`user_id`),
  KEY `type_id` (`type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `ticket_dictionary` (
  `type_id` int NOT NULL AUTO_INCREMENT,
  `type_name` varchar(50) NOT NULL,
  `description` text,
  `priority` enum('Low','Medium','High') DEFAULT 'Medium',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`type_id`),
  CONSTRAINT `ticket_types_fk1` FOREIGN KEY (`type_id`) REFERENCES `ticket` (`ticket_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `role_id` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `ticket_interaction` (
  `interaction_id` int NOT NULL AUTO_INCREMENT,
  `ticket_id` int NOT NULL,
  `interaction_type` enum('Message','Assignment') NOT NULL,
  `sender_id` int DEFAULT NULL,
  `receiver_id` int DEFAULT NULL,
  `content` text,
  `interaction_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`interaction_id`),
  KEY `ticket_id` (`ticket_id`),
  KEY `sender_id` (`sender_id`),
  KEY `receiver_id` (`receiver_id`),
  CONSTRAINT `ticket_interaction_ibfk_1` FOREIGN KEY (`ticket_id`) REFERENCES `ticket` (`ticket_id`) ON DELETE CASCADE,
  CONSTRAINT `ticket_interaction_ibfk_2` FOREIGN KEY (`sender_id`) REFERENCES `user` (`user_id`) ON DELETE SET NULL,
  CONSTRAINT `ticket_interaction_ibfk_3` FOREIGN KEY (`receiver_id`) REFERENCES `user` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `attachment` (
  `attachment_id` int NOT NULL AUTO_INCREMENT,
  `ticket_id` int NOT NULL,
  `file_path` varchar(255),
  `uploaded_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `uploaded_by` int NOT NULL,
  `description` varchar(100) DEFAULT NULL COMMENT 'describe the attachments',
  PRIMARY KEY (`attachment_id`),
  KEY `ticket_id` (`ticket_id`),
  KEY `uploaded_by` (`uploaded_by`),
  CONSTRAINT `attachment_ibfk_1` FOREIGN KEY (`ticket_id`) REFERENCES `ticket` (`ticket_id`) ON DELETE CASCADE,
  CONSTRAINT `attachment_ibfk_2` FOREIGN KEY (`uploaded_by`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci; ;

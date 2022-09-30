CREATE DATABASE hoee;

CREATE TABLE `hoee`.`user` (
  `id` VARCHAR(20) NOT NULL,
  `password` VARCHAR(70) NOT NULL,
  `name` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`id`));

CREATE TABLE `hoee`.`capsule` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(45) NOT NULL,
  `content` TEXT NOT NULL,
  `created_at` DATE NOT NULL,
  `post_at` DATE NOT NULL,
  `status` INT NOT NULL,
  PRIMARY KEY (`id`));

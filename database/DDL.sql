-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema quiz
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema quiz
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `quiz` DEFAULT CHARACTER SET utf8 ;
USE `quiz` ;

-- -----------------------------------------------------
-- Table `quiz`.`candidates`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `quiz`.`candidates` (
  `candidate_id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(145) NOT NULL,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  PRIMARY KEY (`candidate_id`),
  UNIQUE INDEX `candidate_id_UNIQUE` (`candidate_id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `quiz`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `quiz`.`users` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `candidate_id` INT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `idEmployers_UNIQUE` (`user_id` ASC) VISIBLE,
  INDEX `fk_employers_candidates1_idx` (`candidate_id` ASC) VISIBLE,
  CONSTRAINT `fk_employers_candidates1`
    FOREIGN KEY (`candidate_id`)
    REFERENCES `quiz`.`candidates` (`candidate_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `quiz`.`question_types`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `quiz`.`question_types` (
  `type_id` INT NOT NULL AUTO_INCREMENT,
  `type_name` VARCHAR(45) NOT NULL,
  `type_description` VARCHAR(245) NOT NULL,
  PRIMARY KEY (`type_id`),
  UNIQUE INDEX `type_id_UNIQUE` (`type_id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `quiz`.`questions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `quiz`.`questions` (
  `question_id` INT NOT NULL AUTO_INCREMENT,
  `question` VARCHAR(1024) NOT NULL,
  `score` FLOAT NOT NULL,
  `time_allowed` INT NOT NULL,
  `question_type_id` INT NOT NULL,
  PRIMARY KEY (`question_id`),
  UNIQUE INDEX `question_id_UNIQUE` (`question_id` ASC) VISIBLE,
  INDEX `fk_questions_question_types1_idx` (`question_type_id` ASC) VISIBLE,
  CONSTRAINT `fk_questions_question_types1`
    FOREIGN KEY (`question_type_id`)
    REFERENCES `quiz`.`question_types` (`type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `quiz`.`quizzes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `quiz`.`quizzes` (
  `quiz_id` INT NOT NULL AUTO_INCREMENT,
  `total_score` FLOAT NOT NULL,
  `total_time` INT NOT NULL,
  `question_id` INT NULL,
  `due_date` DATE NOT NULL,
  `candidate_id` INT NULL,
  PRIMARY KEY (`quiz_id`),
  UNIQUE INDEX `quiz_id_UNIQUE` (`quiz_id` ASC) VISIBLE,
  INDEX `fk_quizzes_questions1_idx` (`question_id` ASC) VISIBLE,
  INDEX `fk_quizzes_candidates1_idx` (`candidate_id` ASC) VISIBLE,
  CONSTRAINT `fk_quizzes_questions1`
    FOREIGN KEY (`question_id`)
    REFERENCES `quiz`.`questions` (`question_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_quizzes_candidates1`
    FOREIGN KEY (`candidate_id`)
    REFERENCES `quiz`.`candidates` (`candidate_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `quiz`.`candidate_takes_quizzes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `quiz`.`candidate_takes_quizzes` (
  `link_id` INT NOT NULL AUTO_INCREMENT,
  `candidate_id` INT NOT NULL,
  `quiz_id` INT NOT NULL,
  `unique_link` VARCHAR(145) NOT NULL,
  PRIMARY KEY (`link_id`),
  INDEX `fk_candidates_has_quizzes_quizzes1_idx` (`quiz_id` ASC) VISIBLE,
  INDEX `fk_candidates_has_quizzes_candidates1_idx` (`candidate_id` ASC) VISIBLE,
  UNIQUE INDEX `link_id_UNIQUE` (`link_id` ASC) VISIBLE,
  CONSTRAINT `fk_candidates_has_quizzes_candidates1`
    FOREIGN KEY (`candidate_id`)
    REFERENCES `quiz`.`candidates` (`candidate_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_candidates_has_quizzes_quizzes1`
    FOREIGN KEY (`quiz_id`)
    REFERENCES `quiz`.`quizzes` (`quiz_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `quiz`.`users_quizzes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `quiz`.`users_quizzes` (
  `user_id` INT NOT NULL,
  `quiz_id` INT NOT NULL,
  INDEX `fk_users_has_quizzes_quizzes1_idx` (`quiz_id` ASC) VISIBLE,
  INDEX `fk_users_has_quizzes_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_quizzes_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `quiz`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_quizzes_quizzes1`
    FOREIGN KEY (`quiz_id`)
    REFERENCES `quiz`.`quizzes` (`quiz_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

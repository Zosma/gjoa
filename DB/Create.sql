-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema icebreaker
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `icebreaker` ;

-- -----------------------------------------------------
-- Schema icebreaker
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `icebreaker` DEFAULT CHARACTER SET latin1 ;
USE `icebreaker` ;

-- -----------------------------------------------------
-- Table `icebreaker`.`public_keys`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `icebreaker`.`public_keys` ;

CREATE TABLE IF NOT EXISTS `icebreaker`.`public_keys` (
  `pub_id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `public_key` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`pub_id`),
  UNIQUE INDEX `pub_id_UNIQUE` (`pub_id` ASC),
  UNIQUE INDEX `public_key_UNIQUE` (`public_key` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `icebreaker`.`hashes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `icebreaker`.`hashes` ;

CREATE TABLE IF NOT EXISTS `icebreaker`.`hashes` (
  `hid` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `hash` VARCHAR(64) NOT NULL,
  `type` VARCHAR(1) NOT NULL,
  `index` TINYINT(1) NOT NULL,
  `pub_id` BIGINT(20) UNSIGNED NULL,
  PRIMARY KEY (`hid`),
  UNIQUE INDEX `hid_UNIQUE` (`hid` ASC),
  INDEX `fk_hashes_public_keys1_idx` (`pub_id` ASC),
  CONSTRAINT `fk_hashes_public_keys1`
    FOREIGN KEY (`pub_id`)
    REFERENCES `icebreaker`.`public_keys` (`pub_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `icebreaker`.`private_keys`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `icebreaker`.`private_keys` ;

CREATE TABLE IF NOT EXISTS `icebreaker`.`private_keys` (
  `pri_id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `private_key` VARCHAR(64) NULL,
  `private_key_wif` VARCHAR(74) NULL,
  `private_key_wif_comp` VARCHAR(76) NULL,
  `pub_id` BIGINT(20) UNSIGNED NULL,
  PRIMARY KEY (`pri_id`),
  UNIQUE INDEX `pri_id_UNIQUE` (`pri_id` ASC),
  UNIQUE INDEX `private_key_UNIQUE` (`private_key` ASC),
  INDEX `fk_private_keys_public_keys1_idx` (`pub_id` ASC),
  CONSTRAINT `fk_private_keys_public_keys1`
    FOREIGN KEY (`pub_id`)
    REFERENCES `icebreaker`.`public_keys` (`pub_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `icebreaker`.`addresses`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `icebreaker`.`addresses` ;

CREATE TABLE IF NOT EXISTS `icebreaker`.`addresses` (
  `aid` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `address` VARCHAR(50) NOT NULL,
  `address_type` TINYINT(1) UNSIGNED NOT NULL DEFAULT 0 COMMENT '0 = UNCOMPRESSED\n1 = COMPRESSED',
  `balance` DECIMAL(20,8) NOT NULL DEFAULT 0.0,
  `status` TINYINT(4) NOT NULL DEFAULT 0 COMMENT '00 = active target\n01 = keypair known',
  `pub_id` BIGINT(20) UNSIGNED NULL,
  PRIMARY KEY (`aid`),
  UNIQUE INDEX `aid_UNIQUE` (`aid` ASC),
  UNIQUE INDEX `address_UNIQUE` (`address` ASC),
  INDEX `fk_addresses_public_keys1_idx` (`pub_id` ASC),
  CONSTRAINT `fk_addresses_public_keys1`
    FOREIGN KEY (`pub_id`)
    REFERENCES `icebreaker`.`public_keys` (`pub_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

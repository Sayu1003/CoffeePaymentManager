CREATE DATABASE IF NOT EXISTS coffeepayment;

USE coffeepayment;

CREATE TABLE IF NOT EXISTS drinks (
  `id` VARCHAR(6) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `price` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS bill (
  `id` Int NOT NULL AUTO_INCREMENT,
  `customer` VARCHAR(45) NULL,
  `total` INT UNSIGNED NOT NULL,
  `method` ENUM('Cash', 'Credit card', 'Debit card', 'Prepaid card', 'E-Wallet', 'Banking') NOT NULL,
  `date` TIMESTAMP NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS orders (
  `bill_id` INT NOT NULL,
  `drinks_id` VARCHAR(6) NOT NULL,
  `quantity` INT NOT NULL,
  `price` INT UNSIGNED NOT NULL,
  `total` INT UNSIGNED NOT NULL,
  FOREIGN KEY (`bill_id`) REFERENCES bill(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`drinks_id`) REFERENCES drinks(`id`) ON DELETE CASCADE
);


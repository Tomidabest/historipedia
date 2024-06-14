-- SQLBook: Code
GRANT ALL PRIVILEGES ON *.* TO 'mariadb_user'@'%' IDENTIFIED BY 'secure_pass123';
FLUSH PRIVILEGES;

CREATE DATABASE historipedia;
USE historipedia;

CREATE TABLE historical_entries (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    year INT NOT NULL
);

INSERT INTO historical_entries (title, description, year) VALUES ('Founding of Rome', 'Legend of Romulus and Remus', -753);
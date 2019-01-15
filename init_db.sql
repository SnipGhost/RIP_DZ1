DROP DATABASE IF EXISTS game_manager;
CREATE DATABASE game_manager CHARACTER SET utf8mb4;
GRANT ALL PRIVILEGES ON game_manager.* TO 'dbuser'@'localhost' IDENTIFIED BY 'password';

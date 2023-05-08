CREATE DATABASE CommonBlock;

USE CommonBlock;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(64) NOT NULL,
    email VARCHAR(120) NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    group_id INT(11)
);

CREATE TABLE account (
    id INT,
    user_id INT,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    age INT(2),
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE chatrooms(
    chatroom_id INT PRIMARY KEY AUTO_INCREMENT,
    user1 VARCHAR(64) NOT NULL, 
    user2 VARCHAR(64) NOT NULL,
    text_message VARCHAR(150)
);
CREATE TABLE messages(
    num ID PRIMARY KEY AUTO_INCREMENT,
    chatroom_id INT,
    user VARCHAR(64),
    text_message VARCHAR(150)
);


CREATE TABLE apartments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    address VARCHAR(120) NOT NULL,
    rent INT NOT NULL,
    num_bedrooms INT NOT NULL,
    lat DECIMAL(7, 4),
    lng DECIMAL(7, 4));


INSERT INTO users (username, email, password_hash)
VALUES ('admin', 'admin@gmail.com', 'password1');

INSERT INTO apartments(address, rent, num_bedrooms, lat, lng)
VALUES
('45 Wall St New York NY 10005', 2200, 1, 40.7062, -74.0100),
('15 Cliff St New York NY 10038', 1800, 2, 40.7083, -74.0057),
('8 Spruce St New York NY 10038', 2800, 3, 40.7101, -74.0052),
('100 John St New York NY 10038', 3100, 1, 40.7081, -74.0053),
('189 Bridge St Brooklyn NY 11201', 2500, 2, 40.7022, -73.9852),
('1 John St Brooklyn NY 11201', 3500, 3, 40.7041, -73.9817),
('25 Broad St New York NY 10004', 2400, 1, 40.7061, -74.0110),
('111 Fulton St New York NY 10038', 1800, 2, 40.7102, -74.0072),
('20 Exchange Pl New York NY 10005', 2800, 3, 40.7070, -74.0103),
('80 John St New York NY 10038', 3100, 1, 40.7084, -74.0064),
('37 Wall St New York NY 10005', 2500, 2, 40.7067, -74.0092),
('45 John St New York NY 10038', 3500, 3, 40.7090, -74.0083),
('200 Water St New York NY 10038', 2200, 1, 40.7062, -74.0033),
('81 Washington St Brooklyn NY 11201', 1800, 2, 40.7022, -73.9893),
('15 William St New York NY 10005', 2800, 3, 40.7069, -74.0082),
('33 Gold St New York NY 10038', 3100, 1, 40.7079, -74.0036),
('25 Hanover St New York NY 10005', 2500, 2, 40.7054, -74.0096),
('63 Wall St New York NY 10005', 3500, 3, 40.7067, -74.0091),
('88 Greenwich St New York NY 10006', 2400, 1, 40.7097, -74.0140),
('15 Park Row New York NY 10038', 1800, 2, 40.7112, -74.0073),
('70 Pine St New York NY 10270', 2800, 3, 40.7067, -74.0072),
('100 Maiden Ln New York NY 10038', 3100, 1, 40.7067, -74.0052),
('95 Wall St New York NY 10005', 2500, 2, 40.7052, -74.0083),
('123 Washington St New York NY 10006', 3500, 3, 40.7094, -74.0132);

CREATE TABLE Reviews (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    listing_id INT NOT NULL,
    rating INT NOT NULL,
    comment TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES Users (id),
    FOREIGN KEY (listing_id) REFERENCES Apartments (id)
);

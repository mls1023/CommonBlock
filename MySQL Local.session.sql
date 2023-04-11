CREATE DATABASE CommonBlock;

USE CommonBlock;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(64) NOT NULL,
    email VARCHAR(120) NOT NULL,
    password_hash VARCHAR(128) NOT NULL
);

CREATE TABLE apartments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    address VARCHAR(120) NOT NULL,
    rent INT NOT NULL,
    num_bedrooms INT NOT NULL
);

INSERT INTO users (username, email, password_hash)
VALUES ('admin', 'admin@gmail.com', 'password1');

INSERT INTO apartments(address, rent, num_bedrooms)
VALUES
('123 Broadway', 2200, 1),
('456 Main St', 1800, 2),
('789 Park Ave', 2800, 3),
('234 Madison Ave', 3100, 1),
('567 Lexington Ave', 2500, 2),
('890 5th Ave', 3500, 3),
('111 Wall St', 2400, 1),
('222 William St', 1800, 2),
('333 Pearl St', 2800, 3),
('444 Water St', 3100, 1),
('555 Front St', 2500, 2),
('666 South St', 3500, 3),
('777 East Broadway', 2200, 1),
('888 West Broadway', 1800, 2),
('999 Hudson St', 2800, 3),
('100 1st Ave', 3100, 1),
('200 2nd Ave', 2500, 2),
('300 3rd Ave', 3500, 3),
('400 4th Ave', 2400, 1),
('500 5th Ave', 1800, 2),
('600 6th Ave', 2800, 3),
('700 7th Ave', 3100, 1),
('800 8th Ave', 2500, 2),
('900 9th Ave', 3500, 3),
('101 10th St', 2200, 1),
('202 11th St', 1800, 2),
('303 12th St', 2800, 3),
('404 13th St', 3100, 1),
('505 14th St', 2500, 2),
('606 15th St', 3500, 3),
('707 16th St', 2400, 1),
('808 17th St', 1800, 2),
('909 18th St', 2800, 3),
('111 19th St', 3100, 1),
('222 20th St', 2500, 2),
('333 21st St', 3500, 3),
('444 22nd St', 2200, 1),
('555 23rd St', 1800, 2),
('666 24th St', 2800, 3);

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

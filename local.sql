drop database if exists furniture;
CREATE DATABASE furniture;
USE furniture;

CREATE TABLE category (
  category_id INT AUTO_INCREMENT PRIMARY KEY,
  category_name VARCHAR(100)
);

INSERT INTO category (category_name)
VALUES
('Bed'),
('Sofa'),
('Furniture'),
('Outdoor'),
('Motor');


CREATE TABLE status (
  status_id INT AUTO_INCREMENT PRIMARY KEY,
  status_name VARCHAR(100)
);

INSERT INTO status (status_name)
VALUES
('Sold'),
('Selling'),
('Own use');

CREATE TABLE platform (
  platform_id INT AUTO_INCREMENT PRIMARY KEY,
  platform_name VARCHAR(100)
);

INSERT INTO platform (platform_name)
VALUES
('Auction'),
('Trademe'),
('Facebook'),
('Wechat');


CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category_id INT NOT NULL,
    status_id INT NOT NULL,
    buy_date DATE NOT NULL,
    buy_price DECIMAL(10, 2) NOT NULL,
    buy_platform_id INT NOT NULL,
    sell_date DATE,
    sell_price DECIMAL(10, 2),
    sell_platform_id INT,
    fees DECIMAL(10, 2),
    image_name VARCHAR(255),
    FOREIGN KEY (category_id) REFERENCES category(category_id),
    FOREIGN KEY (status_id) REFERENCES status(status_id),
    FOREIGN KEY (buy_platform_id) REFERENCES platform(platform_id),
    FOREIGN KEY (sell_platform_id) REFERENCES platform(platform_id)
);


INSERT INTO products (product_name, category_id, status_id, buy_date, buy_price, buy_platform_id, sell_date, sell_price, sell_platform_id, fees,image_name) VALUES
('Sleepyhead King mattress - Balance', 1, 1, '2023-07-15', 155.00, 2, '2023-07-20', 400, 3, 0,'Picture1.jpg');



drop database if exists fu222cs98$default;
CREATE DATABASE fu222cs98$default;
USE fu222cs98$default;

CREATE TABLE category (
  category_id INT AUTO_INCREMENT PRIMARY KEY,
  category_name VARCHAR(100)
);



CREATE TABLE status (
  status_id INT AUTO_INCREMENT PRIMARY KEY,
  status_name VARCHAR(100)
);


CREATE TABLE platform (
  platform_id INT AUTO_INCREMENT PRIMARY KEY,
  platform_name VARCHAR(100)
);



CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category_id INT NOT NULL,
    status_id INT NOT NULL,
    buy_date DATE NOT NULL,
    buy_price DECIMAL(10, 2) NOT NULL,
    buy_platform_id INT NOT NULL,
	image_url VARCHAR(255),
    FOREIGN KEY (category_id) REFERENCES category(category_id),
    FOREIGN KEY (status_id) REFERENCES status(status_id),
    FOREIGN KEY (buy_platform_id) REFERENCES platform(platform_id)
);


CREATE TABLE sales (
    sale_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,
    sell_date DATE ,
    sell_price DECIMAL(10, 2)NOT NULL,
    sell_platform_id INT ,
    fees DECIMAL(10, 2) DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (sell_platform_id) REFERENCES platform(platform_id)
);


INSERT INTO category (category_name)
VALUES
('Bed'),
('Sofa'),
('Furniture'),
('Outdoor'),
('Motor');

INSERT INTO status (status_name)
VALUES
('Sold'),
('Selling'),
('Own use');

INSERT INTO platform (platform_name)
VALUES
('Auction'),
('Trademe'),
('Facebook'),
('Wechat');

INSERT INTO products (product_name, category_id, status_id, buy_date, buy_price, buy_platform_id, image_url)
VALUES
  ('Sleepyhead King mattress - Balance', 1, 1, '2023-07-15', 155, 2, 'Picture1.jpg'),
  ('Tan leather couches x 2', 2, 2, '2023-07-22', 1400, 2, 'Picture2.jpg'),
  ('Sleepyhead Queen bed - Chiropractic Aruba', 1, 1, '2023-07-25', 300, 3, 'Picture3.jpg'),
  ('Free leather couch', 2, 1, '2023-08-10', 0, 3, 'Picture4.jpg'),
  ('Sleepyhead Queen bed - Sanctuary', 1, 1, '2023-08-12', 300, 3, 'Picture5.jpg'),
  ('Beautyrest Queen bed', 1, 1, '2023-08-19', 350, 2, 'Picture6.jpg'),
  ('King Headboard', 1, 1, '2023-08-20', 50, 2, 'Picture7.jpg'),
  ('5 Seater Leather couch', 2, 1, '2023-08-24', 250, 3, 'Picture8.jpg'),
  ('John Deere STX38 Black deck Ride On', 5, 1, '2023-08-24', 800, 3, 'Picture9.jpg'),
  ('Nood double sofa bed', 2, 1, '2023-08-25', 150, 3, 'Picture10.jpg');

  
  
INSERT INTO sales (product_id, sell_date, sell_price, sell_platform_id, fees)
VALUES
  (1, '2023-07-20', 400.0, 3, 0),
  (3, '2023-09-04', 461.0, 2, 36.42),
  (4, '2023-08-14', 400.0, 2, 0),
  (5, '2023-08-18', 600.0, 2, 0),
  (6, '2023-09-24', 1400.0, 2, 0),
  (7, '2023-10-01', 300.0, 2, 23.7),
  (8, '2023-10-12', 600.0, 2, 47),
  (9, '2023-11-08', 1100.0, 3, 200),
  (10, '2023-09-06', 450.0, 2, 35.55);
  

-- Inserting into products table with image_url as NULL
INSERT INTO products (product_id, product_name, category_id, status_id, buy_date, buy_price, buy_platform_id, image_url)
VALUES
  (11, '8x4 Trailer', 5, 1, '2023-08-26', 1000, 3, 'Picture11.jpg'),
  (12, 'Kubu Dining Table', 3, 1, '2023-08-30', 281, 2, 'Picture12.jpg'),
  (13, 'Trundle bed with SereneSleep mattress', 1, 1, '2023-09-01', 200, 2, 'Picture13.jpg'),
  (14, 'Sleepyhead Queen bed - Chiropractic', 1, 1, '2023-09-02', 100, 3, 'Picture14.jpg'),
  (15, 'Sleepyhead Super King Mattress', 1, 1, '2023-09-09', 250, 2, 'Picture15.jpg'),
  (16, 'Le forge 3 seater', 2, 2, '2023-09-12', 80, 1, 'Picture16.jpg'),
  (17, 'Sleepyhead King bed', 1, 1, '2023-09-22', 350, 3, 'Picture17.jpg'),
  (18, 'John Deere STX38 Yellow deck Ride On', 5, 1, '2023-09-22', 300, 3, 'Picture18.jpg'),
  (19, 'Sleepyhead King bed', 1, 1, '2023-09-26', 230, 3,'Picture19.jpg'),
  (20, 'Sleepyhead King bed', 1, 1, '2023-09-28', 150, 2, 'Picture20.jpg'),
  (21, 'Sleepyhead King bed', 1, 1, '2023-09-29', 150, 3, 'Picture21.jpg'),
  (22, 'Sleepyhead King mattress - Matrix', 1, 1, '2023-09-29', 300, 2, 'Picture22.jpg'),
  (23, 'Black Leather couches x 2', 2, 1, '2023-09-30', 100, 2,'Picture23.jpg'),
  (24, '10 x 5 trailer', 5, 1, '2023-10-03', 3000, 3, 'Picture24.jpg'),
  (25, 'Lazy Chair', 2, 1, '2023-10-03', 150, 3, 'Picture25.jpg'),
  (26, 'Hunter leather couches x 2', 2, 1, '2023-10-05', 490, 3, 'Picture26.jpg'),
  (27, 'Mckenzin & Wills Red Leather Couch', 2, 1, '2023-10-12', 350, 3, 'Picture27.jpg'),
  (28, 'Harvey Norman Red Leather Couch', 2, 1, '2023-10-18', 60, 3, 'Picture28.jpg'),
  (29, 'King Koil Queen Bed', 1, 3, '2023-10-21', 300, 3, 'Picture29.jpg'),
  (30, 'Sleepyhead King Sanctuary Mattress', 1, 1, '2023-10-21', 300, 2, 'Picture30.jpg');

-- Inserting into sales table
INSERT INTO sales (product_id, sell_date, sell_price, sell_platform_id, fees)
VALUES
  (11, '2023-11-13', 2999.0, 2, 100),
  (12, '2023-10-12', 850.0, 3, 0),
  (13, '2023-09-09', 250.0, 2, 19.75),
  (14, '2023-09-10', 450.0, 3, 0),
  (15, '2023-11-19', 800.0, 2, 0),
  (17, '2024-01-25', 350.0, 2, 0),
  (18, '2023-11-08', 400.0, 3, 0),
  (19, '2023-10-20', 570.0, 4, 0),
  (20, '2023-10-18', 500.0, 2, 39.5),
  (21, '2023-10-20', 340.0, 2, 0),
  (22, '2023-10-18', 1300.0, 2, 102.7),
  (23, '2023-12-06', 700.0, 2, 0),
  (24, NULL, 3500.0, 3, 0),
  (25, '2023-11-25', 400.0, 2, 31.6),
  (26, '2023-11-26', 500.0, 3, 0),
  (27, '2024-06-27', 400.0, 2, 31.6),
  (28, '2024-01-05', 1000.0, 2, 79),
  (30, '2023-11-25', 300.0, NULL, 0);



INSERT INTO products (product_id, product_name, category_id, status_id, buy_date, buy_price, buy_platform_id, image_url)
VALUES
  (31, 'Beautyrest King bed Conniesur', 1, 1, '2023-10-23', 350, 2, 'Picture31.jpg'),
  (32, 'Beautyrest Black Super King Beyond Grandeur Plush', 1, 1, '2023-10-23', 570, 2, 'Picture32.jpg'),
  (33, 'King Koil King Bed', 1, 1, '2023-10-24', 101, 2, 'Picture33.jpg'),
  (34, 'Brown Leather Couch', 2, 2, '2023-10-27', 200, 3, 'Picture34.jpg'),
  (35, 'Vintage leather couch', 2, 1, '2023-10-28', 350, 3, 'Picture35.jpg'),
  (36, 'Beautyrest Super King Bed', 1, 1, '2023-11-01', 300, 3, 'Picture36.jpg'),
  (37, '8 x 5 Trailer', 5, 1, '2023-11-17', 1000, 3, 'Picture37.jpg'),
  (38, 'Red Leather Chesterfield Lounge Suite', 2, 1, '2023-11-19', 750, 3, 'Picture38.jpg'),
  (39, 'King bed base', 1, 1, '2023-11-19', 100, 3, 'Picture39.jpg'),
  (40, 'Sofa', 2, 1, '2023-11-08', 200, 2, 'Picture40.jpg'),
  (41, 'Sleepyhead King Mattress - Sanctuary', 1, 1, '2023-11-17', 99, 2, 'Picture41.jpg'),
  (42, 'Nood double sofa bed x 2', 1, 1, '2023-11-17', 500, 2, 'Picture42.jpg'),
  (43, 'Queen bed base', 1, 3, '2023-10-25', 100, 3, 'Picture43.jpg'),
  (44, 'Sleepyhead queen bed', 1, 1, '2023-11-19', 295, 3, 'Picture44.jpg'),
  (45, 'Super king headboard', 1, 1, '2023-11-25', 250, 3, 'Picture45.jpg'),
  (46, 'Super King Bed - Sanctuary', 1, 1, '2023-11-25', 400, 3, 'Picture46.jpg'),
  (47, '7x4 Trailer', 5, 1, '2023-07-15', 1500, 3, 'Picture47.jpg'),
  (48, '6x3.9 Trailer', 5, 1, '2023-11-27', 200, 3, 'Picture48.jpg');


-- 插入到 sales 表中
INSERT INTO sales (product_id, sell_date, sell_price, sell_platform_id, fees)
VALUES
  (31, '2023-12-01', 2300.0, NULL, 0),
  (32, '2024-06-01', 2800.0, 2, 0),
  (33, '2024-03-28', 101.0, 3, 0),
  (35, '2024-02-12', 3000.0, 2, 237),
  (36, '2024-03-28', 300.0, 3, 0),
  (37, '2024-03-20', 2350.0, 3, 0),
  (38, '2023-12-05', 2500.0, 2, 0),
  (39, '2024-03-26', 100.0, 3, 0),
  (40, '2024-03-26', 900.0, 3, 0),
  (41, NULL, 400.0, 2, 0),
  (42, '2023-12-15', 850.0, 3, 0),
  (44, '2023-12-21', 450.0, NULL, 0),
  (45, '2024-04-21', 400.0, 3, 0),
  (46, '2024-01-16', 1200.0, 3, 0),
  (47, '2023-11-26', 1850.0, NULL, 0),
  (48, '2023-12-22', 550.0, NULL, 0);

INSERT INTO products (product_id, status_id, product_name, category_id, buy_date, buy_price, buy_platform_id, image_url)
VALUES
  (49, 1, 'Sleepyhead King mattress - Matrix', 1, '2023-12-03 00:00:00', 400, 3, 'Picture49.jpg'),
  (50, 1, 'John Deere L110', 5, '2023-10-14 00:00:00', 800, 3, 'Picture50.jpg'),
  (51, 1, 'Beautyrest Queen mattress', 1, '2023-12-05 00:00:00', 500, 3, 'Picture51.jpg'),
  (52, 1, 'Sleepyhead King Single', 1, '2023-12-10 00:00:00', 250, 3, 'Picture52.jpg'),
  (53, 1, 'Beautyrest Superking bed', 1, '2023-12-11 00:00:00', 500, 2, 'Picture53.jpg'),
  (54, 1, 'La-Z-Boy 3 Seater Leather couch', 2, '2023-12-12 00:00:00', 300, 2, 'Picture54.jpg'),
  (55, 1, 'Sleepyhead King mattress - Balance', 1, '2023-12-12 00:00:00', 100, 2, 'Picture55.jpg'),
  (56, 1, 'Queen headboard', 1, '2023-08-19 00:00:00', 0, 2, 'Picture56.jpg'),
  (57, 1, 'Briford 7x4 900mm trailer', 5, '2023-12-17 00:00:00', 1250, 3, 'Picture57.jpg'),
  (58, 1, 'Queen headboard', 1, '2023-09-03 00:00:00', 0, 2, 'Picture58.jpg'),
  (59, 1, 'Sleepyhead Queen bed - Serenity Series 6', 1, '2023-09-03 00:00:00', 408, 2, 'Picture59.jpg'),
  (60, 1, 'Recliner Chair', 2, '2023-10-10 00:00:00', 100, 3, 'Picture60.jpg'),
  (61, 1, 'Recliner Chair', 2, '2023-08-01 00:00:00', 100, 2, 'Picture61.jpg'),
  (62, 1, 'Recliner Chair', 2, '2023-12-21 00:00:00', 200, 3, 'Picture62.jpg'),
  (63, 1, 'John Deere STX38 Black deck Ride On', 5, '2023-12-21 00:00:00', 1200, 2, 'Picture63.jpg'),
  (64, 1, '2x LUCA HENDRIX II LEATHER CHAIR', 2, '2023-12-14 00:00:00', 400, 3, 'Picture64.jpg'),
  (65, 1, 'Super king headboard', 1, '2023-12-11 00:00:00', 0, 2, 'Picture65.jpg'),
  (66, 1, 'Tandem Trailer', 5, '2024-01-04 00:00:00', 1000, 2, 'Picture66.jpg'),
  (67, 1, 'Husqvarna 1542 Ride On Lawnmower', 5, '2024-01-07 00:00:00', 700, 2, 'Picture67.jpg'),
  (68, 1, '2x Leather recliner armchairs', 2, '2024-01-07 00:00:00', 700, 3, 'Picture68.jpg'),
  (69, 1, 'La-Z-Boy 2 Seater Leather couch suite', 2, '2024-01-07 00:00:00', 350, 3, 'Picture69.jpg'),
  (70, 1, 'Chestfield 2 seater couch', 2, '2024-01-10 00:00:00', 400, 3, 'Picture70.jpg'),
  (71, 1, '2 recliner chairs', 2, '2024-01-10 00:00:00', 55, 3, 'Picture71.jpg'),
  (72, 1, 'Couch and dining table with 4 chairs', 2, '2024-01-17 00:00:00', 100, 3, 'Picture72.jpg'),
  (73, 1, 'Dyson vaccums', 5, '2024-01-17 00:00:00', 80, 3, 'Picture73.jpg'),
  (74, 1, 'Queen bed split base', 1, '2024-01-17 00:00:00', 10, 3, 'Picture74.jpg'),
  (75, 1, 'Chestfield 3 seater couch', 2, '2024-01-19 00:00:00', 320, 3, 'Picture75.jpg'),
  (76, 2, 'Sleepyhead Super King Mattress', 1, '2024-01-13 00:00:00', 200, 3, 'Picture76.jpg'),
  (77, 3, 'Black Leather Lounge Suites 3 + 2 seaters from Asko design', 2, '2024-01-13 00:00:00', 400, 2, 'Picture77.jpg'),
  (78, 1, '2 x STRESS FREE leather Recliner chairs with footstools from McKenzie & Willis', 2, '2024-01-05 00:00:00', 700, 3, 'Picture78.jpg'),
  (79, 2, 'Super King Bed Base with Headboard', 1, '2024-01-21 00:00:00', 80, 3, 'Picture79.jpg'),
  (80, 1, 'Recliner Chair', 2, '2024-01-19 00:00:00', 100, 3, 'Picture80.jpg'),
  (81, 1, 'Leather Chair with footstoll', 2, '2024-01-19 00:00:00', 100, 3, 'Picture81.jpg'),
  (82, 1, 'King Rimu Headboard', 1, '2023-10-19 00:00:00', 0, 2, 'Picture82.jpg'),
  (83, 1, '8.5x5 trailer', 5, '2024-01-25 00:00:00', 600, 3, 'Picture83.jpg'),
  (84, 1, 'Nood 3 seater leather couch', 2, '2024-02-08 00:00:00', 450, 3, 'Picture84.jpg'),
  (85, 1, 'Lounge suite', 2, '2024-02-08 00:00:00', 550, 3, 'Picture85.jpg'),
  (86, 1, 'Beautyrest King bed recharge', 1, '2024-02-25 00:00:00', 250, 2, 'Picture86.jpg'),
  (87, 1, 'IMG Recliner Chair with stool', 2, '2024-03-09 00:00:00', 650, 2, 'Picture87.jpg'),
  (88, 1, 'Chestfield 2 seater couch', 2, '2024-03-01 00:00:00', 150, 3, 'Picture88.jpg');

  
  INSERT INTO sales (product_id,  sell_date, sell_price, sell_platform_id, fees)
VALUES
  (49, '2024-01-05 00:00:00', 1000.0, NULL, 100),
  (50, '2023-12-05 00:00:00', 1000.0, NULL, 0),
  (51, '2024-06-02 00:00:00', 1300.0, 3, 0),
  (52, '2024-02-06 00:00:00', 550.0, NULL, 0),
  (53, '2024-05-09 00:00:00', 1100.0, 2, 86.9),
  (54, '2023-12-28 00:00:00', 600.0, 3, 0),
  (55, '2023-12-19 00:00:00', 80.0, 3, 0),
  (56, '2023-12-19 00:00:00', 100.0, 3, 0),
  (57, '2023-12-24 00:00:00', 2500.0, 3, 0),
  (58, '2023-12-20 00:00:00', 80.0, 3, 0),
  (59, '2023-12-28 00:00:00', 1600.0, 2, 126.4),
  (60,'2023-11-25 00:00:00', 400.0, 2, 31.6),
  (61, '2023-11-25 00:00:00', 250.0, 3, 0),
  (62, '2024-01-21 00:00:00', 350.0, 2, 27.6),
  (63, '2023-12-28 00:00:00', 2800.0, 3, 0),
  (64, '2024-04-13 00:00:00', 1200.0, 3, 0),
  (65, '2023-12-18 00:00:00', 150.0, 3, 0),
  (66, '2024-03-16 00:00:00', 1250.0, 2, 19.99),
  (67, '2024-03-30 00:00:00', 1450.0, 3, 300),
  (68, '2024-01-22 00:00:00', 2000.0, NULL, 158),
  (69, '2024-05-08 00:00:00', 800.0, 2, 63.2),
  (70, '2024-04-05 00:00:00', 650.0, 2, 51.35),
  (71, '2024-01-19 00:00:00', 50.02, 2, 3.95),
  (72, NULL, 170.0, 2, 9.48),
  (73,  '2024-01-19 00:00:00', 90.0, 2, 3),
  (74, '2024-06-06 00:00:00', 10.0, 2, 0),
  (75, '2024-03-08 00:00:00', 1350.0, 2, 106.65),
  (78,  '2024-01-22 00:00:00', 2000.0, NULL, 158),
  (80, '2024-01-25 00:00:00', 150.0, NULL, 0),
  (81, '2024-01-25 00:00:00', 171.0, NULL, 13.51),
  (82, '2024-01-30 00:00:00', 300.0, NULL, 23.7),
  (83, NULL, 650.0, NULL, 53.09),
  (84, '2024-04-22 00:00:00', 1400.0, 2, 110.6),
  (85, '2024-04-22 00:00:00', 1500.0, 2, 118.5),
  (86, '2024-04-07 00:00:00', 1350.0, 2, 106.65),
  (87, '2024-03-22 00:00:00', 1500.0, 2, 0),
  (88, '2024-03-31 00:00:00', 300.0, 3, 0);
  
INSERT INTO products (product_id, product_name, category_id, status_id, buy_date, buy_price, buy_platform_id, image_url)
VALUES
  (89, 'John Deere L110 with Sweeper', 5, 1, '2024-03-10', 700.00, 3, 'Picture89.jpg'),
  (90, 'Nood double sofa bed', 2, 1, '2024-02-29', 207.00, 2, 'Picture90.jpg'),
  (91, 'Briford 6x4 900mm trailer', 5, 1, '2024-03-03', 1000.00, 3, 'Picture91.jpg'),
  (92, 'Briford 7x4 trailer', 5, 1, '2024-03-03', 1000.00, 3, 'Picture92.jpg'),
  (93, 'John Deere LTR180 Ride on Fixing fee $1144', 5, 1, '2024-01-30', 600.00, 2, 'Picture93.jpg'),
  (94, 'Double Horse Float', 5, 1, '2024-01-12', 2000.00, 3, 'Picture94.jpg'),
  (95, 'Beautyrest Reign Firm Super King Bed', 1, 1, '2023-12-13', 1000.00, 3, 'Picture95.jpg'),
  (96, 'John Deere Sweeper', 5, 1, '2024-03-24', 50.00, 3, 'Picture96.jpg'),
  (97, '8x5 Trailer', 5, 1, '2024-03-23', 1600.00, 3, 'Picture97.jpg'),
  (98, '8x5 Roadchef Tandem Trailer', 5, 3, '2024-03-17', 2500.00, 2, 'Picture98.jpg'),
  (99, 'Trundler Bed', 1, 3, '2024-03-24', 125.00, 2, 'Picture99.jpg'),
  (100, 'Beautyrest King bed with headboard', 1, 1, '2024-03-13', 375.00, 3, 'Picture100.jpg'),
  (101, 'King Headboard', 1, 1, '2024-03-13', 0.00, 3, 'Picture101.jpg'),
  (102, 'Chesterfield Style Couch', 2, 1, '2024-04-01', 150.00, 3, 'Picture102.jpg'),
  (103, 'Luca 3 Seater Couch', 2, 1, '2024-04-03', 800.00, 3, 'Picture103.jpg'),
  (104, 'Nood sofa bed', 2, 1, '2024-04-03', 80.00, 2, 'Picture104.jpg'),
  (105, 'Recliner Chair', 2, 1, '2024-04-03', 160.00, 3, 'Picture105.jpg'),
  (106, 'La-Z-Boy L Shape Leather Lounge Suite', 2, 3, '2024-04-03', 200.00, 3, 'Picture106.jpg'),
  (107, 'Nood double sofa bed', 2, 1, '2024-04-06', 100.00, 3, 'Picture107.jpg');

  
  
  INSERT INTO sales (product_id, sell_date, sell_price, sell_platform_id, fees)
VALUES
  (89, '2024-03-10', 0.00, NULL, 0),
  (90, '2024-03-14', 450.00, 3, 0),
  (91, '2024-03-20', 2700.00, 3, 0),
  (92, '2024-03-16', 2000.00, 3, 35.00),
  (93, '2024-06-03', 550.00, 2, 0),
  (94, '2024-04-24', 2600.00, 3, 0),
  (95, '2024-03-25', 2200.00, 2, 0),
  (96, '2024-04-27', 450.00, 3, 0),
  (97, '2024-03-31', 2300.00, 3, 88.00),
  (100, '2024-04-28', 1200.00, 2, 94.80),
  (101, '2024-03-30', 200.00, NULL, 0),
  (102, '2024-05-09', 550.00, 2, 43.45),
  (103, '2024-04-14', 1800.00, 3, 0),
  (104, '2024-06-19', 375.00, 3, 0),
  (105, '2024-04-29', 270.00, 3, 0),
  (107, '2024-04-11', 280.00, 3, 0);
  
 INSERT INTO products (product_id, product_name, category_id, status_id, buy_date, buy_price, buy_platform_id, image_url)
VALUES
  (108, 'Free King Bed with Headboard', 1, 1, '2024-04-06', 0, 3, 'Picture108.jpg'),
  (109, 'Queen bed base', 1, 1, '2024-04-06', 70, 3, 'Picture109.jpg'),
  (110, 'SleepyHead Sanctuary Queen Mattress', 1, 1, '2024-04-12', 100, 3, 'Picture110.jpg'),
  (111, '8x5 Trailer', 5, 1, '2024-04-12', 1200, 3, 'Picture111.jpg'),
  (112, 'Leather Chesterfield 3 + 2 Seater Suite', 2, 1, '2024-04-13', 1300, 3, 'Picture112.jpg'),
  (113, 'John Deere Zero Turn Z235', 5, 1, '2023-11-18', 3500, 3, 'Picture113.jpg'),
  (114, 'Sleepyhead Queen Mattress Matrix', 1, 1, '2024-04-21', 50, 3, 'Picture114.jpg'),
  (115, '2 seater sofa Nood', 2, 1, '2024-04-21', 350, 3, 'Picture115.jpg'),
  (116, 'bedside tables and tallboy', 1, 2, '2024-04-21', 100, 3, 'Picture116.jpg'),
  (117, 'John Deere Zero Turn Z425', 5, 2, '2024-04-16', 1600, 3, 'Picture117.jpg'),
  (118, 'Trailer 7x4', 5, 1, '2024-04-20', 1250, 2, 'Picture118.jpg'),
  (119, '2 seater and one seater couch', 2, 2, '2024-04-22', 100, 3, 'Picture119.jpg'),
  (120, 'DeWalt Charger', 5, 1, '2024-04-26', 0, 3, 'Picture120.jpg'),
  (121, 'Queen mattress Sleepyhead', 1, 2, '2024-04-29', 250, 3, 'Picture121.jpg'),
  (122, 'Yamaha Grizzly 125', 5, 1, '2024-05-08', 1450, 3, 'Picture122.jpg'),
  (123, 'Vehicle Access Ramp', 5, 2, '2024-04-18', 306, 2, 'Picture123.jpg'),
  (124, 'Leather 3 seater couch', 2, 2, '2024-05-06', 185, 2, 'Picture124.jpg'),
  (125, 'Luca Chair', 2, 1, '2024-05-09', 50, 3, 'Picture125.jpg'),
  (126, 'Briford 8x4 Single Axle Trailer', 5, 1, '2024-05-09', 1550, 3, 'Picture126.jpg'),
  (127, 'Leather 3 seater couch', 2, 1, '2024-05-09', 150, 3, 'Picture127.jpg');

  
  INSERT INTO sales (product_id, sell_date, sell_price, sell_platform_id, fees)
VALUES
  (108, '2024-05-19', 100.0, 3, 0),
  (109, '2024-04-22', 70.0, 2, 0),
  (110, '2024-04-22', 550.0, 2, 36.45),
  (111, '2024-04-25', 1800.0, 2, 150),
  (112, '2024-04-20', 1800.0, 2, 0),
  (113, '2024-04-15', 5150.0, 3, 0),
  (114, '2024-06-09', 1000.0, 2, 79),
  (115, '2024-06-28', 650.0, 2, 47.4),
  (118, '2024-04-28', 1500.0, 3, 0),
  (120, '2024-04-26', 30.0, 3, 0),
  (122, '2024-06-21', 1900.0, 3, 0),
  (125, '2024-06-17', 100.0, 2, 7.9),
  (126, '2024-06-14', 1550.0, 3, 0),
  (127, '2024-06-01', 300.0, 2, 23.7);

INSERT INTO products (product_name, category_id, status_id, buy_date, buy_price, buy_platform_id, image_url)
VALUES
  ('John Deere LA105 Ride On Lawn Mower', 5, 1, '2024-05-08 00:00:00', 700, 3, 'Picture128.jpg'),
  ('6x4 Trailer', 5, 1, '2024-05-07 00:00:00', 300, 2, 'Picture129.jpg'),
  ('2 x single bed', 1, 1, '2024-05-06 00:00:00', 175, 3, 'Picture130.jpg'),
  ('Beautyrest Super King Mattress', 1, 2, '2024-05-08 00:00:00', 230, 3, 'Picture131.jpg'),
  ('2x two seater fabric couches', 2, 1, '2024-05-12 00:00:00', 150, 2, 'Picture132.jpg'),
  ('Leather Chesterfield 2 Seater couch', 2, 1, '2024-05-08 00:00:00', 450, 2, 'Picture133.jpg'),
  ('Leather Chesterfield 3 Seater couch', 2, 2, '2024-05-12 00:00:00', 500, 2, 'Picture134.jpg'),
  ('Sleepyhead Queen mattress', 1, 1, '2024-05-12 00:00:00', 150, 3, 'Picture135.jpg'),
  ('3 red bar stools', 2, 2, '2024-05-12 00:00:00', 30, 2, 'Picture136.jpg'),
  ('Trundler Bed', 1, 1, '2024-05-15 00:00:00', 50, 2, 'Picture137.jpg'),
  ('Sleepyhead Super King Mattress', 1, 1, '2024-05-12 00:00:00', 250, 3, 'Picture138.jpg'),
  ('Outdoor table with umbrella', 3, 3, '2024-05-12 00:00:00', 150, 2, 'Picture139.jpg'),
  ('Stressless Chair', 2, 1, '2024-05-22 00:00:00', 160, 3, 'Picture140.jpg'),
  ('Luca 3 Seater Couch', 2, 1, '2024-05-25 00:00:00', 1000, 3, 'Picture141.jpg'),
  ('Sleepyhead Queen bed', 1, 1, '2024-05-25 00:00:00', 450, 3, 'Picture142.jpg'),
  ('Sleepyhead Queen mattress', 1, 1, '2024-05-25 00:00:00', 350, 3, 'Picture143.jpg'),
  ('Sleepyhead King mattress', 1, 1, '2024-05-25 00:00:00', 200, 2, 'Picture144.jpg'),
  ('King Single Electric Bed', 1, 1, '2024-05-26 00:00:00', 185, 2, 'Picture145.jpg'),
  ('King mattress', 1, 1, '2024-05-24 00:00:00', 300, 3, 'Picture146.jpg'),
  ('King single mattress', 1, 1, '2024-05-01 00:00:00', 70, 3, 'Picture147.jpg');

  
  INSERT INTO sales (product_id, sell_date, sell_price, sell_platform_id, fees)
VALUES
  (128, '2024-06-17 00:00:00', 1500.0, 2, 118.5),
  (129, '2024-05-25 00:00:00', 400.0, 3, 0),
  (130, '2024-05-19 00:00:00', 560.0, 3, 0),
  (132, '2024-05-20 00:00:00', 600.0, 3, 0),
  (133, '2024-06-05 00:00:00', 950.0, 2, 75.05),
  (134, NULL, 100.0, NULL, NULL),
  (135, '2024-06-17 00:00:00', 530.0, 3, 0),
  (137, '2024-05-20 00:00:00', 400.0, 3, 0),
  (138, '2024-05-23 00:00:00', 600.0, 2, 47.4),
  (140, '2024-06-22 00:00:00', 400.0, 2, 31.6),
  (141, '2024-06-03 00:00:00', 1600.0, 2, 116.4),
  (142, '2024-06-03 00:00:00', 600.0, 2, 47.4),
  (143, '2024-06-22 00:00:00', 800.0, 2, 0),
  (144, '2024-06-03 00:00:00', 600.0, 3, 0),
  (145, '2024-06-30 00:00:00', 800.0, 3, 0),
  (146, '2024-06-06 00:00:00', 600.0, 3, 0),
  (147, '2024-05-28 00:00:00', 400.0, 3, 0);
  
  
-- 插入产品数据
INSERT INTO products (product_id, product_name, category_id, status_id, buy_date, buy_price, buy_platform_id, image_url)
VALUES
  (148, 'Nood Leather couch', 2, 1, '2024-05-27', 700, 2, 'Picture148.jpg'),
  (149, 'Wooden Bench', 2, 3, '2024-05-28', 100, 3, 'Picture149.jpg'),
  (150, 'Wooden Bench 2', 2, 3, '2024-05-28', 40, 3, 'Picture150.jpg'),
  (151, 'King mattress', 1, 1, '2024-01-21', 140, 3, 'Picture151.jpg'),
  (152, 'Freedom 3 seater leather couch', 2, 2, '2024-06-02', 800, 3, 'Picture152.jpg'),
  (153, 'Kubu TV unit and Buffet', 2, 3, '2024-05-30', 1638, 1, 'Picture153.jpg'),
  (154, '2 Armchairs from Nood', 2, 1, '2023-07-31', 400, 3, 'Picture154.jpg'),
  (155, 'Lounge suite', 2, 1, '2024-06-02', 150, 3, 'Picture155.jpg'),
  (156, 'King mattress', 1, 2, '2024-06-04', 75, 3, 'Picture156.jpg'),
  (157, 'Kubu Coffee Table', 1, 3, '2024-06-03', 80, 3, 'Picture157.jpg'),
  (158, 'Luca 3 + 2 Seater Couches', 2, 1, '2024-06-04', 1300, 4, 'Picture158.jpg'),
  (159, 'Super King bed', 1, 1, '2024-06-07', 250, 2, 'Picture159.jpg'),
  (160, 'Queen bed', 1, 2, '2024-06-07', 100, 2, 'Picture160.jpg'),
  (161, 'Sofa', 2, 1, '2024-06-03', 175, 2, 'Picture161.jpg'),
  (162, 'Leather Chesterfield 2 Seater couch', 2, 1, '2024-06-12', 1100, 3, 'Picture162.jpg'),
  (163, 'King mattress', 1, 1, '2024-06-12', 150, 2, 'Picture163.jpg'),
  (164, 'MTD Ride On With Sweeper', 5, 2, '2024-06-14', 600, 2, 'Picture164.jpg'),
  (165, 'Luca 3 Seater Couch with 2 Chairs', 2, 2, '2024-06-14', 550, 3, 'Picture165.jpg'),
  (166, 'Honda TRX420', 5, 3, '2024-06-14', 2000, 2, 'Picture166.jpg'),
  (167, 'Husqvarna Z242F Zero Turn Ride On Lawn Mower', 5, 1, '2024-03-19', 4500, 3, 'Picture167.jpg');


-- 插入销售数据
INSERT INTO sales (product_id, sell_date, sell_price, sell_platform_id, fees)
VALUES
  (148, '2024-06-30', 1330.0, 3, 0),
  (151, '2024-06-02', 250.0, NULL, 19.75),
  (154, '2024-06-04', 1000.0, NULL, 0),
  (155, '2024-06-09', 450.0, 3, 0),
  (158, '2024-06-21', 2900.0, 3, 0),
  (159, '2024-06-30', 500.0, 3, 0),
  (161, '2024-06-13', 200.0, 3, 0),
  (162, '2024-06-29', 1350.0, 2, 106.65),
  (163, '2024-06-29', 730.0, 3, 0),
  (165, NULL, 500.0, NULL, 0),
  (167, '2024-06-18', 6500.0, 3, 0);

-- 插入产品数据
INSERT INTO products (product_id, product_name, category_id, status_id, buy_date, buy_price, buy_platform_id, image_url)
VALUES
  (168, 'Nood sofa bed', 2, 1, '2024-03-15', 230, 3, 'Picture168.jpg'),
  (169, 'Luca 3.5 Seater fabric couch', 2, 1, '2024-05-10', 1000, 2, 'Picture169.jpg'),
  (170, 'Luca 1 Seater fabric armchair', 2, 1, '2024-05-10', 200, 2, 'Picture170.jpg'),
  (171, 'Outdoor table', 2, 1, '2024-05-10', 100, 2, 'Picture171.jpg'),
  (172, 'Lounge suite', 2, 2, '2024-06-21', 650, 3, 'Picture172.jpg'),
  (173, 'Hunter Fabric couch 3 seater', 2, 1, '2024-06-29', 100, 2, 'Picture173.jpg'),
  (174, 'Farmers 3 seater fabric couch', 2, 2, '2024-06-28', 80, 2, 'Picture174.jpg'),
  (175, 'Beautyrest Super King Bed', 1, 2, '2024-06-14', 500, 2, 'Picture175.jpg'),
  (176, 'Harvey Norman Leather couch 2 seater', 2, 2, '2024-06-28', 90, 2, 'Picture176.jpg'),
  (177, 'Sleepyhead Super King bed - Matrix', 1, 2, '2024-06-29', 580, 2, 'Picture177.jpg'),
  (178, 'Stressfree chair', 2, 2, '2024-06-30', 650, 3, 'Picture178.jpg'),
  (179, 'Sofa bed', 2, 2, '2024-06-30', 50, 2, 'Picture179.jpg'),
  (180, 'SleepMaker King bed', 1, 2, '2024-06-30', 400, 2, 'Picture180.jpg'),
  (181, 'Beautyrest Queen bed', 1, 2, '2024-07-01', 635.00, 2, 'Picture181.jpg'),
  (182, 'Super King Mattress', 1, 2, '2024-07-03', 1.00, 2, 'Picture182.jpg'),
  (183, 'Luca 2 Seater + 2 Armchairs', 2, 2, '2024-07-06', 850.00, 3, 'Picture183.jpg'),
  (184, '2 seater couch', 2, 2, '2024-07-01', 50.00, 3, 'Picture184.jpg');


-- 插入销售数据
INSERT INTO sales (product_id, sell_date, sell_price, sell_platform_id, fees)
VALUES
  (168, '2024-06-21', 420.0, 3, 0),
  (169, '2024-06-03', 1300.0, 3, 0),
  (170, '2024-06-15', 550.0, 3, 0),
  (171, '2024-06-15', 200.0, 3, 0),
  (173, '2024-06-30', 230.0, 3, 0);

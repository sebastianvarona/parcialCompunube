
-- Users Database
CREATE DATABASE IF NOT EXISTS myflaskapp_users;
USE myflaskapp_users;

CREATE TABLE IF NOT EXISTS users (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name varchar(255),
    email varchar(255),
    username varchar(255),
    password varchar(255)
);

INSERT INTO users VALUES(null, "juan", "juan@gmail.com", "juan", "123"),
    (null, "maria", "maria@gmail.com", "maria", "456");

-- Products Database
CREATE DATABASE IF NOT EXISTS myflaskapp_products;
USE myflaskapp_products;

CREATE TABLE IF NOT EXISTS products (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name varchar(255) NOT NULL,
    price float NOT NULL,
    quantity int NOT NULL
);

INSERT INTO products VALUES(null, "Laptop", 999.99, 10),
    (null, "Mouse", 29.99, 50),
    (null, "Keyboard", 79.99, 30),
    (null, "Monitor", 299.99, 15);

-- Orders Database
CREATE DATABASE IF NOT EXISTS myflaskapp_orders;
USE myflaskapp_orders;

CREATE TABLE IF NOT EXISTS orders (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_name varchar(255) NOT NULL,
    user_email varchar(255),
    total float NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_items (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    order_id int NOT NULL,
    product_id int NOT NULL,
    product_name varchar(255),
    quantity int NOT NULL,
    price float NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

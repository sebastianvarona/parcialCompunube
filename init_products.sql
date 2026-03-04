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

create database amazon_data;
USE amazon_data;

CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(255) UNIQUE
);

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    URL VARCHAR(255),
    title VARCHAR(255),
    asin VARCHAR(255),
    ratings DECIMAL(3, 2),
    price DECIMAL(10, 2),
    gender VARCHAR(50),
    category_id INT,
    sub_category VARCHAR(255),
    brand_name VARCHAR(255),
    description TEXT,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE colors (
    color_id INT AUTO_INCREMENT PRIMARY KEY,
    color_name VARCHAR(50) UNIQUE
);

CREATE TABLE product_colors (
    product_id INT,
    color_id INT,
    PRIMARY KEY (product_id, color_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (color_id) REFERENCES colors(color_id)
);

CREATE TABLE reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    review TEXT,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);



show tables;




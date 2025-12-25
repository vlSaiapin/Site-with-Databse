CREATE DATABASE kursova;

USE kursova;

CREATE TABLE `categories` (
    `category_id` int NOT NULL AUTO_INCREMENT,
    `category_name` varchar(100) NOT NULL,
    `description` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`category_id`)
) ENGINE = InnoDB AUTO_INCREMENT = 5 DEFAULT CHARSET = utf8mb4;

CREATE TABLE `suppliers` (
    `supplier_id` int NOT NULL AUTO_INCREMENT,
    `supplier_name` varchar(100) NOT NULL,
    `phone` varchar(20) NOT NULL,
    `email` varchar(100) DEFAULT NULL,
    `address` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`supplier_id`)
) ENGINE = InnoDB AUTO_INCREMENT = 10 DEFAULT CHARSET = utf8mb4;

CREATE TABLE `customers` (
    `customer_id` int NOT NULL AUTO_INCREMENT,
    `first_name` varchar(100) NOT NULL,
    `last_name` varchar(100) DEFAULT NULL,
    `phone` varchar(20) NOT NULL,
    `email` varchar(100) DEFAULT NULL,
    `address` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`customer_id`)
) ENGINE = InnoDB AUTO_INCREMENT = 4 DEFAULT CHARSET = utf8mb4;

CREATE TABLE `employees` (
    `employee_id` int NOT NULL AUTO_INCREMENT,
    `first_name` varchar(100) NOT NULL,
    `last_name` varchar(100) NOT NULL,
    `position` varchar(100) NOT NULL,
    `phone` varchar(20) NOT NULL,
    PRIMARY KEY (`employee_id`)
) ENGINE = InnoDB AUTO_INCREMENT = 3 DEFAULT CHARSET = utf8mb4;

CREATE TABLE `products` (
    `product_id` int NOT NULL AUTO_INCREMENT,
    `product_name` varchar(255) NOT NULL,
    `category_id` int NOT NULL,
    `supplier_id` int NOT NULL,
    `price` decimal(10, 2) NOT NULL,
    `unit` varchar(20) NOT NULL,
    PRIMARY KEY (`product_id`),
    KEY `fk_products_category` (`category_id`),
    KEY `fk_products_supplier` (`supplier_id`),
    CONSTRAINT `fk_products_category` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`),
    CONSTRAINT `fk_products_supplier` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`supplier_id`)
) ENGINE = InnoDB AUTO_INCREMENT = 13 DEFAULT CHARSET = utf8mb4;

CREATE TABLE `orders` (
    `order_id` int NOT NULL AUTO_INCREMENT,
    `customer_id` int NOT NULL,
    `employee_id` int NOT NULL,
    `order_date` datetime NOT NULL,
    `status` varchar(20) NOT NULL,
    PRIMARY KEY (`order_id`),
    KEY `fk_orders_customer` (`customer_id`),
    KEY `fk_orders_employee` (`employee_id`),
    CONSTRAINT `fk_orders_customer` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `fk_orders_employee` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 4 DEFAULT CHARSET = utf8mb4;

CREATE TABLE `order_items` (
    `order_item_id` int NOT NULL AUTO_INCREMENT,
    `order_id` int NOT NULL,
    `product_id` int NOT NULL,
    `quantity` int NOT NULL,
    `price_at_order` decimal(10, 2) NOT NULL,
    PRIMARY KEY (`order_item_id`),
    KEY `fk_order_items_order` (`order_id`),
    KEY `fk_order_items_product` (`product_id`),
    CONSTRAINT `fk_order_items_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_order_items_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 7 DEFAULT CHARSET = utf8mb4;

CREATE TABLE `warehouse` (
    `warehouse_id` int NOT NULL AUTO_INCREMENT,
    `product_id` int NOT NULL,
    `quantity_in_stock` int NOT NULL,
    `last_update` datetime NOT NULL,
    PRIMARY KEY (`warehouse_id`),
    KEY `fk_warehouse_product` (`product_id`),
    CONSTRAINT `fk_warehouse_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 7 DEFAULT CHARSET = utf8mb4;
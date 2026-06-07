CREATE DATABASE smart_clinic;

USE smart_clinic;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(255),
    role VARCHAR(50)
);

CREATE TABLE patients (
    patient_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(20),
    city VARCHAR(100),
    phone VARCHAR(20),
    height FLOAT,
    weight FLOAT,
    bmi FLOAT,
    verdict VARCHAR(50),
    created_at DATETIME,
    updated_at DATETIME,
    created_by VARCHAR(100)
);
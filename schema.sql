CREATE DATABASE school_db;

USE school_db;

CREATE TABLE student (
	student_id INT PRIMARY KEY,
    student_name VARCHAR(255),
    class varchar(25),
    gender VARCHAR(10),
    phone_number VARCHAR(25),
    email VARCHAR(50),
    address VARCHAR(25)
);
CREATE TABLE parents (
	parent_id INT PRIMARY KEY,
    parent_name VARCHAR(255) NOT NULL,
    student_id INT,
    parent_phoneNumber VARCHAR(15),
    parent_email VARCHAR(50),
    FOREIGN KEY(student_id) REFERENCES student(student_id) ON DELETE CASCADE
);

CREATE TABLE student_parent (
	student_id INT,
    parent_id INT,
	FOREIGN KEY(student_id) REFERENCES student(student_id) ON DELETE CASCADE,
	FOREIGN KEY(parent_id) REFERENCES parents(parent_id) ON DELETE CASCADE
);

CREATE TABLE users (
	id INT PRIMARY KEY,
	full_name varchar(255),
    username VARCHAR(255),
    password VARCHAR(255)
);

INSERT INTO users (id, full_name, username, password)  VALUES (1, 'admin', 'a', '1');

SELECT * FROM student;
SELECT * FROM users;
SELECT * FROM parents;

DROP TABLE users;
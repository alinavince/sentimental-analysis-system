-- ============================================================
-- Smart Sentiment Analysis System - MySQL Database Setup
-- Run this in MySQL Workbench before starting the Django server
-- ============================================================

-- Step 1: Create the database
CREATE DATABASE IF NOT EXISTS sentiment_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Step 2: Create the user (change password as needed)
CREATE USER IF NOT EXISTS 'sentiment_user'@'localhost' IDENTIFIED BY 'sentiment@123';

-- Step 3: Grant privileges
GRANT ALL PRIVILEGES ON sentiment_db.* TO 'sentiment_user'@'localhost';
FLUSH PRIVILEGES;

-- Step 4: Use the database
USE sentiment_db;

-- Step 5: (Optional) Verify
SHOW DATABASES LIKE 'sentiment_db';
SELECT User, Host FROM mysql.user WHERE User = 'sentiment_user';

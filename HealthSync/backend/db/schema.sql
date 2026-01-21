-- HealthSync Database Schema

-- Create a table for users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a table for health metrics
CREATE TABLE health_metrics (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    weight DECIMAL(5, 2),
    height DECIMAL(5, 2),
    blood_pressure VARCHAR(10),
    heart_rate INT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create an index on user_id in health_metrics for faster queries
CREATE INDEX idx_user_id ON health_metrics(user_id);
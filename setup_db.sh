#!/bin/bash

# Database setup script for Note Cloud application

echo "Setting up database for Note Cloud application..."

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL is not installed. Please install PostgreSQL first."
    exit 1
fi

# Database configuration
DB_NAME="MyDB"
DB_USER="postgres"
DB_PASSWORD="QusaiPOSTGRES204"

# Check if database exists
if sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    echo "Database $DB_NAME already exists."
else
    echo "Creating database $DB_NAME..."
    sudo -u postgres psql -c "CREATE DATABASE \"$DB_NAME\";"
    echo "Database created successfully."
fi

# Create tables if they don't exist
echo "Creating tables if they don't exist..."

# Connect to the database and create tables
sudo -u postgres psql -d $DB_NAME -c "
-- Create user table if it doesn't exist
CREATE TABLE IF NOT EXISTS \"user\" (
    id SERIAL PRIMARY KEY,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(150) NOT NULL,
    first_name VARCHAR(150) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    log_status INTEGER DEFAULT 0
);

-- Create note table if it doesn't exist
CREATE TABLE IF NOT EXISTS note (
    id SERIAL PRIMARY KEY,
    data TEXT NOT NULL,
    user_id INTEGER REFERENCES \"user\"(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create access_log table if it doesn't exist
CREATE TABLE IF NOT EXISTS access_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES \"user\"(id),
    action VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(50),
    user_agent VARCHAR(255)
);

-- Create settings table if it doesn't exist
CREATE TABLE IF NOT EXISTS settings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES \"user\"(id),
    theme VARCHAR(20) DEFAULT 'light',
    font_size VARCHAR(10) DEFAULT 'medium',
    notes_per_page INTEGER DEFAULT 10,
    email_notifications BOOLEAN DEFAULT FALSE
);

-- Create backup table if it doesn't exist
CREATE TABLE IF NOT EXISTS backup (
    id SERIAL PRIMARY KEY,
    note_id INTEGER REFERENCES note(id),
    data TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"

echo "Database setup completed successfully!"

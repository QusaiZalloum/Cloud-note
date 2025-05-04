#!/bin/bash

# Start script for Note Cloud application

echo "Starting Note Cloud application..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if the database setup script exists and is executable
if [ -f "./setup_db.sh" ]; then
    echo "Running database setup script..."
    ./setup_db.sh
else
    echo "Database setup script not found. Please run setup_db.sh manually."
fi

# Install required packages
echo "Installing required Python packages..."
pip3 install flask flask-sqlalchemy flask-login flask-bcrypt psycopg2-binary pytz

# Start the application
echo "Starting the Flask application..."
python3 main.py

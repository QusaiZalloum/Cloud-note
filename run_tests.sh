#!/bin/bash

# Test script for Note Cloud application

echo "Running tests for Note Cloud application..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create test directory if it doesn't exist
mkdir -p tests

# Create test file
cat > tests/test_app.py << 'EOF'
import sys
import os
import unittest
from flask import Flask
from flask_testing import TestCase

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from website import create_app
from website.models import db, User, Note, AccessLog, Settings, Backup

class TestNoteCloudApp(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def test_app_exists(self):
        self.assertIsNotNone(self.app)
        
    def test_home_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        
    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
        
    def test_signup_page(self):
        response = self.client.get('/sign-up')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign Up', response.data)
        
    def test_user_model(self):
        user = User(email='test@example.com', first_name='Test', password='password123')
        db.session.add(user)
        db.session.commit()
        
        retrieved_user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.first_name, 'Test')
        
    def test_note_model(self):
        user = User(email='test@example.com', first_name='Test', password='password123')
        db.session.add(user)
        db.session.commit()
        
        note = Note(data='Test note content', user_id=user.id)
        db.session.add(note)
        db.session.commit()
        
        retrieved_note = Note.query.filter_by(user_id=user.id).first()
        self.assertIsNotNone(retrieved_note)
        self.assertEqual(retrieved_note.data, 'Test note content')
        
    def test_settings_model(self):
        user = User(email='test@example.com', first_name='Test', password='password123')
        db.session.add(user)
        db.session.commit()
        
        settings = Settings(user_id=user.id, theme='dark', font_size='large')
        db.session.add(settings)
        db.session.commit()
        
        retrieved_settings = Settings.query.filter_by(user_id=user.id).first()
        self.assertIsNotNone(retrieved_settings)
        self.assertEqual(retrieved_settings.theme, 'dark')
        self.assertEqual(retrieved_settings.font_size, 'large')
        
    def test_access_log_model(self):
        user = User(email='test@example.com', first_name='Test', password='password123')
        db.session.add(user)
        db.session.commit()
        
        log = AccessLog(user_id=user.id, action='Login', ip_address='127.0.0.1')
        db.session.add(log)
        db.session.commit()
        
        retrieved_log = AccessLog.query.filter_by(user_id=user.id).first()
        self.assertIsNotNone(retrieved_log)
        self.assertEqual(retrieved_log.action, 'Login')
        
    def test_backup_model(self):
        user = User(email='test@example.com', first_name='Test', password='password123')
        db.session.add(user)
        db.session.commit()
        
        note = Note(data='Original content', user_id=user.id)
        db.session.add(note)
        db.session.commit()
        
        backup = Backup(note_id=note.id, data='Original content')
        db.session.add(backup)
        db.session.commit()
        
        retrieved_backup = Backup.query.filter_by(note_id=note.id).first()
        self.assertIsNotNone(retrieved_backup)
        self.assertEqual(retrieved_backup.data, 'Original content')

if __name__ == '__main__':
    unittest.main()
EOF

# Install test dependencies
echo "Installing test dependencies..."
pip3 install flask-testing

# Run the tests
echo "Running tests..."
python3 -m unittest discover -s tests

echo "Tests completed!"

# Note Cloud - Web Application Documentation

## Project Overview
Note Cloud is a web-based note-taking application that allows users to securely store and organize their notes online. The application provides user authentication, note management, and cloud accessibility features.

## Features
- User Registration and Authentication
- Note Management (Create, Read, Update, Delete)
- User Settings Customization
- Activity Logging
- Note Backup System
- Responsive Design

## Technical Stack
- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Security**: Flask-Bcrypt, Flask-Login

## Directory Structure
```
website_updated/
├── main.py                    # Application entry point
├── setup_db.sh                # Database setup script
├── start.sh                   # Application startup script
├── run_tests.sh               # Automated tests script
├── manual_test_checklist.sh   # Manual testing guide
├── website/                   # Main application package
│   ├── __init__.py            # Flask application factory
│   ├── models.py              # Database models
│   ├── auth.py                # Authentication routes
│   ├── views.py               # Main application routes
│   ├── static/                # Static files
│   │   ├── css/               # CSS stylesheets
│   │   └── js/                # JavaScript files
│   └── templates/             # HTML templates
│       ├── base.html          # Base template
│       ├── home.html          # Home page
│       ├── login.html         # Login page
│       ├── sign_up.html       # Registration page
│       ├── edit_note.html     # Note editing page
│       ├── settings.html      # User settings page
│       └── activity_log.html  # Activity log page
└── tests/                     # Test directory
    └── test_app.py            # Unit tests
```

## Installation and Setup

### Prerequisites
- Python 3.6 or higher
- PostgreSQL database
- pip (Python package manager)

### Setup Instructions
1. Clone or download the application files
2. Make the setup scripts executable:
   ```
   chmod +x setup_db.sh start.sh run_tests.sh
   ```
3. Run the database setup script:
   ```
   ./setup_db.sh
   ```
4. Start the application:
   ```
   ./start.sh
   ```
5. Access the application at http://localhost:5000

### Database Configuration
The application is configured to connect to a PostgreSQL database with the following settings:
- Database Name: MyDB
- Username: postgres
- Password: QusaiPOSTGRES204
- Host: localhost
- Port: 5432

You can modify these settings in the `__init__.py` file if needed.

## Application Structure

### Models
- **User**: Stores user credentials and profile information
- **Note**: Stores the content of user-created notes
- **AccessLog**: Keeps track of user activity for security and monitoring
- **Settings**: Stores user preferences and configurations
- **Backup**: Stores backup copies of notes for data recovery

### Routes
- **Authentication Routes** (`auth.py`):
  - `/login`: User login
  - `/logout`: User logout
  - `/sign-up`: User registration
  - `/`: Index route (redirects to login or home)

- **View Routes** (`views.py`):
  - `/home`: Main notes dashboard
  - `/create-note`: Create a new note
  - `/edit-note/<note_id>`: Edit an existing note
  - `/delete-note/<note_id>`: Delete a note
  - `/settings`: User settings management
  - `/activity-log`: View user activity history

## Security Features
- Password hashing using bcrypt
- SQL injection protection with parameterized queries
- Session management with Flask-Login
- Activity logging for security monitoring
- Input validation and sanitization

## Testing
The application includes both automated and manual testing capabilities:

### Automated Tests
Run the automated tests using:
```
./run_tests.sh
```

These tests verify:
- Database models functionality
- Route accessibility
- Basic application logic

### Manual Tests
A comprehensive manual testing checklist is provided in `manual_test_checklist.sh`. Run it to view the checklist:
```
./manual_test_checklist.sh
```

## Future Improvements
As outlined in the project proposal, future improvements could include:
- Cloud hosting deployment
- Advanced search and tagging system
- Collaboration tools
- Mobile application
- Voice-to-text feature
- Dark mode and UI customization (partially implemented)
- Automatic backups and restores (partially implemented)

## Troubleshooting
- If you encounter database connection issues, verify PostgreSQL is running and the credentials are correct
- For package installation issues, try running `pip install -r requirements.txt` manually
- Check the application logs for detailed error information

## Credits
Developed by Kusai Zalloum and Kareem Zalloum
Completed and enhanced by Manus AI

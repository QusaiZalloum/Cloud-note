#!/bin/bash

# Manual test checklist for Note Cloud application

echo "Manual Test Checklist for Note Cloud Application"
echo "==============================================="
echo ""
echo "This checklist helps verify that all features of the Note Cloud application"
echo "are working correctly. Follow these steps to manually test the application."
echo ""

cat << 'EOF'
## Authentication Tests

1. User Registration
   - [ ] Navigate to /sign-up
   - [ ] Enter valid email, name, and matching passwords
   - [ ] Verify successful account creation and redirection to home page
   - [ ] Try registering with an existing email and verify error message
   - [ ] Try registering with mismatched passwords and verify error message
   - [ ] Try registering with a short password and verify error message

2. User Login
   - [ ] Navigate to /login
   - [ ] Enter valid credentials and verify successful login
   - [ ] Enter invalid email and verify error message
   - [ ] Enter invalid password and verify error message
   - [ ] Verify session persistence (stay logged in after page refresh)

3. User Logout
   - [ ] Click logout link when logged in
   - [ ] Verify redirection to login page
   - [ ] Verify inability to access protected pages after logout

## Note Management Tests

4. Note Creation
   - [ ] Navigate to home page when logged in
   - [ ] Enter note content and submit
   - [ ] Verify note appears in the list
   - [ ] Try submitting empty note and verify error message

5. Note Editing
   - [ ] Click edit button on an existing note
   - [ ] Modify content and save
   - [ ] Verify changes are reflected in the note list
   - [ ] Verify updated timestamp is shown

6. Note Deletion
   - [ ] Click delete button on an existing note
   - [ ] Confirm deletion in the prompt
   - [ ] Verify note is removed from the list

## Settings Tests

7. User Settings
   - [ ] Navigate to /settings
   - [ ] Change theme, font size, and notes per page settings
   - [ ] Save changes and verify success message
   - [ ] Verify settings are applied to the interface
   - [ ] Toggle email notifications and verify the change is saved

8. Activity Log
   - [ ] Navigate to /activity-log
   - [ ] Verify login, note creation, and other activities are recorded
   - [ ] Verify timestamps, actions, and other details are correct

## Security Tests

9. Authentication Protection
   - [ ] Try accessing /home, /settings, or /activity-log without logging in
   - [ ] Verify redirection to login page
   - [ ] Try accessing another user's notes (if multiple test users exist)
   - [ ] Verify proper error handling for unauthorized access

10. Input Validation
    - [ ] Try submitting form data with special characters
    - [ ] Try submitting very long input strings
    - [ ] Verify proper handling and escaping of user input

## UI/UX Tests

11. Responsive Design
    - [ ] Test the application on different screen sizes
    - [ ] Verify layout adjusts appropriately for mobile, tablet, and desktop
    - [ ] Verify all elements are accessible and usable on small screens

12. Browser Compatibility
    - [ ] Test the application in different browsers (Chrome, Firefox, Safari)
    - [ ] Verify consistent appearance and functionality across browsers

## Performance Tests

13. Load Time
    - [ ] Measure page load times for different sections
    - [ ] Verify acceptable performance with multiple notes

14. Error Handling
    - [ ] Intentionally cause errors (e.g., disconnect database)
    - [ ] Verify appropriate error messages are displayed
    - [ ] Verify application recovers gracefully from errors
EOF

echo ""
echo "To run the application for testing:"
echo "1. Execute ./setup_db.sh to set up the database"
echo "2. Execute ./start.sh to start the application"
echo "3. Access the application at http://localhost:5000"
echo ""
echo "After completing the tests, document any issues found and their severity."

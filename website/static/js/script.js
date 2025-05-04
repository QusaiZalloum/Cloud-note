// JavaScript for Note Cloud application

// Apply user settings when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Apply theme from user settings if available
    const theme = localStorage.getItem('theme') || 'light';
    const fontSize = localStorage.getItem('fontSize') || 'medium';
    
    applyTheme(theme);
    applyFontSize(fontSize);
    
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Add event listeners for theme selection if on settings page
    const themeSelect = document.getElementById('theme');
    if (themeSelect) {
        themeSelect.addEventListener('change', function() {
            applyTheme(this.value);
            localStorage.setItem('theme', this.value);
        });
    }
    
    // Add event listeners for font size selection if on settings page
    const fontSizeSelect = document.getElementById('font_size');
    if (fontSizeSelect) {
        fontSizeSelect.addEventListener('change', function() {
            applyFontSize(this.value);
            localStorage.setItem('fontSize', this.value);
        });
    }
    
    // Add confirmation for delete actions
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this note?')) {
                e.preventDefault();
            }
        });
    });
    
    // Textarea auto-resize
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(function(textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        // Trigger the event on page load
        textarea.dispatchEvent(new Event('input'));
    });
});

// Function to apply theme
function applyTheme(theme) {
    document.body.classList.remove('theme-light', 'theme-dark', 'theme-blue');
    document.body.classList.add('theme-' + theme);
}

// Function to apply font size
function applyFontSize(size) {
    document.body.classList.remove('font-small', 'font-medium', 'font-large');
    document.body.classList.add('font-' + size);
}

// Function to validate forms
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    let isValid = true;
    
    // Email validation
    const emailInput = form.querySelector('input[type="email"]');
    if (emailInput && emailInput.value) {
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!emailRegex.test(emailInput.value)) {
            alert('Please enter a valid email address.');
            isValid = false;
        }
    }
    
    // Password validation
    const passwordInputs = form.querySelectorAll('input[type="password"]');
    if (passwordInputs.length >= 2) {
        const password1 = passwordInputs[0].value;
        const password2 = passwordInputs[1].value;
        
        if (password1 !== password2) {
            alert('Passwords do not match.');
            isValid = false;
        }
        
        if (password1.length < 7) {
            alert('Password must be at least 7 characters long.');
            isValid = false;
        }
    }
    
    return isValid;
}

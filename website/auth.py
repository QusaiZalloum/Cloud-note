from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, AccessLog, Settings, db
import re

auth = Blueprint('auth', __name__)

# Email validation regex
email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            if check_password_hash(user.password, password):
                flash(f'Welcome back, {user.first_name}!', category='success')
                login_user(user, remember=True)
                
                # Log the login action
                log = AccessLog(user_id=user.id, action="Logged in", 
                                ip_address=request.remote_addr, 
                                user_agent=request.user_agent.string)
                db.session.add(log)
                db.session.commit()
                
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, please try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    # Log the logout action
    log = AccessLog(user_id=current_user.id, action="Logged out", 
                    ip_address=request.remote_addr, 
                    user_agent=request.user_agent.string)
    db.session.add(log)
    db.session.commit()
    
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Email already exists.', category='error')
        elif not email_regex.match(email):
            flash('Email is invalid.', category='error')
        elif len(first_name) < 2:
            flash('First name must be longer than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Create new user with hashed password
            new_user = User(
                email=email,
                first_name=first_name,
                password=generate_password_hash(password1, method='pbkdf2:sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            
            # Create default settings for the user
            user_settings = Settings(user_id=new_user.id)
            db.session.add(user_settings)
            
            # Log the registration
            log = AccessLog(user_id=new_user.id, action="Registered account", 
                            ip_address=request.remote_addr, 
                            user_agent=request.user_agent.string)
            db.session.add(log)
            db.session.commit()
            
            login_user(new_user, remember=True)
            flash('Account created successfully!', category='success')
            return redirect(url_for('views.home'))
    
    return render_template("sign_up.html", user=current_user)

@auth.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    else:
        return redirect(url_for('auth.login'))

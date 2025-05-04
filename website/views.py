from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Note, AccessLog, db
from datetime import datetime
import pytz

views = Blueprint('views', __name__)

@views.route('/home')
@login_required
def home():
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.updated_at.desc()).all()
    return render_template('home.html', user=current_user, notes=notes)

@views.route('/create-note', methods=['POST'])
@login_required
def create_note():
    note = request.form.get('note')

    if not note or len(note) < 1:
        flash('Note cannot be empty', category='error')
    else:
        new_note = Note(data=note, user_id=current_user.id)
        db.session.add(new_note)
        
        # Log the action
        log = AccessLog(user_id=current_user.id, action="Created note", 
                        ip_address=request.remote_addr, 
                        user_agent=request.user_agent.string)
        db.session.add(log)
        
        db.session.commit()
        flash('Note added!', category='success')
    
    return redirect(url_for('views.home'))

@views.route('/delete-note/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get(note_id)
    
    if not note:
        flash('Note not found.', category='error')
    elif note.user_id != current_user.id:
        flash('You do not have permission to delete this note.', category='error')
    else:
        db.session.delete(note)
        
        # Log the action
        log = AccessLog(user_id=current_user.id, action=f"Deleted note {note_id}", 
                        ip_address=request.remote_addr, 
                        user_agent=request.user_agent.string)
        db.session.add(log)
        
        db.session.commit()
        flash('Note deleted!', category='success')
    
    return redirect(url_for('views.home'))

@views.route('/edit-note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get(note_id)
    
    if not note:
        flash('Note not found.', category='error')
        return redirect(url_for('views.home'))
    
    if note.user_id != current_user.id:
        flash('You do not have permission to edit this note.', category='error')
        return redirect(url_for('views.home'))
    
    if request.method == 'POST':
        note_content = request.form.get('note')
        
        if not note_content or len(note_content) < 1:
            flash('Note cannot be empty', category='error')
        else:
            # Create backup of the original note
            from .models import Backup
            backup = Backup(note_id=note.id, data=note.data)
            db.session.add(backup)
            
            # Update the note
            note.data = note_content
            note.updated_at = datetime.now(pytz.UTC)
            
            # Log the action
            log = AccessLog(user_id=current_user.id, action=f"Edited note {note_id}", 
                            ip_address=request.remote_addr, 
                            user_agent=request.user_agent.string)
            db.session.add(log)
            
            db.session.commit()
            flash('Note updated!', category='success')
            return redirect(url_for('views.home'))
    
    return render_template('edit_note.html', note=note, user=current_user)

@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    from .models import Settings
    
    # Get or create user settings
    user_settings = Settings.query.filter_by(user_id=current_user.id).first()
    if not user_settings:
        user_settings = Settings(user_id=current_user.id)
        db.session.add(user_settings)
        db.session.commit()
    
    if request.method == 'POST':
        theme = request.form.get('theme')
        font_size = request.form.get('font_size')
        notes_per_page = request.form.get('notes_per_page')
        email_notifications = 'email_notifications' in request.form
        
        user_settings.theme = theme
        user_settings.font_size = font_size
        user_settings.notes_per_page = int(notes_per_page)
        user_settings.email_notifications = email_notifications
        
        # Log the action
        log = AccessLog(user_id=current_user.id, action="Updated settings", 
                        ip_address=request.remote_addr, 
                        user_agent=request.user_agent.string)
        db.session.add(log)
        
        db.session.commit()
        flash('Settings updated!', category='success')
        return redirect(url_for('views.settings'))
    
    return render_template('settings.html', user=current_user, settings=user_settings)

@views.route('/activity-log')
@login_required
def activity_log():
    logs = AccessLog.query.filter_by(user_id=current_user.id).order_by(AccessLog.timestamp.desc()).limit(50).all()
    return render_template('activity_log.html', user=current_user, logs=logs)

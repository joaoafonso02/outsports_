from flask import Blueprint, render_template, request, flash, jsonify,redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from .models import Note
from . import db
import json
from datetime import date


views = Blueprint('views', __name__)


# HOME PAGE
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


# YOUR SPORTS PAGE
@views.route('/your_sports', methods=['GET', 'POST'])
@login_required
def your_sports():
    # Get the user's sports field
    sports = current_user.data['sports']
    return render_template("your_sports.html", user=current_user, sports=sports)

@views.route('/todo_sports', methods=['GET', 'POST'])
@login_required
def add_sport():
    if request.method == 'POST':
        title = request.form.get('title')
        completed = 'completed' in request.form

        # Create a new todo dictionary
        new_todo = {'title': title, 'completed': completed}

        # Update the "sports" array in the "data" field, i want: data = db.DictField(default={'sports': [], 'gallery': [], 'calendar': []})
        current_user.update(push__data__sports=new_todo)
        
        flash('Sport added!', category='success')       
        
        return redirect(url_for('views.your_sports'))

    return render_template("your_sports.html", user=current_user)

@views.route('/delete_sport', methods=['GET', 'POST'])
def delete_sport():
    sport_title = request.args.get('title')
    current_user.update(pull__data__sports__title=sport_title)
    return redirect(url_for('views.your_sports'))
  
@views.route('/update_sports', methods=['GET', 'POST'])
def update_sports():
    if request.method == 'POST':
        print("POST")
        return redirect(url_for('views.your_sports'))

    return redirect(url_for('views.your_sports'))


# NOTES PAGE
@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST': 
        note_text = request.form.get('note')

        if len(note_text) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note_text, user=current_user)
            new_note.save()

            # Update the user's notes field
            current_user.update(push__notes=new_note)

            flash('Note added!', category='success')
            
            # Redirect to the same page after a successful POST
            return redirect(url_for('views.notes'))

    return render_template("notes.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note_data = json.loads(request.data)
    note_id = note_data['noteId']

    try:
        note = Note.objects.get(id=note_id)
        print(note_id)
        
        # delete the note from the user's notes field
        current_user.update(pull__notes=note)
        note.delete()
        return jsonify({'success': True})

    except Note.DoesNotExist:
        print("DOESNOTEXIST")
        return jsonify({'success': False, 'error': 'Note not found'})
    except Exception as e:
        print("lol")
        return jsonify({'success': False, 'error': str(e)})


# GALLERY PAGE
@views.route('/gallery', methods=['GET', 'POST'])
@login_required
def gallery():
    return render_template("gallery.html", user=current_user)

@views.route('/add_to_gallery', methods=['GET', 'POST'])
@login_required
def add_to_gallery():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image = request.files['image']

        filename = secure_filename(image.filename)
        image.save(os.path.join('website/static/img/uploaded_files', filename))
        
        new_image = {'title': title, 'description': description, 'image': filename}
        current_user.update(push__data__gallery=new_image)
        
        flash('Image added!', category='success')
        return redirect(url_for('views.gallery'))
    return render_template("gallery.html", user=current_user)

@views.route('/delete_gallery_image', methods=['GET', 'POST'])
def delete_gallery_image():
    image_title = request.args.get('title')
    print(image_title)
    current_user.update(pull__data__gallery__title=image_title)
    return redirect(url_for('views.gallery'))


# CALENDAR PAGE
@views.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    time = date.today()
    
    day = time.strftime("%A")
    
    return render_template("calendar.html", user=current_user, day=day)

@views.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['due_date']
        repeat_option = request.form['repeat_option']
        
        new_event = {'title': title, 'description': description, 'date': date, 'repeat_option': repeat_option}
        
        # Check if the title contains "surf"
        if 'kitesurf' in title.lower() or 'kiteboarding' in title.lower() or 'kite' in title.lower():
            new_event['image_path'] = '/img/kitesurf.jpg'
        elif 'surf' in title.lower() or 'surfing' in title.lower():
            new_event['image_path'] = '/img/surf.jpg'
        elif 'skate' in title.lower() or 'skating' in title.lower():
            new_event['image_path'] = '/img/skate.jpg'
        elif 'bike' in title.lower() or 'biking' in title.lower():
            new_event['image_path'] = '/img/bike.jpg'
        elif 'football' in title.lower() or 'soccer' in title.lower() or 'futebol' in title.lower() or 'fútebol' in title.lower():
            new_event['image_path'] = '/img/roni.jpg'
        
        current_user.update(push__data__calendar=new_event)
        
        flash('Event added!', category='success')
        return redirect(url_for('views.calendar'))
    
    return render_template("calendar.html", user=current_user)

@views.route('/delete_calendar_event', methods=['GET', 'POST'])
def delete_calendar_event():
    event_title = request.args.get('title')
    current_user.update(pull__data__calendar__title=event_title)
    return redirect(url_for('views.calendar'))


# PROFILE PAGE
@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@views.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        # Check if the form data exists before accessing it
        email = request.form.get('email', current_user.email)
        name = request.form.get('name', current_user.name)
        contact = request.form.get('contact', current_user.contact)
        country = request.form.get('country', current_user.country)
        
        current_user.update(email=email, name=name, contact=contact, country=country)
        
        flash('Profile updated!', category='success')
        return redirect(url_for('views.profile'))
    
    return render_template("profile.html", user=current_user)

@views.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    current_password = request.form.get('currentPassword')
    new_password = request.form.get('newPassword')
    confirm_password = request.form.get('confirmPassword')

    if not current_user.check_password(current_password):
        print("Wrong password, try again!")
        flash('Wrong password, try again!', category='error')
    elif new_password != confirm_password:
        print("Passwords don't match!")
        flash('Passwords don\'t match!', category='error')
    else:
        print("Password changed successfully!")
        current_user.set_password(new_password)
        current_user.update(password=current_user.password_hash)

    flash('Password changed successfully!', category='success')
    return redirect(url_for('views.profile'))

@views.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    current_user.delete()
    return redirect(url_for('auth.logout'))

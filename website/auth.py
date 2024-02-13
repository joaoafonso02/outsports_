from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_status = None  

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.objects(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            login_status = 'success'
            return redirect(url_for('views.home', id=user.id))
        else:
            login_status = 'failure'
    
    print(login_status)
    return render_template("login.html", user=current_user, login_status=login_status)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    error_message = None
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.objects(email=email).first()  
        if user:
            error_message = 'Email already exists.'
        elif len(email) < 4:
            error_message = 'Email must be greater than 3 characters.'
        elif len(name) < 2:
            error_message = 'First name must be greater than 1 character.'
        elif password1 != password2:
            error_message = 'Passwords don\'t match.'
        elif len(password1) < 4:
            error_message = 'Password must be at least 4 characters.'
        else:
            hashed_password = generate_password_hash(password1, method='pbkdf2:sha256')
            new_user = User(email=email, name=name, password=hashed_password)

            new_user.save()  # Save the new user to the MongoDB collection
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
        
    print(error_message)

    return render_template("login.html", user=current_user, error_message=error_message)

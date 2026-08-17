import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegistrationForm, LoginForm
from app.services.mongo_service import User

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.create(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower(),
            password=form.password.data
        )
        flash('Account created successfully! Welcome to Virtual Study Group.', 'success')
        login_user(user)
        return redirect(url_for('main.dashboard'))
        
    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data.strip())
        if not user:
            # Check by email as well
            user = User.get_by_email(form.username.data.strip().lower())

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page or url_for('main.dashboard'))
        
        flash('Invalid username/email or password.', 'danger')
        
    return render_template('auth/login.html', form=form)


@bp.route('/google-login', methods=['POST'])
def google_login():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    name = data.get('name', '').strip()

    if not email:
        return jsonify({'status': 'error', 'message': 'Email not provided by Google'}), 400

    # Find existing user in MongoDB Atlas or create one
    user = User.get_by_email(email)
    if not user:
        # Generate clean username from email or name
        base_username = name.replace(' ', '_').lower() if name else email.split('@')[0]
        username = base_username
        # Handle duplicates if username exists
        counter = 1
        while User.get_by_username(username):
            username = f"{base_username}_{counter}"
            counter += 1

        user = User.create(
            username=username,
            email=email,
            password=str(uuid.uuid4())  # Random secure hash for Google Auth users
        )

    login_user(user, remember=True)
    flash(f'Welcome to Virtual Study Group, {user.username}!', 'success')
    return jsonify({'status': 'success', 'redirect': url_for('main.dashboard')})


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out safely.', 'info')
    return redirect(url_for('main.index'))
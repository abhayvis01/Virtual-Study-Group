from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.forms import RegistrationForm, LoginForm
from app.models import User
from app.extensions import db, login_manager
from app.auth import bp
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User, Group, Resource
from app.forms import GroupForm, ResourceForm
from app.extensions import db
from app.main import bp

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    groups = Group.query.filter_by(created_by=current_user.id).all()
    return render_template('dashboard.html', groups=groups)

@bp.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    form = GroupForm()
    if form.validate_on_submit():
        group = Group(
            name=form.name.data,
            description=form.description.data,
            created_by=current_user.id
        )
        db.session.add(group)
        db.session.commit()
        flash('Group created successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('create_group.html', form=form)

@bp.route('/group/<int:group_id>')
@login_required
def group(group_id):
    group = Group.query.get_or_404(group_id)
    resources = Resource.query.filter_by(group_id=group_id).all()
    return render_template('group.html', group=group, resources=resources)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('main.index'))

@bp.route('/add_resource/<int:group_id>', methods=['GET', 'POST'])
@login_required
def add_resource(group_id):
    form = ResourceForm()
    if form.validate_on_submit():
        resource = Resource(
            name=form.name.data,
            type=form.type.data,
            content=form.content.data,
            uploaded_by=current_user.id,
            group_id=group_id
        )
        db.session.add(resource)
        db.session.commit()
        flash('Resource added successfully!', 'success')
        return redirect(url_for('main.group', group_id=group_id))
    return render_template('add_resource.html', form=form)
from flask import render_template, redirect, url_for, flash, request, Blueprint, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Group, Resource
from .forms import RegistrationForm, LoginForm, GroupForm, ResourceForm
from .extensions import db, login_manager
import requests

bp = Blueprint('main', __name__)
meet_bp = Blueprint('meet', __name__)

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
        group = Group(name=form.name.data, description=form.description.data, created_by=current_user.id)
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

@bp.route('/add_resource/<int:group_id>', methods=['GET', 'POST'])
@login_required
def add_resource(group_id):
    form = ResourceForm()
    if form.validate_on_submit():
        resource = Resource(name=form.name.data, type=form.type.data, content=form.content.data, uploaded_by=current_user.id, group_id=group_id)
        db.session.add(resource)
        db.session.commit()
        flash('Resource added successfully!', 'success')
        return redirect(url_for('main.group', group_id=group_id))
    return render_template('add_resource.html', form=form)

@bp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@bp.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@meet_bp.route('/create-meeting', methods=['POST'])
def create_meeting():
    # Logic to create a Google Meet meeting using Google Meet API
    meeting_link = "https://meet.google.com/example"  # Replace with actual API call
    return jsonify({'meetingLink': meeting_link})
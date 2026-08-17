from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.mongo_service import GroupService, ResourceService, AnalyticsService
from app.forms import JoinRoomForm

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    public_groups = GroupService.get_all_public_groups()
    return render_template('index.html', public_groups=public_groups)


@bp.route('/terms')
def terms():
    return render_template('terms.html')


@bp.route('/dashboard')
@login_required
def dashboard():
    user_groups = GroupService.get_user_groups(current_user.id)
    public_groups = GroupService.get_all_public_groups()
    join_form = JoinRoomForm()
    
    # Study Analytics & Logs
    study_logs = AnalyticsService.get_user_logs(current_user.id)
    total_hours = round(current_user.total_study_minutes / 60.0, 1)
    
    # Quick statistics
    stats = {
        'total_joined': len(user_groups),
        'created_by_me': sum(1 for g in user_groups if str(g.get('created_by')) == str(current_user.id)),
        'total_hours': total_hours,
        'streak_count': getattr(current_user, 'streak_count', 1),
        'xp_points': getattr(current_user, 'xp_points', 50)
    }
    
    return render_template('dashboard.html', 
                           user_groups=user_groups, 
                           public_groups=public_groups, 
                           study_logs=study_logs,
                           stats=stats,
                           join_form=join_form)


@bp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@bp.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
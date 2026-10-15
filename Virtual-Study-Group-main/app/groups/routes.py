from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.services.mongo_service import GroupService, ResourceService, ChatService, TaskService, WhiteboardService, FlashcardService
from app.forms import GroupForm, ResourceForm, JoinRoomForm

bp = Blueprint('groups', __name__)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_group():
    form = GroupForm()
    if form.validate_on_submit():
        group = GroupService.create_group(
            name=form.name.data.strip(),
            description=form.description.data.strip(),
            category=form.category.data,
            creator_id=current_user.id
        )
        flash(f'Study Group "{group["name"]}" created! Room Code: {group["room_code"]}', 'success')
        return redirect(url_for('groups.view_group', group_id=group['_id']))
        
    return render_template('create_group.html', form=form)


@bp.route('/join', methods=['POST'])
@login_required
def join_group():
    form = JoinRoomForm()
    if form.validate_on_submit():
        code = form.room_code.data.strip().upper()
        group = GroupService.get_by_room_code(code)
        if group:
            GroupService.add_member(group['_id'], current_user.id)
            flash(f'Successfully joined "{group["name"]}"!', 'success')
            return redirect(url_for('groups.view_group', group_id=group['_id']))
        else:
            flash('Invalid room code. Please check and try again.', 'danger')
    return redirect(url_for('main.dashboard'))


@bp.route('/delete/<group_id>', methods=['POST'])
@login_required
def delete_group(group_id):
    success = GroupService.delete_group(group_id, current_user.id)
    if success:
        flash('Study room deleted successfully.', 'info')
    else:
        flash('Could not delete room or permission denied.', 'danger')
    return redirect(url_for('main.dashboard'))


@bp.route('/<group_id>')
@login_required
def view_group(group_id):
    group = GroupService.get_by_id(group_id)
    if not group:
        flash('Study group not found.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Restrict room access: only members and the creator can view the room
    is_member = str(current_user.id) in [str(m) for m in group.get('members', [])]
    is_creator = str(group.get('created_by')) == str(current_user.id)
    if not is_member and not is_creator:
        flash(f'Access Denied: You must enter the valid access code to join "{group["name"]}".', 'danger')
        return redirect(url_for('main.dashboard'))

    resources = ResourceService.get_group_resources(group_id)
    messages = ChatService.get_group_messages(group_id)
    tasks = TaskService.get_group_tasks(group_id)
    flashcards = FlashcardService.get_group_cards(group_id)
    resource_form = ResourceForm()
    
    return render_template('group.html',
                           group=group,
                           resources=resources,
                           messages=messages,
                           tasks=tasks,
                           flashcards=flashcards,
                           resource_form=resource_form)

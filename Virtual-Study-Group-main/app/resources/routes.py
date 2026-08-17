from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.mongo_service import ResourceService, GroupService
from app.services.firebase_service import FirebaseService
from app.forms import ResourceForm

bp = Blueprint('resources', __name__)

@bp.route('/add/<group_id>', methods=['GET', 'POST'])
@login_required
def add_resource(group_id):
    group = GroupService.get_by_id(group_id)
    if not group:
        flash('Group not found.', 'danger')
        return redirect(url_for('main.dashboard'))

    form = ResourceForm()
    if form.validate_on_submit():
        file_url = ""
        if form.file.data:
            _, file_url = FirebaseService.upload_file(form.file.data, folder=f"resources/{group_id}")

        ResourceService.add_resource(
            name=form.name.data.strip(),
            rtype=form.type.data,
            content=form.content.data.strip(),
            file_url=file_url,
            group_id=group_id,
            uploader_id=current_user.id
        )
        flash('Study resource added successfully!', 'success')
        return redirect(url_for('groups.view_group', group_id=group_id))

    return render_template('add_resource.html', form=form, group=group)

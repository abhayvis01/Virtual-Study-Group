import base64
import io
import mimetypes
from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file, abort
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
        filename = ""
        file_b64 = None
        file_mimetype = "application/octet-stream"

        if form.file.data and form.file.data.filename:
            file_storage = form.file.data
            filename = file_storage.filename
            file_mimetype = file_storage.content_type or mimetypes.guess_type(filename)[0] or 'application/octet-stream'

            # 1. Read file bytes for permanent cloud persistence in MongoDB Atlas
            file_bytes = file_storage.read()
            if file_bytes:
                file_b64 = base64.b64encode(file_bytes).decode('utf-8')
            file_storage.seek(0)

            # 2. Also attempt upload via Firebase Storage (or local fallback)
            _, external_url = FirebaseService.upload_file(file_storage, folder=f"resources/{group_id}")
            if external_url and external_url.startswith('http'):
                file_url = external_url

        # Create resource doc
        res_doc = ResourceService.add_resource(
            name=form.name.data.strip(),
            rtype=form.type.data,
            content=form.content.data.strip(),
            file_url=file_url,
            group_id=group_id,
            uploader_id=current_user.id,
            filename=filename,
            file_data=file_b64,
            file_mimetype=file_mimetype
        )

        # If no external cloud URL was returned, use our guaranteed permanent endpoint
        if not file_url and file_b64:
            direct_url = url_for('resources.download_resource', resource_id=res_doc['_id'])
            # Update the file_url on MongoDB
            from app.db import mongo
            if mongo.is_connected and mongo.db is not None:
                mongo.db.resources.update_one({'_id': res_doc['_id']}, {'$set': {'file_url': direct_url}})
            res_doc['file_url'] = direct_url

        flash('Study resource added and saved permanently!', 'success')
        return redirect(url_for('groups.view_group', group_id=group_id))

    return render_template('add_resource.html', form=form, group=group)

@bp.route('/download/<resource_id>')
def download_resource(resource_id):
    """
    Guaranteed cross-device file delivery endpoint.
    Serves the file directly from MongoDB cloud storage if local disk / external URL is unavailable.
    """
    res = ResourceService.get_resource_by_id(resource_id)
    if not res:
        abort(404, description="Resource not found")

    # If the file data is saved in MongoDB, serve it directly
    if res.get('file_data'):
        try:
            file_bytes = base64.b64decode(res['file_data'])
            filename = res.get('filename') or f"{res.get('name', 'resource')}.pdf"
            mimetype = res.get('file_mimetype') or 'application/octet-stream'
            return send_file(
                io.BytesIO(file_bytes),
                mimetype=mimetype,
                as_attachment=False,  # Allows viewing in browser tab (PDF viewer)
                download_name=filename
            )
        except Exception as e:
            print(f"[Resource Serve Error]: {e}")

    # Fallback to external URL if present
    if res.get('file_url') and res['file_url'].startswith('http'):
        return redirect(res['file_url'])

    abort(404, description="File content unavailable on server")

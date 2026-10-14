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
        try:
            file_url = ""
            filename = ""
            file_b64 = None
            file_mimetype = "application/octet-stream"

            if form.file.data and form.file.data.filename:
                file_storage = form.file.data
                filename = file_storage.filename
                file_mimetype = file_storage.content_type or mimetypes.guess_type(filename)[0] or 'application/octet-stream'

                # 1. Read file bytes safely (up to 15 MB)
                try:
                    file_storage.seek(0)
                    file_bytes = file_storage.read()
                    if file_bytes and len(file_bytes) < 15 * 1024 * 1024:
                        file_b64 = base64.b64encode(file_bytes).decode('utf-8')
                    file_storage.seek(0)
                except Exception as read_err:
                    print(f"[Resource Read Error]: {read_err}")
                    file_b64 = None

                # 2. Upload via Firebase Storage if available (or local disk)
                try:
                    _, external_url = FirebaseService.upload_file(file_storage, folder=f"resources/{group_id}")
                    if external_url and external_url.startswith('http'):
                        file_url = external_url
                    elif external_url:
                        file_url = external_url
                except Exception as upl_err:
                    print(f"[Upload Fallback Notice]: {upl_err}")

            # 3. Create resource doc in MongoDB Atlas
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

            # 4. Generate guaranteed permanent download URL
            if file_b64 or file_url:
                direct_url = url_for('resources.download_resource', resource_id=res_doc['_id'])
                # If we don't have an external HTTPS URL, route through our persistent endpoint
                if not (file_url and file_url.startswith('http')):
                    from app.db import mongo
                    if mongo.is_connected and mongo.db is not None:
                        mongo.db.resources.update_one({'_id': res_doc['_id']}, {'$set': {'file_url': direct_url}})
                    res_doc['file_url'] = direct_url

            flash('Study resource uploaded and saved successfully!', 'success')
            return redirect(url_for('groups.view_group', group_id=group_id))

        except Exception as e:
            import traceback
            print(f"[Add Resource Error]:\n{traceback.format_exc()}")
            flash(f'An error occurred while uploading: {str(e)}', 'danger')
            return render_template('add_resource.html', form=form, group=group)

    return render_template('add_resource.html', form=form, group=group)

@bp.route('/download/<resource_id>')
def download_resource(resource_id):
    """
    Guaranteed cross-device file delivery endpoint.
    Serves the file directly from MongoDB cloud storage if local disk / external URL is unavailable.
    """
    try:
        res = ResourceService.get_resource_by_id(resource_id)
        if not res:
            abort(404, description="Resource not found")

        # 1. If binary/base64 data exists in MongoDB, stream it directly
        if res.get('file_data'):
            try:
                file_bytes = base64.b64decode(res['file_data'])
                filename = res.get('filename') or f"{res.get('name', 'resource')}.pdf"
                mimetype = res.get('file_mimetype') or mimetypes.guess_type(filename)[0] or 'application/pdf'
                return send_file(
                    io.BytesIO(file_bytes),
                    mimetype=mimetype,
                    as_attachment=False,
                    download_name=filename
                )
            except Exception as e:
                print(f"[Resource Serve Error]: {e}")

        # 2. If stored as a local filesystem path and file exists, stream it
        file_url = res.get('file_url', '')
        if file_url and file_url.startswith('/static/'):
            local_rel = file_url.lstrip('/')
            full_path = os.path.join(current_app.root_path, local_rel.replace('static/', 'static' + os.sep))
            if os.path.exists(full_path):
                filename = res.get('filename') or os.path.basename(full_path)
                mimetype = res.get('file_mimetype') or mimetypes.guess_type(filename)[0] or 'application/octet-stream'
                return send_file(
                    full_path,
                    mimetype=mimetype,
                    as_attachment=False,
                    download_name=filename
                )

        # 3. If external HTTP/HTTPS URL exists, redirect to it
        if file_url and file_url.startswith('http'):
            return redirect(file_url)

        abort(404, description="File content unavailable on server")
    except Exception as exc:
        print(f"[Download Route Error]: {exc}")
        abort(404, description="Resource could not be loaded")

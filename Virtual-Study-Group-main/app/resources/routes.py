import os
import base64
import io
import mimetypes
from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file, abort, current_app, Response
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

            # Inspect request.files first, then form.file.data
            uploaded_file = request.files.get('file') or form.file.data
            if uploaded_file and hasattr(uploaded_file, 'filename') and uploaded_file.filename:
                filename = uploaded_file.filename.strip()
                file_mimetype = uploaded_file.content_type or mimetypes.guess_type(filename)[0] or 'application/octet-stream'

                # 1. Read file bytes safely (up to 15 MB)
                try:
                    uploaded_file.seek(0)
                    file_bytes = uploaded_file.read()
                    if file_bytes and len(file_bytes) < 15 * 1024 * 1024:
                        file_b64 = base64.b64encode(file_bytes).decode('utf-8')
                        print(f"[Resource Upload]: Read {len(file_bytes)} bytes for '{filename}'")
                    uploaded_file.seek(0)
                except Exception as read_err:
                    print(f"[Resource Read Error]: {read_err}")

                # 2. Upload via Firebase Storage if available (or local disk)
                try:
                    _, external_url = FirebaseService.upload_file(uploaded_file, folder=f"resources/{group_id}")
                    if external_url:
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

            # 4. Always ensure file_url routes through our permanent streaming endpoint if a file was attached
            if filename:
                direct_url = url_for('resources.download_resource', resource_id=res_doc['_id'])
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
                raw_b64 = res['file_data']
                if isinstance(raw_b64, str):
                    file_bytes = base64.b64decode(raw_b64)
                else:
                    file_bytes = bytes(raw_b64)
                
                filename = res.get('filename') or f"{res.get('name', 'resource')}.pdf"
                mimetype = res.get('file_mimetype') or mimetypes.guess_type(filename)[0] or 'application/pdf'
                
                response = send_file(
                    io.BytesIO(file_bytes),
                    mimetype=mimetype,
                    as_attachment=False,
                    download_name=filename
                )
                response.headers['Content-Disposition'] = f'inline; filename="{filename}"'
                response.headers['Content-Type'] = mimetype
                return response
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
                response = send_file(
                    full_path,
                    mimetype=mimetype,
                    as_attachment=False,
                    download_name=filename
                )
                response.headers['Content-Disposition'] = f'inline; filename="{filename}"'
                return response

        # 3. If external HTTP/HTTPS URL exists and is not our own endpoint, redirect to it
        if file_url and file_url.startswith('http') and '/resources/download/' not in file_url:
            return redirect(file_url)

        # 4. If neither binary data nor file exists on server (e.g. legacy upload prior to cloud persistence),
        # render a graceful study note viewer page instead of throwing raw 404
        content_text = res.get('content', '')
        res_name = res.get('name', 'Study Document')
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{res_name} - Virtual Study Group</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 2rem; display: flex; justify-content: center; align-items: center; min-height: 80vh; margin: 0; }}
                .card {{ background: #1e293b; border: 1px solid #334155; border-radius: 16px; padding: 2.5rem; max-width: 600px; width: 100%; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5); }}
                h2 {{ margin-top: 0; color: #38bdf8; display: flex; align-items: center; gap: 0.75rem; font-size: 1.5rem; }}
                .badge {{ background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; }}
                .content-box {{ background: #0f172a; border-radius: 10px; padding: 1.25rem; margin: 1.5rem 0; line-height: 1.6; border: 1px solid #334155; color: #cbd5e1; white-space: pre-wrap; }}
                .btn {{ display: inline-flex; align-items: center; gap: 0.5rem; background: #6366f1; color: white; text-decoration: none; padding: 0.75rem 1.25rem; border-radius: 10px; font-weight: 600; font-size: 0.9rem; }}
                .btn:hover {{ background: #4f46e5; }}
            </style>
        </head>
        <body>
            <div class="card">
                <span class="badge">{res.get('type', 'DOCUMENT')}</span>
                <h2><i class="fa-solid fa-file-lines"></i> {res_name}</h2>
                <p style="color: #94a3b8; font-size: 0.9rem;">
                    This resource was saved with the following description & study notes:
                </p>
                <div class="content-box">{content_text or 'No description provided.'}</div>
                <div style="display: flex; gap: 0.75rem; align-items: center;">
                    <a href="javascript:window.history.back()" class="btn"><i class="fa-solid fa-arrow-left"></i> Back to Room</a>
                    <span style="color: #64748b; font-size: 0.8rem;">💡 Please re-upload the PDF to enable in-browser binary preview.</span>
                </div>
            </div>
        </body>
        </html>
        """, 200, {'Content-Type': 'text/html; charset=utf-8'}

    except Exception as exc:
        print(f"[Download Route Error]: {exc}")
        abort(404, description="Resource could not be loaded")

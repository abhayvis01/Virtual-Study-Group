import os
import base64
import io
import mimetypes
import traceback
from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file, abort, current_app, make_response
from flask_login import login_required, current_user
from app.services.mongo_service import ResourceService, GroupService
from app.services.firebase_service import FirebaseService
from app.forms import ResourceForm

bp = Blueprint('resources', __name__)


def _read_file_bytes(file_storage):
    """Safely read all bytes from a FileStorage / file-like object, returning (bytes, filename, mimetype)."""
    if not file_storage or not getattr(file_storage, 'filename', None):
        return None, '', 'application/octet-stream'

    filename = file_storage.filename.strip()
    mimetype = (getattr(file_storage, 'content_type', None)
                or mimetypes.guess_type(filename)[0]
                or 'application/octet-stream')

    try:
        file_storage.seek(0)
        data = file_storage.read()
        file_storage.seek(0)
        if data:
            print(f"[Resource IO]: Read {len(data):,} bytes — '{filename}' ({mimetype})")
            return data, filename, mimetype
    except Exception as e:
        print(f"[Resource IO Error]: {e}")

    return None, filename, mimetype


def _store_binary(raw_bytes):
    """Convert raw bytes to bson.Binary for native MongoDB binary storage (no base64 overhead)."""
    try:
        from bson import Binary
        return Binary(raw_bytes)
    except ImportError:
        # Fallback: store as base64 string (works but +33% size)
        return base64.b64encode(raw_bytes).decode('utf-8')


def _decode_file_data(file_data):
    """Decode file_data from MongoDB — handles bson.Binary, bytes, and legacy base64 strings."""
    if file_data is None:
        return None

    # bson.Binary or raw bytes → already usable
    if isinstance(file_data, (bytes, bytearray)):
        return bytes(file_data)

    # Legacy base64 string
    if isinstance(file_data, str):
        try:
            return base64.b64decode(file_data)
        except Exception:
            return None

    return None


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
            file_binary = None
            file_mimetype = "application/octet-stream"

            # ── 1. Extract the uploaded file from request ──
            uploaded_file = request.files.get('file') or getattr(form.file, 'data', None)
            raw_bytes, filename, file_mimetype = _read_file_bytes(uploaded_file)

            if raw_bytes:
                # Store as native bson.Binary (efficient, no base64 bloat)
                file_binary = _store_binary(raw_bytes)

                # Also try Firebase/local upload for external URL backup
                try:
                    uploaded_file.seek(0)
                    _, external_url = FirebaseService.upload_file(uploaded_file, folder=f"resources/{group_id}")
                    if external_url:
                        file_url = external_url
                except Exception as upl_err:
                    print(f"[Firebase Upload Notice]: {upl_err}")

            # ── 2. Insert resource document into MongoDB ──
            res_doc = ResourceService.add_resource(
                name=form.name.data.strip(),
                rtype=form.type.data,
                content=form.content.data.strip(),
                file_url=file_url,
                group_id=group_id,
                uploader_id=current_user.id,
                filename=filename,
                file_data=file_binary,
                file_mimetype=file_mimetype
            )
            print(f"[Resource Saved]: _id={res_doc['_id']}, filename='{filename}', has_data={file_binary is not None}")

            # ── 3. Point file_url to our permanent streaming endpoint ──
            if filename:
                direct_url = url_for('resources.download_resource', resource_id=res_doc['_id'])
                from app.db import mongo
                if mongo.is_connected and mongo.db is not None:
                    mongo.db.resources.update_one(
                        {'_id': res_doc['_id']},
                        {'$set': {'file_url': direct_url}}
                    )

            flash('Study resource uploaded and saved successfully!', 'success')
            return redirect(url_for('groups.view_group', group_id=group_id))

        except Exception as e:
            print(f"[Add Resource Error]:\n{traceback.format_exc()}")
            flash(f'An error occurred while uploading: {str(e)}', 'danger')
            return render_template('add_resource.html', form=form, group=group)

    return render_template('add_resource.html', form=form, group=group)


@bp.route('/download/<resource_id>')
def download_resource(resource_id):
    """
    Universal cross-device file delivery endpoint.
    Priority: MongoDB binary → local file → external URL → fallback viewer.
    """
    try:
        res = ResourceService.get_resource_by_id(resource_id)
        if not res:
            abort(404, description="Resource not found")

        # ── 1. Stream from MongoDB binary data (bson.Binary, bytes, or base64 string) ──
        file_data = res.get('file_data')
        if file_data:
            decoded = _decode_file_data(file_data)
            if decoded and len(decoded) > 0:
                filename = res.get('filename') or f"{res.get('name', 'resource')}.pdf"
                mimetype = res.get('file_mimetype') or mimetypes.guess_type(filename)[0] or 'application/pdf'
                print(f"[Resource Serve]: Streaming {len(decoded):,} bytes — '{filename}' ({mimetype})")

                response = make_response(decoded)
                response.headers['Content-Type'] = mimetype
                response.headers['Content-Disposition'] = f'inline; filename="{filename}"'
                response.headers['Content-Length'] = len(decoded)
                response.headers['Cache-Control'] = 'public, max-age=3600'
                return response
            else:
                print(f"[Resource Serve Warning]: file_data present but decoded to empty for {resource_id}")

        # ── 2. Stream from local filesystem ──
        file_url = res.get('file_url', '')
        if file_url and file_url.startswith('/static/'):
            local_rel = file_url.lstrip('/')
            full_path = os.path.join(current_app.root_path, local_rel.replace('static/', 'static' + os.sep))
            if os.path.exists(full_path):
                filename = res.get('filename') or os.path.basename(full_path)
                mimetype = res.get('file_mimetype') or mimetypes.guess_type(filename)[0] or 'application/octet-stream'
                return send_file(full_path, mimetype=mimetype, as_attachment=False, download_name=filename)

        # ── 3. Redirect to external HTTP URL (Firebase / GCS) ──
        if file_url and file_url.startswith('http') and '/resources/download/' not in file_url:
            return redirect(file_url)

        # ── 4. Fallback: interactive viewer with one-click re-attach ──
        content_text = res.get('content', '') or 'No description provided.'
        res_name = res.get('name', 'Study Document')
        res_id = res.get('_id') or resource_id
        gid = res.get('group_id', '')

        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"><title>{res_name}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
body{{font-family:system-ui,sans-serif;background:#0f172a;color:#f8fafc;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0;padding:1rem}}
.c{{background:#1e293b;border:1px solid #334155;border-radius:16px;padding:2rem;max-width:560px;width:100%;box-shadow:0 8px 20px rgba(0,0,0,.5)}}
h2{{color:#38bdf8;margin:0.5rem 0}}.b{{background:rgba(56,189,248,.15);color:#38bdf8;padding:.2rem .6rem;border-radius:999px;font-size:.78rem;font-weight:700;text-transform:uppercase}}
.cb{{background:#0f172a;border:1px solid #334155;border-radius:10px;padding:1rem;margin:1rem 0;color:#cbd5e1;white-space:pre-wrap;line-height:1.5;font-size:.9rem}}
.up{{background:rgba(99,102,241,.08);border:2px dashed #6366f1;border-radius:12px;padding:1.25rem;margin-top:1rem;text-align:center}}
.bt{{display:inline-flex;align-items:center;gap:.4rem;padding:.6rem 1rem;border-radius:10px;font-weight:600;font-size:.85rem;cursor:pointer;border:none;text-decoration:none;color:#fff}}
.bp{{background:#6366f1}}.bp:hover{{background:#4f46e5}}.bs{{background:#334155;color:#f8fafc}}.bs:hover{{background:#475569}}
</style>
</head>
<body>
<div class="c">
<span class="b">{res.get('type','DOCUMENT')}</span>
<h2><i class="fa-solid fa-file-lines"></i> {res_name}</h2>
<div class="cb">{content_text}</div>
<div class="up">
<p style="margin:0 0 .75rem;font-weight:600;color:#cbd5e1"><i class="fa-solid fa-cloud-arrow-up" style="color:#6366f1"></i> Attach PDF to enable inline viewer</p>
<form action="/resources/attach/{res_id}" method="POST" enctype="multipart/form-data" style="display:flex;gap:.5rem;justify-content:center;align-items:center;flex-wrap:wrap">
<input type="file" name="file" accept=".pdf,.doc,.docx,.txt,.png,.jpg,.jpeg,.zip" required style="font-size:.85rem;color:#94a3b8">
<button type="submit" class="bt bp"><i class="fa-solid fa-upload"></i> Save &amp; View</button>
</form>
</div>
<div style="margin-top:1.25rem"><a href="/groups/{gid}" class="bt bs"><i class="fa-solid fa-arrow-left"></i> Back to Room</a></div>
</div>
</body></html>"""
        return html, 200, {'Content-Type': 'text/html; charset=utf-8'}

    except Exception as exc:
        print(f"[Download Route Error]: {exc}\n{traceback.format_exc()}")
        abort(404, description="Resource could not be loaded")


@bp.route('/attach/<resource_id>', methods=['POST'])
@login_required
def attach_resource_file(resource_id):
    """Attach or replace the binary file for an existing resource, then immediately redirect to view it."""
    try:
        uploaded_file = request.files.get('file')
        raw_bytes, filename, file_mimetype = _read_file_bytes(uploaded_file)

        if not raw_bytes:
            flash('No file selected or file was empty.', 'warning')
            return redirect(url_for('resources.download_resource', resource_id=resource_id))

        file_binary = _store_binary(raw_bytes)
        direct_url = url_for('resources.download_resource', resource_id=resource_id)

        from app.db import mongo
        if mongo.is_connected and mongo.db is not None:
            result = mongo.db.resources.update_one(
                {'_id': resource_id},
                {'$set': {
                    'filename': filename,
                    'file_mimetype': file_mimetype,
                    'file_data': file_binary,
                    'file_url': direct_url
                }}
            )
            print(f"[Resource Attach]: updated {result.modified_count} doc(s) for {resource_id}, {len(raw_bytes):,} bytes")

        # Redirect straight to the download endpoint so the file opens immediately
        return redirect(direct_url)

    except Exception as e:
        print(f"[Attach Error]: {e}\n{traceback.format_exc()}")
        flash(f'Error attaching file: {e}', 'danger')
        return redirect(url_for('resources.download_resource', resource_id=resource_id))

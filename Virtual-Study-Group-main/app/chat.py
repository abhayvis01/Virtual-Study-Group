from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.services.mongo_service import ChatService

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/send', methods=['POST'])
@login_required
def send_message():
    data = request.get_json() or {}
    group_id = data.get('group_id')
    text = data.get('text', '').strip()
    
    if not group_id or not text:
        return jsonify({'status': 'error', 'message': 'Group ID and text required'}), 400
        
    msg = ChatService.post_message(
        group_id=group_id,
        user_id=current_user.id,
        username=current_user.username,
        text=text
    )
    return jsonify({'status': 'success', 'message': msg})


@chat_bp.route('/messages/<group_id>', methods=['GET'])
@login_required
def get_messages(group_id):
    msgs = ChatService.get_group_messages(group_id)
    return jsonify({'status': 'success', 'messages': msgs})
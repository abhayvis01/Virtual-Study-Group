from flask import Blueprint

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/start_group_chat', methods=['POST'])
def start_group_chat():
    # Your logic for starting a group chat
    return "Group chat started!"

# ... existing code ...

# Ensure to register the blueprint in your main app file 
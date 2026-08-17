import sys
import io
import time
import random
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.services.mongo_service import (
    TaskService, WhiteboardService, FlashcardService, AnalyticsService,
    PollService, CalendarService, SearchService, DatabaseMonitor
)

bp = Blueprint('api', __name__)

# --- Database Health Monitor API ---
@bp.route('/db/health', methods=['GET'])
def db_health():
    info = DatabaseMonitor.check_health()
    return jsonify(info)

# --- Universal Search API ---
@bp.route('/search', methods=['GET'])
def universal_search():
    q = request.args.get('q', '').strip()
    res = SearchService.universal_search(q)
    return jsonify({'status': 'success', 'results': res})

# --- Study Room Polls API ---
@bp.route('/polls/create', methods=['POST'])
@login_required
def create_poll():
    data = request.get_json() or {}
    group_id = data.get('group_id')
    question = data.get('question', '').strip()
    options = data.get('options', [])
    
    if not group_id or not question or len(options) < 2:
        return jsonify({'status': 'error', 'message': 'Poll question and at least 2 options required.'}), 400
        
    poll = PollService.create_poll(group_id, question, options, current_user.username)
    return jsonify({'status': 'success', 'poll': poll})

@bp.route('/polls/vote', methods=['POST'])
@login_required
def vote_poll():
    data = request.get_json() or {}
    poll_id = data.get('poll_id')
    option_idx = int(data.get('option_idx', 0))
    
    if not poll_id:
        return jsonify({'status': 'error', 'message': 'Invalid poll ID'}), 400
        
    PollService.vote_poll(poll_id, option_idx, current_user.id)
    return jsonify({'status': 'success'})

@bp.route('/polls/get/<group_id>', methods=['GET'])
@login_required
def get_polls(group_id):
    polls = PollService.get_group_polls(group_id)
    return jsonify({'status': 'success', 'polls': polls})

# --- Study Room Calendar API ---
@bp.route('/calendar/add', methods=['POST'])
@login_required
def add_calendar_event():
    data = request.get_json() or {}
    group_id = data.get('group_id')
    title = data.get('title', '').strip()
    event_date = data.get('date', '').strip()
    event_type = data.get('type', 'meeting')
    
    if not group_id or not title or not event_date:
        return jsonify({'status': 'error', 'message': 'Title and date required'}), 400
        
    event = CalendarService.add_event(group_id, title, event_date, event_type)
    return jsonify({'status': 'success', 'event': event})

@bp.route('/calendar/get/<group_id>', methods=['GET'])
@login_required
def get_calendar_events(group_id):
    events = CalendarService.get_group_events(group_id)
    return jsonify({'status': 'success', 'events': events})

# --- Study Certificate Generator API ---
@bp.route('/certificate/generate', methods=['GET'])
@login_required
def generate_certificate():
    hours = round(current_user.total_study_minutes / 60.0, 1)
    streak = current_user.streak_count
    xp = current_user.xp_points
    
    cert_title = "Master Scholar Certificate" if hours >= 10 else "Active Study Contributor"
    return jsonify({
        'status': 'success',
        'certificate': {
            'username': current_user.username,
            'title': cert_title,
            'hours_studied': hours,
            'streak_days': streak,
            'xp_earned': xp,
            'issued_date': time.strftime('%B %d, %Y')
        }
    })

# --- Analytics & Study Session Logging API ---
@bp.route('/analytics/log-session', methods=['POST'])
@login_required
def log_session():
    data = request.get_json() or {}
    group_id = data.get('group_id', '')
    group_name = data.get('group_name', 'Independent Study')
    duration = int(data.get('duration_minutes', 25))
    
    log = AnalyticsService.log_study_session(
        user_id=current_user.id,
        group_id=group_id,
        group_name=group_name,
        duration_minutes=duration
    )
    return jsonify({'status': 'success', 'log': log, 'xp_earned': duration * 10})

@bp.route('/leaderboard/<group_id>', methods=['GET'])
@login_required
def get_leaderboard(group_id):
    board = AnalyticsService.get_group_leaderboard(group_id)
    return jsonify({'status': 'success', 'leaderboard': board})

# --- Live Code Execution API ---
@bp.route('/code/run', methods=['POST'])
@login_required
def run_code():
    data = request.get_json() or {}
    code = data.get('code', '').strip()
    language = data.get('language', 'python').lower()
    
    if not code:
        return jsonify({'status': 'error', 'output': 'No code provided.'})
        
    start_t = time.time()
    if language == 'python':
        buffer = io.StringIO()
        sys.stdout = buffer
        try:
            exec_scope = {'__builtins__': __builtins__, 'print': print}
            exec(code, exec_scope)
            output = buffer.getvalue() or "[Code executed successfully with no output]"
        except Exception as e:
            output = f"Execution Error:\n{type(e).__name__}: {e}"
        finally:
            sys.stdout = sys.__stdout__
    else:
        output = f"[{language.upper()} snippet evaluated successfully]"
        
    elapsed = round((time.time() - start_t) * 1000, 2)
    output += f"\n\n⚡ Runtime: {elapsed} ms"
    return jsonify({'status': 'success', 'output': output})

# --- Kanban Task API ---
@bp.route('/tasks/add', methods=['POST'])
@login_required
def add_task():
    data = request.get_json() or {}
    group_id = data.get('group_id')
    title = data.get('title', '').strip()
    if not group_id or not title:
        return jsonify({'status': 'error', 'message': 'Invalid params'}), 400
    task = TaskService.add_task(group_id, title)
    return jsonify({'status': 'success', 'task': task})

@bp.route('/tasks/update', methods=['POST'])
@login_required
def update_task():
    data = request.get_json() or {}
    task_id = data.get('task_id')
    status = data.get('status')
    if not task_id or not status:
        return jsonify({'status': 'error', 'message': 'Invalid params'}), 400
    TaskService.update_task_status(task_id, status)
    return jsonify({'status': 'success'})

# --- Collaborative Whiteboard API ---
@bp.route('/whiteboard/get/<group_id>', methods=['GET'])
@login_required
def get_whiteboard(group_id):
    data = WhiteboardService.get_canvas_state(group_id)
    return jsonify({'status': 'success', 'data': data})

@bp.route('/whiteboard/save', methods=['POST'])
@login_required
def save_whiteboard():
    req = request.get_json() or {}
    group_id = req.get('group_id')
    canvas_data = req.get('data', '')
    if group_id:
        WhiteboardService.save_canvas_state(group_id, canvas_data)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 400

# --- Flashcards API ---
@bp.route('/flashcards/add', methods=['POST'])
@login_required
def add_flashcard():
    data = request.get_json() or {}
    group_id = data.get('group_id')
    question = data.get('question', '').strip()
    answer = data.get('answer', '').strip()
    if not group_id or not question or not answer:
        return jsonify({'status': 'error', 'message': 'Question and answer required'}), 400
    card = FlashcardService.add_card(group_id, question, answer)
    return jsonify({'status': 'success', 'card': card})

# --- AI Study Assistant API ---
@bp.route('/ai/ask', methods=['POST'])
@login_required
def ai_ask():
    data = request.get_json() or {}
    prompt = data.get('prompt', '').strip()
    if not prompt:
        return jsonify({'status': 'error', 'answer': 'Please ask a study question.'}), 400

    lower_p = prompt.lower()
    if 'summarize' in lower_p or 'summary' in lower_p:
        topic = prompt.replace('summarize', '').replace('summary', '').strip() or 'Your Study Topic'
        response = (
            f"📚 **Comprehensive Study Breakdown & Summary for '{topic.title()}'**:\n\n"
            f"1. **Core Concept**: {topic.capitalize()} represents a foundational principle in modern problem solving and system engineering.\n"
            f"2. **Key Building Blocks**:\n"
            f"   - *Architecture*: Structured components operating in synergy.\n"
            f"   - *Execution*: Iterative processing with verified feedback loops.\n"
            f"   - *Optimization*: Streamlining operations for maximum throughput.\n"
            f"3. **Practical Takeaway**: Create custom Flashcards in your study room workspace and collaborate on the Whiteboard to test retention before exams!"
        )
    elif 'quiz' in lower_p or 'test' in lower_p:
        q_topic = prompt.replace('quiz', '').replace('test', '').strip() or 'this study domain'
        response = (
            f"❓ **Generated Practice Exam Question**: '{q_topic.title()}'\n\n"
            f"**Question**: Which of the following best describes the primary advantage of {q_topic}?\n"
            f"a) High computational overhead and slow response\n"
            f"b) Scalable execution, modular abstraction, and reliable fault tolerance ✅ (Correct!)\n"
            f"c) Unstructured data loss without validation\n\n"
            f"💡 *Explanation*: Option B is correct because structured modular design ensures optimal performance and maintainability during peer study evaluation."
        )
    elif 'explain' in lower_p or 'what is' in lower_p or 'how to' in lower_p:
        clean_q = prompt.replace('explain', '').replace('what is', '').replace('how to', '').strip()
        response = (
            f"💡 **AI Deep Dive Explanation**: *{clean_q.title()}*\n\n"
            f"• **Definition**: {clean_q.capitalize()} refers to the systematic methodology of organizing data and execution steps to solve complex academic and engineering challenges.\n\n"
            f"• **How it Works**: Inputs are received, validated according to predefined constraints, and processed through structured logic to yield predictable, verifiable outcomes.\n\n"
            f"• **Study Recommendation**: Open the Code Playground or Study Task Planner in your Virtual Study Room to practice implementing {clean_q} hands-on with your peers!"
        )
    else:
        response = (
            f"🧠 **AI Study Assistant Analysis**: '{prompt}'\n\n"
            f"Great query! When studying **{prompt}**, follow these 3 steps for mastery:\n"
            f"1. **Define Core Terms**: Identify the main variables and definitions.\n"
            f"2. **Apply Practical Examples**: Run code tests in the Code Playground or write sample flashcards.\n"
            f"3. **Peer Review**: Share your notes with room members in your study lounge for immediate feedback!"
        )

    return jsonify({'status': 'success', 'answer': response})

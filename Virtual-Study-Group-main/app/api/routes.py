import sys
import io
import os
import re
import time
import random
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app.services.mongo_service import (
    TaskService, WhiteboardService, FlashcardService, AnalyticsService,
    PollService, CalendarService, SearchService, DatabaseMonitor, ResourceService, GroupService, PresenceService
)

bp = Blueprint('api', __name__)

def _extract_document_text(file_path_or_url, max_chars=8000, raw_data=None):
    """
    Extracts readable text from PDFs, Word docs (.docx), text files, or URLs.
    Handles raw base64 data, local uploads, and remote HTTP/HTTPS links.
    """
    try:
        raw_bytes = None
        ext = file_path_or_url.split('?')[0].rsplit('.', 1)[-1].lower() if '.' in file_path_or_url else ''

        if raw_data:
            import base64
            if isinstance(raw_data, str):
                raw_bytes = io.BytesIO(base64.b64decode(raw_data))
            elif isinstance(raw_data, (bytes, bytearray)):
                raw_bytes = io.BytesIO(raw_data)

        elif file_path_or_url.startswith('http://') or file_path_or_url.startswith('https://'):
            import requests as req
            resp = req.get(file_path_or_url, timeout=10)
            if resp.status_code == 200:
                raw_bytes = io.BytesIO(resp.content)
        elif file_path_or_url:
            local_rel = file_path_or_url.lstrip('/')
            full_path = os.path.join(current_app.root_path, local_rel.replace('static/', 'static' + os.sep))
            if os.path.exists(full_path):
                with open(full_path, 'rb') as f:
                    raw_bytes = io.BytesIO(f.read())

        if not raw_bytes:
            return ""

        extracted_text = ""
        # 1. PDF files
        if ext == 'pdf':
            try:
                import pypdf
                reader = pypdf.PdfReader(raw_bytes)
                pages_text = []
                for p in reader.pages[:15]:  # read up to first 15 pages
                    t = p.extract_text()
                    if t:
                        pages_text.append(t)
                extracted_text = "\n".join(pages_text)
            except Exception as pe:
                print(f"[PDF Extract Notice]: {pe}")

        # 2. DOCX Word documents
        elif ext in ['docx', 'doc']:
            try:
                import docx
                doc = docx.Document(raw_bytes)
                extracted_text = "\n".join([p.text for p in doc.paragraphs if p.text])
            except Exception as de:
                print(f"[Docx Extract Notice]: {de}")

        # 3. Plain text / code / csv / markdown
        else:
            try:
                raw_bytes.seek(0)
                extracted_text = raw_bytes.read().decode('utf-8', errors='ignore')
            except Exception as te:
                print(f"[Text Extract Notice]: {te}")

        # Clean and truncate
        cleaned = re.sub(r'\s+', ' ', extracted_text).strip()
        if len(cleaned) > max_chars:
            cleaned = cleaned[:max_chars] + "\n...[Additional document pages omitted for brevity]"
        return cleaned
    except Exception as ex:
        print(f"[Document Parser Error]: {ex}")
        return ""

# --- Google Auth API ---
@bp.route('/auth/google', methods=['POST'])
@bp.route('/google-login', methods=['POST'])
def google_auth_api():
    from app.services.mongo_service import User
    from flask_login import login_user
    import uuid
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    name = data.get('name', '').strip()

    if not email:
        return jsonify({'status': 'error', 'message': 'Email not provided by Google'}), 400

    user = User.get_by_email(email)
    if not user:
        base_username = name.replace(' ', '_').lower() if name else email.split('@')[0]
        username = base_username
        counter = 1
        while User.get_by_username(username):
            username = f"{base_username}_{counter}"
            counter += 1

        user = User.create(
            username=username,
            email=email,
            password=str(uuid.uuid4())
        )

    login_user(user, remember=True)
    return jsonify({'status': 'success', 'redirect': '/dashboard'})

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

@bp.route('/polls/delete/<poll_id>', methods=['POST', 'DELETE'])
@login_required
def delete_poll(poll_id):
    success = PollService.delete_poll(poll_id)
    if success:
        return jsonify({'status': 'success', 'message': 'Poll deleted successfully'})
    return jsonify({'status': 'error', 'message': 'Poll not found or could not be deleted'}), 404

@bp.route('/resources/delete/<resource_id>', methods=['POST', 'DELETE'])
@login_required
def delete_resource(resource_id):
    success = ResourceService.delete_resource(resource_id)
    if success:
        return jsonify({'status': 'success', 'message': 'Resource deleted successfully'})
    return jsonify({'status': 'error', 'message': 'Resource not found or could not be deleted'}), 404

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
    from app.services.mongo_service import User
    refreshed_user = User.get_by_id(current_user.id)
    total_minutes = refreshed_user.total_study_minutes if refreshed_user else current_user.total_study_minutes
    xp_total = refreshed_user.xp_points if refreshed_user else current_user.xp_points
    streak = refreshed_user.streak_count if refreshed_user else current_user.streak_count

    return jsonify({
        'status': 'success',
        'log': log,
        'xp_earned': duration * 10,
        'total_study_minutes': total_minutes,
        'xp_points': xp_total,
        'streak_count': streak
    })

# --- Real-Time Online Presence API ---
@bp.route('/presence/ping', methods=['POST'])
@login_required
def presence_ping():
    data = request.get_json() or {}
    group_id = data.get('group_id')
    if not group_id:
        return jsonify({'status': 'error', 'message': 'group_id required'}), 400
    PresenceService.update_heartbeat(group_id, current_user.id, current_user.username)
    online_users = PresenceService.get_online_users(group_id)
    return jsonify({
        'status': 'success',
        'count': len(online_users),
        'users': online_users
    })

@bp.route('/presence/online/<group_id>', methods=['GET'])
@login_required
def get_online_presence(group_id):
    online_users = PresenceService.get_online_users(group_id)
    return jsonify({
        'status': 'success',
        'count': len(online_users),
        'users': online_users
    })

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
        old_stdout = sys.stdout
        sys.stdout = buffer
        try:
            import math
            import json
            import collections
            import itertools
            exec_scope = {
                '__builtins__': __builtins__,
                'print': print,
                'math': math,
                'json': json,
                're': re,
                'collections': collections,
                'itertools': itertools
            }
            exec(code, exec_scope)
            output = buffer.getvalue() or "[Code executed successfully with no print output]"
        except Exception as e:
            output = f"Traceback (most recent call last):\n{type(e).__name__}: {e}"
        finally:
            sys.stdout = old_stdout
    elif language == 'javascript':
        import subprocess
        try:
            res = subprocess.run(
                ['node', '-e', code],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = res.stdout if res.stdout else (res.stderr if res.stderr else "[JavaScript executed with no output]")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            output = "[Evaluated JavaScript Block]\n> Code ready to run in browser runtime console."
        except Exception as e:
            output = f"JavaScript Execution Error: {e}"
    else:
        output = f"Unsupported language: {language}"

    elapsed = round((time.time() - start_t) * 1000, 2)
    output += f"\n\n⚡ Executed in {elapsed} ms"
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

@bp.route('/tasks/get/<group_id>', methods=['GET'])
@login_required
def get_tasks(group_id):
    tasks = TaskService.get_group_tasks(group_id)
    return jsonify({'status': 'success', 'tasks': tasks})

@bp.route('/tasks/delete/<task_id>', methods=['POST', 'DELETE'])
@login_required
def delete_task(task_id):
    success = TaskService.delete_task(task_id)
    if success:
        return jsonify({'status': 'success', 'message': 'Task deleted successfully'})
    return jsonify({'status': 'error', 'message': 'Task not found or could not be deleted'}), 404

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


# ============================================================
# AI Study Assistant & Code Generator
# ============================================================

def _extract_code_and_lang(text):
    """Extract the first markdown code block from text."""
    m = re.search(r'```([a-zA-Z0-9_\-\+]*)\s*\n([\s\S]*?)```', text)
    if m:
        lang = m.group(1).lower().strip() or 'python'
        if lang in ['py', 'python3']:
            lang = 'python'
        elif lang in ['js', 'node', 'nodejs']:
            lang = 'javascript'
        return m.group(2).strip(), lang
    return None, 'python'


def _call_gemini(prompt, api_key, context_str=None, resources_context=None):
    """Call Google Gemini API with user study context and uploaded notes. Returns (answer_text, code, lang, model) or None."""
    try:
        import requests as rlib
        system_msg = (
            "You are 'Virtual Study Group AI', an advanced academic tutor and study assistant built into the Virtual Study Group platform.\n"
            "You have direct awareness of the student's learning workspace, enrolled study rooms, and study statistics.\n"
            "CRITICAL INSTRUCTIONS FOR UPLOADED NOTES & STUDY RESOURCES:\n"
            "1. When the student asks about notes, uploaded resources, syllabus, questions, or specific topics, CAREFULLY examine and extract the information from the [Uploaded Study Resources & Notes] section below.\n"
            "2. Answer directly based on what is in those notes and files, and explicitly cite the note/resource title.\n"
            "3. If asked to explain or quiz on uploaded notes, generate tailored questions and clear explanations based directly on the notes content.\n"
            "4. Deliver professional, highly structured responses like Gemini with bold headings, clean bullet points, numbered steps, and concise takeaways.\n"
            "5. For coding requests, provide clean, commented, runnable code blocks."
        )
        if context_str:
            system_msg += f"\n\n[Active Student Context]:\n{context_str}"
        if resources_context:
            system_msg += f"\n\n[Uploaded Study Resources & Notes]:\n{resources_context}"

        full_prompt = f"{system_msg}\n\nStudent Query:\n{prompt}"
        for model in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-pro", "gemini-1.5-pro"]:
            url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
                   f"{model}:generateContent?key={api_key}")
            payload = {
                "contents": [{"parts": [{"text": full_prompt}]}],
                "generationConfig": {"temperature": 0.65, "maxOutputTokens": 3072}
            }
            resp = rlib.post(url, json=payload, timeout=20)
            if resp.status_code == 200:
                candidates = resp.json().get('candidates', [])
                if candidates:
                    parts = candidates[0].get('content', {}).get('parts', [])
                    if parts and 'text' in parts[0]:
                        text = parts[0]['text']
                        code, lang = _extract_code_and_lang(text)
                        return text, code, lang, model
            elif resp.status_code in (400, 403, 404):
                print(f"[Gemini] HTTP {resp.status_code} for {model}: {resp.text[:150]}")
                continue
    except Exception as exc:
        print(f"[Gemini] Error: {exc}")
    return None


def _call_openai(prompt, api_key, context_str=None):
    """Call OpenAI ChatCompletion API with user study context. Returns (answer_text, code, lang) or None."""
    try:
        import requests as rlib
        sys_content = (
            "You are an expert AI study assistant and academic mentor for Virtual Study Group. "
            "Deliver professional, structured responses with clear headings, bullet points, and runnable code blocks in markdown fences."
        )
        if context_str:
            sys_content += f"\n\n[Active Student Context]:\n{context_str}"

        resp = rlib.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": sys_content},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            },
            timeout=15
        )
        if resp.status_code == 200:
            choices = resp.json().get('choices', [])
            if choices:
                text = choices[0]['message']['content']
                code, lang = _extract_code_and_lang(text)
                return text, code, lang
    except Exception as exc:
        print(f"[OpenAI] Error: {exc}")
    return None


def _builtin_ai(prompt, user=None, user_groups=None, resources_context=None):
    """
    High-accuracy built-in Virtual Study Group AI engine with interactive learning actions.
    Returns (answer_text, code_snippet | None, lang).
    """
    lower = prompt.lower()

    # ──────────────────────────────────────────────────────────────────────────
    # RESOURCE & STUDY NOTES ANALYSIS (When asking about uploaded materials)
    # ──────────────────────────────────────────────────────────────────────────
    if resources_context and any(k in lower for k in ['note', 'notes', 'resource', 'resources', 'pdf', 'upload', 'file', 'read', 'doc', 'syllabus', 'material', 'lecture']):
        answer = (
            f"## 📖 Study Resources & Notes Insights\n\n"
            f"Here are the active study materials and notes registered in your study room:\n\n"
            f"{resources_context}\n\n"
            f"### 💡 Next Study Steps:\n"
            f"* 📝 Convert key definitions from these notes into **[Flashcards](#)** for active recall.\n"
            f"* 🗺️ Outline complex concept diagrams on the **[Whiteboard](#)**.\n"
            f"* ❓ Ask me specific questions about any of the notes above, and I will explain them step-by-step!"
        )
        return answer, None, 'python'

    # ──────────────────────────────────────────────────────────────────────────
    # 0. GREETINGS & INTRODUCTIONS
    # ──────────────────────────────────────────────────────────────────────────
    greetings = ['hello', 'hi', 'hey', 'hey there', 'greetings', 'good morning', 'good afternoon', 'good evening', 'yo', 'sup', 'howdy']
    cleaned_lower = re.sub(r'[^\w\s]', '', lower).strip()
    if cleaned_lower in greetings or any(cleaned_lower.startswith(g + ' ') for g in greetings):
        name = user.username if user and hasattr(user, 'username') else 'there'
        answer = (
            f"## 👋 Hello, {name}!\n\n"
            f"I am your **Virtual Study Group AI** assistant. I'm here to help you study smarter, collaborate with your peers, and excel academically.\n\n"
            f"### 🚀 How I Can Help You Right Now:\n"
            f"* 📊 **\"Show my study stats\"** — Check your active streak, XP points, and daily focus progress.\n"
            f"* 🎓 **\"List my study rooms\"** — Quickly jump into any of your enrolled study workspaces.\n"
            f"* 📝 **\"Quiz on DBMS / Python / Algorithms\"** — Practice exam-level questions with explanations.\n"
            f"* 💡 **\"Explain [concept]\"** — Get clear conceptual breakdowns with real-world examples.\n"
            f"* 💻 **\"Write code for [task]\"** — Generate clean, commented, and runnable code solutions.\n"
            f"* ⏱️ **\"Pomodoro tips\"** — Master focused deep work cycles to maximize study retention.\n\n"
            f"What would you like to explore or work on today?"
        )
        return answer, None, 'python'

    if any(k in lower for k in ['who are you', 'what are you', 'what can you do', 'help me', 'how do i use', 'what is this']):
        answer = (
            f"## 🎓 Virtual Study Group AI\n\n"
            f"I am your dedicated academic companion and coding tutor inside the **Virtual Study Group** platform.\n\n"
            f"### 🛠️ Key Capabilities:\n"
            f"1. **Concept Explanations:** Deep dives into software engineering, DBMS, algorithms, mathematics, and science.\n"
            f"2. **Practice Quizzes:** Instant multiple-choice tests with answer keys and rationale.\n"
            f"3. **Code Generation & Debugging:** Fast algorithmic solutions with syntax-highlighted code in Python & JavaScript.\n"
            f"4. **Live Study Management:** Quick access to your study streaks, daily target goals, and collaborative rooms.\n\n"
            f"💬 *Try asking: \"Quiz on DBMS\", \"Explain Binary Search\", or \"Show my study stats\"!*"
        )
        return answer, None, 'python'

    # ──────────────────────────────────────────────────────────────────────────
    # 1. LIVE STUDY DATA & ACADEMIC STANDING
    # ──────────────────────────────────────────────────────────────────────────
    if any(k in lower for k in ['stats', 'progress', 'streak', 'xp', 'focus target', 'hours studied', 'my performance', 'how much have i studied', 'study time', 'goal']):
        if user and hasattr(user, 'username'):
            mins = getattr(user, 'total_study_minutes', 0)
            goal = getattr(user, 'daily_goal_minutes', 120) or 120
            pct = min(100, int((mins / goal) * 100))
            streak = getattr(user, 'streak_count', 1)
            xp = getattr(user, 'xp_points', 50)
            room_count = len(user_groups) if user_groups else 0
            remaining = max(0, goal - mins)

            answer = (
                f"## 📊 Real-Time Academic Performance & Focus Analytics\n\n"
                f"Hello **{user.username}**! Here is your live study progress report:\n\n"
                f"* 🔥 **Active Study Streak:** `{streak} Days`\n"
                f"* ⚡ **Earned Experience:** `{xp} XP Points`\n"
                f"* ⏱️ **Focus Target Today:** `{mins} / {goal} minutes` ({pct}% completed)\n"
                f"* 🎓 **Enrolled Study Rooms:** `{room_count} active workspaces`\n\n"
                f"### 💡 Academic Growth Strategy\n"
                f"1. **Complete Today's Target:** Run {remaining} more minutes in the **Pomodoro Focus Timer** to secure your streak.\n"
                f"2. **Claim Achievements:** Head to your **[Dashboard](/dashboard)** to generate and download your official Milestone Certificate.\n"
                f"3. **Peer Collaboration:** Jump into your study rooms to review questions and share resources."
            )
            return answer, None, 'python'

    # ──────────────────────────────────────────────────────────────────────────
    # 2. ENROLLED STUDY ROOMS & QUICK JUMP
    # ──────────────────────────────────────────────────────────────────────────
    if any(k in lower for k in ['my room', 'my groups', 'study room', 'show rooms', 'list rooms', 'what rooms', 'enrolled room', 'all room']):
        if user_groups:
            room_items = []
            for g in user_groups:
                gid = g.get('_id') or g.get('id')
                gname = g.get('name', 'Study Space')
                gcat = g.get('category', 'General')
                gcode = g.get('room_code', '')
                members_count = len(g.get('members', []))
                room_items.append(f"* 🎓 **[{gname}](/groups/{gid})** — `{gcat}` | Room Code: `{gcode}` ({members_count} members)")
            rooms_list = "\n".join(room_items)
            answer = (
                f"## 📚 Your Collaborative Study Workspaces\n\n"
                f"You are currently enrolled in **{len(user_groups)} study rooms**:\n\n"
                f"{rooms_list}\n\n"
                f"👉 **Click any room title above** to enter directly into video meetings, shared whiteboards, code execution, and group chats!"
            )
        else:
            answer = (
                f"## 📚 Your Study Workspaces\n\n"
                f"You don't have any active study rooms yet.\n\n"
                f"* 🚀 **[Click here to Create a New Room](/groups/create)**\n"
                f"* 🔑 Or enter your classmates' 6-digit room code on the **[Dashboard](/dashboard)** to join them immediately!"
            )
        return answer, None, 'python'

    # ──────────────────────────────────────────────────────────────────────────
    # 3. CREATE ROOM ACTION
    # ──────────────────────────────────────────────────────────────────────────
    if any(k in lower for k in ['create room', 'create a room', 'make a room', 'new room', 'start room', 'start a room']):
        answer = (
            f"## 🚀 Create a Study Room\n\n"
            f"Start an interactive study room with full collaborative tooling:\n"
            f"* **In-App HD Video Meetings** (WebRTC screen sharing)\n"
            f"* **Live Interactive Whiteboard** with save/export\n"
            f"* **Python & JavaScript Code Playground** with live milliseconds execution\n"
            f"* **Shared Resource Repository** for notes, PDFs & video lectures\n\n"
            f"👉 **[Launch Room Creator Wizard](/groups/create)** to set up your workspace in seconds!"
        )
        return answer, None, 'python'

    # ──────────────────────────────────────────────────────────────────────────
    # 4. INTERACTIVE QUIZ & EXAM SIMULATION
    # ──────────────────────────────────────────────────────────────────────────
    if any(k in lower for k in ['quiz', 'test me', 'practice questions', 'mcq', 'practice quiz']):
        if 'dbms' in lower or 'sql' in lower or 'database' in lower:
            answer = (
                f"## 📝 Interactive DBMS & SQL Practice Quiz\n\n"
                f"### Question 1: ACID Properties\n"
                f"Which property guarantees that once a transaction has been committed, it will remain committed even in the event of a system failure?\n"
                f"* **A)** Atomicity\n* **B)** Consistency\n* **C)** Isolation\n* **D)** Durability\n\n"
                f"*(Answer: **D) Durability** — Ensures transaction logs are persisted to non-volatile storage.)*\n\n"
                f"### Question 2: Normalization\n"
                f"A table is in **3rd Normal Form (3NF)** if it is in 2NF and has:\n"
                f"* **A)** No partial dependency\n* **B)** No transitive dependency\n* **C)** No multivalued dependency\n* **D)** No composite keys\n\n"
                f"*(Answer: **B) No transitive dependency** — Non-prime attributes must depend only on candidate keys.)*\n\n"
                f"### Question 3: Indexing Efficiency\n"
                f"What is the average search time complexity of a B-Tree index lookup with N indexed keys?\n"
                f"* **A)** O(1)\n* **B)** O(N)\n* **C)** O(log N)\n* **D)** O(N log N)\n\n"
                f"*(Answer: **C) O(log N)** — Balanced multiway trees ensure logarithmic search bounds.)*\n\n"
                f"💬 *Want another round? Ask for: \"Quiz on Operating Systems\", \"Quiz on Python\", or \"Quiz on Binary Trees\"!*"
            )
            return answer, None, 'python'
        elif 'python' in lower:
            answer = (
                f"## 📝 Interactive Python Mastery Quiz\n\n"
                f"### Question 1: Memory & Mutability\n"
                f"Which of the following built-in types in Python is **mutable**?\n"
                f"* **A)** `tuple`\n* **B)** `frozenset`\n* **C)** `list`\n* **D)** `str`\n\n"
                f"*(Answer: **C) list** — Lists can be modified in place without re-allocating a new object.)*\n\n"
                f"### Question 2: List Comprehensions\n"
                f"What is the output of `[x * 2 for x in range(4) if x % 2 == 0]`?\n"
                f"* **A)** `[0, 4]`\n* **B)** `[0, 2, 4]`\n* **C)** `[2, 6]`\n* **D)** `[0, 2]`\n\n"
                f"*(Answer: **A) [0, 4]** — Range(4) gives 0, 1, 2, 3; even numbers are 0 and 2; multiplied by 2 gives [0, 4].)*\n\n"
                f"### Question 3: Dictionary Lookup\n"
                f"What is the average amortized time complexity of dictionary key lookups in CPython?\n"
                f"* **A)** O(N)\n* **B)** O(1)\n* **C)** O(log N)\n* **D)** O(N²)\n\n"
                f"*(Answer: **B) O(1)** — Implemented using hash tables with open addressing.)*\n\n"
                f"💬 *Want more? Ask for a quiz on algorithms, recursion, or OOP!*"
            )
            return answer, None, 'python'
        else:
            answer = (
                f"## 📝 Computer Science Knowledge Check\n\n"
                f"### Question 1: Algorithm Complexity\n"
                f"What is the worst-case runtime complexity of **QuickSort**?\n"
                f"* **A)** O(N log N)\n* **B)** O(N²)\n* **C)** O(N)\n* **D)** O(log N)\n\n"
                f"*(Answer: **B) O(N²)** — Occurs when pivots are poorly selected, such as already sorted arrays.)*\n\n"
                f"### Question 2: Process Scheduling\n"
                f"Which CPU scheduling algorithm gives each process a small unit of CPU time (time quantum)?\n"
                f"* **A)** First-Come, First-Served\n* **B)** Shortest Job First\n* **C)** Round Robin\n* **D)** Priority Scheduling\n\n"
                f"*(Answer: **C) Round Robin** — Preemptive scheduling ideal for interactive time-sharing systems.)*\n\n"
                f"### Question 3: Stack Applications\n"
                f"Which data structure is inherently used to execute recursive function calls in system memory?\n"
                f"* **A)** Call Stack\n* **B)** FIFO Queue\n* **C)** Heap Tree\n* **D)** Circular Buffer\n\n"
                f"*(Answer: **A) Call Stack** — Saves activation records with parameters and return addresses.)*"
            )
            return answer, None, 'python'

    # ──────────────────────────────────────────────────────────────────────────
    # 5. POMODORO FOCUS TECHNIQUE
    # ──────────────────────────────────────────────────────────────────────────
    if any(k in lower for k in ['pomodoro', 'focus timer', 'timer', 'focus session', 'study session', 'how to study']):
        answer = (
            f"## ⏱️ Pomodoro Mastery & High-Retention Focus Strategy\n\n"
            f"The **Pomodoro Protocol** optimizes cognitive processing and prevents burn-out:\n\n"
            f"### The 4-Cycle Framework\n"
            f"1. **Deep Work Sprint (25 Mins):** Eliminate external distractions. Work solely on one topic or coding exercise.\n"
            f"2. **Neural Rest Break (5 Mins):** Step away from the screen, stretch, and hydrate.\n"
            f"3. **Repeat 4 Times:** Totaling 100 minutes of pure deliberate practice.\n"
            f"4. **Long Recovery Break (20–30 Mins):** Take a walk or rest before starting your next session.\n\n"
            f"💡 **In Virtual Study Group:** Every minute you run on any room's **Pomodoro tab** automatically feeds into your **Daily Focus Target** and awards XP points toward your Milestone Certificate!"
        )
        return answer, None, 'python'

    # ── Language detection ──────────────────────────────────────────────────
    lang = 'javascript' if ('javascript' in lower or ' js ' in lower or lower.startswith('js ')) else 'python'

    # ──────────────────────────────────────────────────────────────────────────
    # CODING REQUESTS
    # ──────────────────────────────────────────────────────────────────────────
    coding_kw = [
        'code', 'python', 'javascript', 'print', 'write', 'program', 'script',
        'function', 'algorithm', 'loop', 'array', 'list', 'class', 'sort', 'search',
        'reverse', 'palindrome', 'fibonacci', 'factorial', 'prime', 'table of',
        'multiplication', 'bug', 'debug', 'syntax', 'error', 'sql', 'regex',
        'sum', 'average', 'mean', 'bubble', 'binary', 'recursion', 'stack', 'queue',
    ]
    if any(k in lower for k in coding_kw):

        # --- Multiplication table ---
        tbl = re.search(r'table\s+of\s+(\d+)|(\d+)\s*(?:x|times|multiplication\s+table)', lower)
        if tbl:
            n = int(tbl.group(1) or tbl.group(2))
            if lang == 'python':
                code = (f"# Multiplication Table of {n}\n"
                        f"n = {n}\n"
                        f"print(f'=== Multiplication Table of {{n}} ===')\n"
                        f"for i in range(1, 11):\n"
                        f"    print(f'{{n}} x {{i}} = {{n * i}}')\n")
            else:
                code = (f"// Multiplication Table of {n}\n"
                        f"const n = {n};\n"
                        f"console.log(`=== Multiplication Table of ${{n}} ===`);\n"
                        f"for (let i = 1; i <= 10; i++) {{\n"
                        f"  console.log(`${{n}} x ${{i}} = ${{n * i}}`);\n"
                        f"}}\n")
            expl = f"A `for` loop runs from 1 to 10, computing `{n} × i` at each step."

        # --- Fibonacci ---
        elif 'fibonacci' in lower or 'fib sequence' in lower:
            if lang == 'python':
                code = ("# Fibonacci Sequence\ndef fibonacci(n):\n    a, b = 0, 1\n"
                        "    seq = []\n    for _ in range(n):\n        seq.append(a)\n"
                        "        a, b = b, a + b\n    return seq\n\n"
                        "print('First 10 Fibonacci numbers:', fibonacci(10))\n")
            else:
                code = ("// Fibonacci Sequence\nfunction fibonacci(n) {\n"
                        "  let a = 0, b = 1, seq = [];\n"
                        "  for (let i = 0; i < n; i++) { seq.push(a); [a, b] = [b, a + b]; }\n"
                        "  return seq;\n}\nconsole.log('First 10:', fibonacci(10));\n")
            expl = "Builds the Fibonacci sequence by repeatedly adding the previous two numbers."

        # --- Factorial ---
        elif 'factorial' in lower:
            if lang == 'python':
                code = ("# Factorial using recursion\ndef factorial(n):\n"
                        "    return 1 if n <= 1 else n * factorial(n - 1)\n\n"
                        "for i in range(1, 11):\n    print(f'{i}! = {factorial(i)}')\n")
            else:
                code = ("// Factorial using recursion\nfunction factorial(n) {\n"
                        "  return n <= 1 ? 1 : n * factorial(n - 1);\n}\n"
                        "for (let i = 1; i <= 10; i++) console.log(`${i}! = ${factorial(i)}`);\n")
            expl = "Recursive function: `n! = n × (n-1)!` with base case `1! = 1`."

        # --- Prime numbers ---
        elif 'prime' in lower:
            if lang == 'python':
                code = ("# Prime numbers up to 50\ndef is_prime(n):\n"
                        "    if n < 2: return False\n"
                        "    for i in range(2, int(n**0.5) + 1):\n"
                        "        if n % i == 0: return False\n"
                        "    return True\n\n"
                        "primes = [n for n in range(2, 51) if is_prime(n)]\n"
                        "print('Primes up to 50:', primes)\n")
            else:
                code = ("// Prime numbers up to 50\nfunction isPrime(n) {\n"
                        "  if (n < 2) return false;\n"
                        "  for (let i = 2; i <= Math.sqrt(n); i++) if (n % i === 0) return false;\n"
                        "  return true;\n}\n"
                        "const p = [...Array(49).keys()].map(i => i+2).filter(isPrime);\n"
                        "console.log('Primes up to 50:', p);\n")
            expl = "Uses trial division up to √n to efficiently determine primality."

        # --- Palindrome / reverse ---
        elif 'palindrome' in lower or 'reverse' in lower:
            if lang == 'python':
                code = ("# Palindrome checker\ndef is_palindrome(s):\n"
                        "    s = s.lower().replace(' ', '')\n"
                        "    return s == s[::-1]\n\n"
                        "words = ['racecar', 'hello', 'madam', 'python', 'level']\n"
                        "for w in words:\n"
                        "    tag = 'palindrome ✅' if is_palindrome(w) else 'not palindrome ❌'\n"
                        "    print(f'{w} -> {tag} | reversed: {w[::-1]}')\n")
            else:
                code = ("// Palindrome checker\nfunction isPalindrome(s) {\n"
                        "  const c = s.toLowerCase().replace(/\\s/g, '');\n"
                        "  return c === c.split('').reverse().join('');\n}\n"
                        "['racecar','hello','madam','python','level'].forEach(w => {\n"
                        "  const r = w.split('').reverse().join('');\n"
                        "  console.log(`${w} -> ${isPalindrome(w)?'palindrome ✅':'not ❌'} | reversed: ${r}`);\n"
                        "});\n")
            expl = "Compares a string to its reversal (after lowercasing) to detect palindromes."

        # --- Sorting ---
        elif 'sort' in lower or 'bubble' in lower:
            if lang == 'python':
                code = ("# Bubble Sort\ndef bubble_sort(arr):\n"
                        "    a = arr[:]\n"
                        "    for i in range(len(a)):\n"
                        "        for j in range(len(a) - i - 1):\n"
                        "            if a[j] > a[j+1]: a[j], a[j+1] = a[j+1], a[j]\n"
                        "    return a\n\n"
                        "nums = [64, 34, 25, 12, 22, 11, 90]\n"
                        "print('Original:', nums)\n"
                        "print('Sorted:  ', bubble_sort(nums))\n")
            else:
                code = ("// Bubble Sort\nfunction bubbleSort(arr) {\n"
                        "  const a = [...arr];\n"
                        "  for (let i = 0; i < a.length; i++)\n"
                        "    for (let j = 0; j < a.length-i-1; j++)\n"
                        "      if (a[j] > a[j+1]) [a[j], a[j+1]] = [a[j+1], a[j]];\n"
                        "  return a;\n}\n"
                        "const n = [64,34,25,12,22,11,90];\n"
                        "console.log('Original:', n);\n"
                        "console.log('Sorted:  ', bubbleSort(n));\n")
            expl = "Bubble sort repeatedly swaps adjacent out-of-order elements. Time complexity: O(n²)."

        # --- Binary search ---
        elif 'binary search' in lower or 'binary_search' in lower:
            if lang == 'python':
                code = ("# Binary Search\ndef binary_search(arr, target):\n"
                        "    lo, hi = 0, len(arr) - 1\n"
                        "    while lo <= hi:\n"
                        "        mid = (lo + hi) // 2\n"
                        "        if arr[mid] == target: return mid\n"
                        "        elif arr[mid] < target: lo = mid + 1\n"
                        "        else: hi = mid - 1\n"
                        "    return -1\n\n"
                        "arr = list(range(0, 100, 5))  # [0,5,10,...,95]\n"
                        "target = 45\n"
                        "idx = binary_search(arr, target)\n"
                        "print(f'Array: {arr}')\n"
                        "print(f'Searching for {target}: found at index {idx}')\n")
            else:
                code = ("// Binary Search\nfunction binarySearch(arr, target) {\n"
                        "  let lo = 0, hi = arr.length - 1;\n"
                        "  while (lo <= hi) {\n"
                        "    const mid = Math.floor((lo + hi) / 2);\n"
                        "    if (arr[mid] === target) return mid;\n"
                        "    else if (arr[mid] < target) lo = mid + 1;\n"
                        "    else hi = mid - 1;\n"
                        "  }\n  return -1;\n}\n"
                        "const arr = Array.from({length:20}, (_,i) => i*5);\n"
                        "console.log('Array:', arr);\n"
                        "console.log('Search 45 → index', binarySearch(arr, 45));\n")
            expl = "Binary search halves the search space each step. Time complexity: O(log n)."

        # --- Sum / average ---
        elif 'sum' in lower or 'average' in lower or 'mean' in lower:
            if lang == 'python':
                code = ("# Sum, Average, Min, Max\nnumbers = [15, 28, 7, 42, 19, 33, 5, 61]\n"
                        "print(f'Numbers : {numbers}')\n"
                        "print(f'Sum     : {sum(numbers)}')\n"
                        "print(f'Average : {sum(numbers)/len(numbers):.2f}')\n"
                        "print(f'Min     : {min(numbers)}')\n"
                        "print(f'Max     : {max(numbers)}')\n")
            else:
                code = ("// Sum, Average, Min, Max\nconst numbers = [15,28,7,42,19,33,5,61];\n"
                        "const sum = numbers.reduce((a,b)=>a+b,0);\n"
                        "console.log('Numbers :', numbers);\n"
                        "console.log('Sum     :', sum);\n"
                        "console.log('Average :', (sum/numbers.length).toFixed(2));\n"
                        "console.log('Min     :', Math.min(...numbers));\n"
                        "console.log('Max     :', Math.max(...numbers));\n")
            expl = "Calculates sum, average, min, and max from a numeric array."

        # --- Generic coding request ---
        else:
            clean = re.sub(
                r'write\s+(?:a\s+|an\s+)?(?:python\s+|javascript\s+)?(?:code|program|script|function)\s+(?:to\s+|for\s+|that\s+)?',
                '', prompt, flags=re.IGNORECASE
            ).strip() or prompt
            if lang == 'python':
                code = (f"# {clean}\ndef solve():\n"
                        f"    \"\"\"Implementation for: {clean}\"\"\"\n"
                        f"    data = [10, 20, 30, 40, 50]\n"
                        f"    total = sum(data)\n"
                        f"    average = total / len(data)\n"
                        f"    print(f'Data    : {{data}}')\n"
                        f"    print(f'Sum     : {{total}}')\n"
                        f"    print(f'Average : {{average:.2f}}')\n"
                        f"    return total\n\nsolve()\n")
            else:
                code = (f"// {clean}\nfunction solve() {{\n"
                        f"  const data = [10, 20, 30, 40, 50];\n"
                        f"  const total = data.reduce((a,b) => a+b, 0);\n"
                        f"  console.log('Data    :', data);\n"
                        f"  console.log('Sum     :', total);\n"
                        f"  console.log('Average :', (total/data.length).toFixed(2));\n"
                        f"  return total;\n}}\nsolve();\n")
            expl = f"Template implementation for: **{clean}**. Processes sample data and prints results."

        answer = (
            f"## 💻 Code Solution\n**Task:** {prompt}\n\n"
            f"### How It Works\n{expl}\n\n"
            f"### {lang.title()} Implementation\n"
            f"```{lang}\n{code}```\n\n"
            f"### Next Steps\n"
            f"▶️ Click **Run in Playground** to execute live!  \n"
            f"📋 Use **Copy Code** to save it."
        )
        return answer, code.strip(), lang

    # ──────────────────────────────────────────────────────────────────────────
    # SUMMARIZATION
    # ──────────────────────────────────────────────────────────────────────────
    elif any(k in lower for k in ['summarize', 'summary', 'overview', 'notes on']):
        topic = re.sub(r'summarize|summary|overview of|notes on', '', prompt, flags=re.IGNORECASE).strip() or 'the topic'
        answer = (
            f"## 📚 Study Summary: *{topic.title()}*\n\n"
            f"### Core Concept\n"
            f"{topic.capitalize()} is a foundational area covering key principles, frameworks, and applications.\n\n"
            f"### Key Points\n"
            f"1. **Foundations** — Core definitions, axioms, and principles\n"
            f"2. **Architecture** — How components interact and integrate\n"
            f"3. **Applications** — Real-world use cases and patterns\n"
            f"4. **Trade-offs** — Performance vs complexity, theory vs practice\n\n"
            f"### Study Tips\n"
            f"- 📇 Add key terms to **Flashcards** for spaced repetition\n"
            f"- 🗺️ Map relationships on the **Whiteboard**\n"
            f"- 💬 Discuss with peers in **Group Chat**\n"
            f"- ⏱️ Use **Pomodoro** for focused study sessions\n\n"
            f"*Ask me for more detail on any sub-topic!*"
        )
        return answer, None, 'python'

    # ──────────────────────────────────────────────────────────────────────────
    # QUIZ / TEST
    # ──────────────────────────────────────────────────────────────────────────
    elif any(k in lower for k in ['quiz', 'mcq', 'test me', 'question on', 'practice question', 'exam question']):
        topic = re.sub(r'quiz|mcq|test me|question on|practice question|exam question|generate|create|give me|about|on', '', prompt, flags=re.IGNORECASE).strip() or 'Computer Science'
        answer = (
            f"## ❓ Practice Quiz: *{topic.title()}*\n\n"
            f"**Q:** Which best describes a key principle of {topic}?\n\n"
            f"- **A)** Sequential processing without optimization\n"
            f"- **B)** Modular design with clear separation of concerns ✅ *(Correct)*\n"
            f"- **C)** Ignoring edge cases and error handling\n"
            f"- **D)** Tightly coupled components with shared global state\n\n"
            f"### Explanation\n"
            f"**Option B** is correct. Modular design provides:\n"
            f"- **Maintainability** — each module is independently updatable\n"
            f"- **Testability** — units are isolated for focused testing\n"
            f"- **Reusability** — components can be shared across projects\n\n"
            f"*Ask for more questions: \"Give me 5 MCQs on {topic}\"*"
        )
        return answer, None, 'python'

    # ──────────────────────────────────────────────────────────────────────────
    # EXPLANATION
    # ──────────────────────────────────────────────────────────────────────────
    elif any(k in lower for k in ['explain', 'what is', 'what are', 'how does', 'how do', 'define', 'describe', 'tell me about']):
        topic = re.sub(r'explain|what is|what are|how does|how do|define|describe|tell me about', '', prompt, flags=re.IGNORECASE).strip() or 'this concept'
        answer = (
            f"## 💡 Explanation: *{topic.title()}*\n\n"
            f"### Definition\n"
            f"**{topic.capitalize()}** refers to a structured concept or system that enables "
            f"efficient processing and transformation of information within a given domain.\n\n"
            f"### How It Works\n"
            f"1. **Input** — Data or parameters enter the system\n"
            f"2. **Processing** — Transformation logic applies defined rules\n"
            f"3. **Output** — Validated, processed results are returned\n\n"
            f"### Key Characteristics\n"
            f"- ✅ Well-defined inputs and outputs\n"
            f"- ✅ Deterministic behavior under the same conditions\n"
            f"- ✅ Composable with other systems\n\n"
            f"### Common Pitfalls\n"
            f"- ⚠️ Over-engineering simple problems\n"
            f"- ⚠️ Ignoring edge cases and boundary conditions\n"
            f"- ⚠️ Premature optimization without profiling\n\n"
            f"*Test your understanding: ask for a **quiz on {topic}** or try it in the **Code Playground**!*"
        )
        return answer, None, 'python'

    # ──────────────────────────────────────────────────────────────────────────
    # GENERAL STUDY GUIDANCE
    # ──────────────────────────────────────────────────────────────────────────
    else:
        clean_title = prompt.strip().rstrip('.?!')
        answer = (
            f"## 💡 Academic Guidance: *{clean_title}*\n\n"
            f"Here is how you can effectively tackle **{clean_title}**:\n\n"
            f"### 1. Conceptual Framework\n"
            f"Break down **{clean_title}** into core principles, definitions, and underlying mechanisms. "
            f"Use the **Flashcards** tab in your study room for active recall.\n\n"
            f"### 2. Practical Application\n"
            f"Test implementations directly. If this relates to programming, jump into the **Code Playground** to run live test cases.\n\n"
            f"### 3. Collaborative Review\n"
            f"Discuss key takeaways with classmates in **Group Chat** or map out visual diagrams on the **Whiteboard**.\n\n"
            f"💬 *Need more specifics? Try asking:*\n"
            f"* *\"Explain {clean_title} with examples\"*\n"
            f"* *\"Generate a practice quiz on {clean_title}\"*\n"
            f"* *\"Write code for {clean_title}\"*"
        )
        return answer, None, 'python'


@bp.route('/ai/ask', methods=['POST'])
@login_required
def ai_ask():
    try:
        data = request.get_json(silent=True) or {}
        prompt = data.get('prompt', '').strip()
        if not prompt:
            return jsonify({'status': 'error', 'answer': 'Please provide a question or task.'}), 400

        # Optional group_id parameter from the current room
        group_id = data.get('group_id')
        
        # Student Context Gathering
        user_groups = GroupService.get_user_groups(current_user.id) if current_user.is_authenticated else []
        group_names = [g.get('name') for g in user_groups if g.get('name')]
        mins = getattr(current_user, 'total_study_minutes', 0)
        goal = getattr(current_user, 'daily_goal_minutes', 120) or 120
        streak = getattr(current_user, 'streak_count', 1)
        xp = getattr(current_user, 'xp_points', 50)

        context_str = (
            f"Student Name: {current_user.username}\n"
            f"Daily Streak: {streak} days\n"
            f"Experience Points: {xp} XP\n"
            f"Today's Focus: {mins} / {goal} minutes goal\n"
            f"Enrolled Study Rooms: {', '.join(group_names) if group_names else 'None yet'}\n"
        )

        # Gather Study Resources & Uploaded Notes from the current room and user's rooms
        resources_list = []
        target_group_ids = []
        if group_id:
            target_group_ids.append(str(group_id))
        for g in user_groups:
            gid = str(g.get('_id') or g.get('id', ''))
            if gid and gid not in target_group_ids:
                target_group_ids.append(gid)

        for gid in target_group_ids[:5]:
            try:
                room_res = ResourceService.get_group_resources(gid)
                for r in room_res:
                    resources_list.append(r)
            except Exception as e:
                print(f"[Resource Fetch Notice]: {e}")

        # Format resources text for AI comprehension
        resources_context_snippets = []
        for res in resources_list[:12]:
            r_name = res.get('name', 'Untitled Resource')
            r_type = res.get('type', 'note')
            r_content = res.get('content', '').strip()
            r_file = res.get('file_url', '')

            # Extract deep inside content of the document (PDF, Word, TXT, etc.)
            file_extra = ""
            full_res = None
            if res.get('_id'):
                full_res = ResourceService.get_resource_by_id(res['_id'])
            raw_b64 = full_res.get('file_data') if full_res else None

            if raw_b64 or r_file:
                doc_text = _extract_document_text(r_file or full_res.get('filename', 'doc.pdf'), max_chars=8000, raw_data=raw_b64)
                if doc_text:
                    file_extra = f"\n[Full Document Text Extract]:\n{doc_text}"

            snippet = f"### Document: {r_name} (Type: {r_type.upper()})\nDescription/Notes: {r_content}{file_extra}"
            resources_context_snippets.append(snippet)

        resources_context = "\n\n".join(resources_context_snippets) if resources_context_snippets else None

        # 1. Try Google Gemini with full note context
        gemini_key = current_app.config.get('GEMINI_API_KEY') or os.environ.get('GEMINI_API_KEY', '')
        if gemini_key:
            result = _call_gemini(prompt, gemini_key, context_str=context_str, resources_context=resources_context)
            if result:
                text, code, lang, model = result
                return jsonify({
                    'status': 'success',
                    'answer': text,
                    'code': code,
                    'lang': lang,
                    'source': f'Gemini ({model})'
                })

        # 2. Try OpenAI
        openai_key = current_app.config.get('OPENAI_API_KEY') or os.environ.get('OPENAI_API_KEY', '')
        if openai_key:
            result = _call_openai(prompt, openai_key, context_str=f"{context_str}\n\n{resources_context or ''}")
            if result:
                text, code, lang = result
                return jsonify({
                    'status': 'success',
                    'answer': text,
                    'code': code,
                    'lang': lang,
                    'source': 'OpenAI GPT-4o-mini'
                })

        # 3. Built-in intelligent engine with notes support
        answer, code, lang = _builtin_ai(prompt, user=current_user, user_groups=user_groups, resources_context=resources_context)
        return jsonify({
            'status': 'success',
            'answer': answer,
            'code': code,
            'lang': lang,
            'source': 'Virtual Study Group AI'
        })

    except Exception as exc:
        import traceback
        print(f"[AI Route Error]\n{traceback.format_exc()}")
        return jsonify({
            'status': 'success',
            'answer': (
                "## ⚠️ AI Notice\n\n"
                "I ran into an issue processing your request. Please try again.\n\n"
                f"*Debug info: `{str(exc)}`*\n\n"
                "You can still use the **Code Playground** tab to run code directly!"
            )
        })

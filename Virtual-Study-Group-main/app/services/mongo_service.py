import uuid
import datetime
import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.db import mongo

# Fallback In-Memory Storage for zero-config offline execution
_MEMORY_DB = {
    'users': {},
    'groups': {},
    'resources': {},
    'messages': {},
    'tasks': {},
    'whiteboards': {},
    'flashcards': {},
    'study_logs': {},
    'polls': {},
    'calendar': {}
}

def ensure_indexes():
    """Create MongoDB Atlas performance indexes and seed default demo student account."""
    if mongo.is_connected and mongo.db is not None:
        try:
            mongo.db.users.create_index('username', unique=True)
            mongo.db.users.create_index('email', unique=True)
            mongo.db.groups.create_index('room_code', unique=True)
            mongo.db.groups.create_index('members')
            mongo.db.resources.create_index('group_id')
            mongo.db.messages.create_index([('group_id', 1), ('timestamp', 1)])
            mongo.db.study_logs.create_index([('user_id', 1), ('date', -1)])
            print("[DBMS Engine] MongoDB Atlas compound performance indexes verified.")
        except Exception as e:
            print(f"[DBMS Index Warning] Could not ensure indexes: {e}")
            
    # Auto-seed a ready-to-use demo account: student / student123
    seed_demo_account()

def seed_demo_account():
    try:
        existing = User.get_by_username("student")
        if not existing:
            demo_user = User.create(
                username="student",
                email="student@studygroup.local",
                password="student123"
            )
            print("[Auth Engine] Seeded default demo account: username='student', password='student123'")
    except Exception as e:
        print(f"[Auth Engine] Demo account check notice: {e}")

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data.get('_id') or user_data.get('id'))
        self.username = user_data.get('username')
        self.email = user_data.get('email')
        self.password_hash = user_data.get('password_hash')
        self.created_at = user_data.get('created_at', datetime.datetime.utcnow())
        self.avatar_url = user_data.get('avatar_url', f"https://api.dicebear.com/7.x/bottts/svg?seed={self.username}")
        self.streak_count = user_data.get('streak_count', 1)
        self.last_study_date = user_data.get('last_study_date', datetime.date.today().isoformat())
        self.xp_points = user_data.get('xp_points', 50)
        self.total_study_minutes = user_data.get('total_study_minutes', 0)
        self.daily_goal_minutes = user_data.get('daily_goal_minutes', 120)

    @staticmethod
    def get_by_id(user_id):
        if mongo.is_connected and mongo.db is not None:
            data = mongo.db.users.find_one({'_id': str(user_id)})
            return User(data) if data else None
        data = _MEMORY_DB['users'].get(str(user_id))
        return User(data) if data else None

    @staticmethod
    def get_by_username(username):
        u_clean = username.strip()
        if mongo.is_connected and mongo.db is not None:
            data = mongo.db.users.find_one({'username': {'$regex': f'^{u_clean}$', '$options': 'i'}})
            if not data:
                data = mongo.db.users.find_one({'username': u_clean})
            return User(data) if data else None
        for u in _MEMORY_DB['users'].values():
            if u.get('username', '').lower() == u_clean.lower():
                return User(u)
        return None

    @staticmethod
    def get_by_email(email):
        e_clean = email.strip().lower()
        if mongo.is_connected and mongo.db is not None:
            data = mongo.db.users.find_one({'email': {'$regex': f'^{e_clean}$', '$options': 'i'}})
            if not data:
                data = mongo.db.users.find_one({'email': e_clean})
            return User(data) if data else None
        for u in _MEMORY_DB['users'].values():
            if u.get('email', '').lower() == e_clean:
                return User(u)
        return None

    @staticmethod
    def create(username, email, password):
        user_id = str(uuid.uuid4())
        pwd_hash = generate_password_hash(password)
        today_str = datetime.date.today().isoformat()
        user_doc = {
            '_id': user_id,
            'id': user_id,
            'username': username,
            'email': email,
            'password_hash': pwd_hash,
            'created_at': datetime.datetime.utcnow(),
            'avatar_url': f"https://api.dicebear.com/7.x/bottts/svg?seed={username}",
            'streak_count': 1,
            'last_study_date': today_str,
            'xp_points': 50,
            'total_study_minutes': 0,
            'daily_goal_minutes': 120
        }
        if mongo.is_connected and mongo.db is not None:
            mongo.db.users.insert_one(user_doc)
        else:
            _MEMORY_DB['users'][user_id] = user_doc
        return User(user_doc)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class GroupService:
    @staticmethod
    def create_group(name, description, category, creator_id):
        group_id = str(uuid.uuid4())
        room_code = str(uuid.uuid4())[:6].upper()
        group_doc = {
            '_id': group_id,
            'id': group_id,
            'name': name,
            'description': description,
            'category': category or 'General',
            'created_by': str(creator_id),
            'room_code': room_code,
            'members': [str(creator_id)],
            'created_at': datetime.datetime.utcnow(),
            'jitsi_room_name': f"StudyGroup_{room_code}"
        }
        if mongo.is_connected and mongo.db is not None:
            mongo.db.groups.insert_one(group_doc)
        else:
            _MEMORY_DB['groups'][group_id] = group_doc
        return group_doc

    @staticmethod
    def get_by_id(group_id):
        if mongo.is_connected and mongo.db is not None:
            return mongo.db.groups.find_one({'_id': str(group_id)})
        return _MEMORY_DB['groups'].get(str(group_id))

    @staticmethod
    def get_by_room_code(room_code):
        room_code = room_code.strip().upper()
        if mongo.is_connected and mongo.db is not None:
            return mongo.db.groups.find_one({'room_code': room_code})
        for g in _MEMORY_DB['groups'].values():
            if g.get('room_code') == room_code:
                return g
        return None

    @staticmethod
    def get_user_groups(user_id):
        uid = str(user_id)
        if mongo.is_connected and mongo.db is not None:
            return list(mongo.db.groups.find({'members': uid}))
        return [g for g in _MEMORY_DB['groups'].values() if uid in g.get('members', [])]

    @staticmethod
    def get_all_public_groups():
        if mongo.is_connected and mongo.db is not None:
            return list(mongo.db.groups.find().limit(50))
        return list(_MEMORY_DB['groups'].values())

    @staticmethod
    def add_member(group_id, user_id):
        gid, uid = str(group_id), str(user_id)
        if mongo.is_connected and mongo.db is not None:
            mongo.db.groups.update_one({'_id': gid}, {'$addToSet': {'members': uid}})
        else:
            if gid in _MEMORY_DB['groups']:
                if uid not in _MEMORY_DB['groups'][gid]['members']:
                    _MEMORY_DB['groups'][gid]['members'].append(uid)

    @staticmethod
    def delete_group(group_id, user_id):
        gid, uid = str(group_id), str(user_id)
        if mongo.is_connected and mongo.db is not None:
            group = mongo.db.groups.find_one({'_id': gid})
            if group and str(group.get('created_by')) == uid:
                mongo.db.groups.delete_one({'_id': gid})
                mongo.db.resources.delete_many({'group_id': gid})
                mongo.db.messages.delete_many({'group_id': gid})
                mongo.db.tasks.delete_many({'group_id': gid})
                mongo.db.flashcards.delete_many({'group_id': gid})
                return True
        else:
            if gid in _MEMORY_DB['groups']:
                if str(_MEMORY_DB['groups'][gid].get('created_by')) == uid:
                    del _MEMORY_DB['groups'][gid]
                    return True
        return False


class ResourceService:
    @staticmethod
    def add_resource(name, rtype, content, file_url, group_id, uploader_id, filename='', file_data=None, file_mimetype=''):
        res_id = str(uuid.uuid4())
        doc = {
            '_id': res_id,
            'id': res_id,
            'name': name,
            'type': rtype,
            'content': content,
            'file_url': file_url or '',
            'filename': filename or '',
            'file_data': file_data,  # base64 string or binary stored directly in MongoDB
            'file_mimetype': file_mimetype or 'application/octet-stream',
            'group_id': str(group_id),
            'uploaded_by': str(uploader_id),
            'created_at': datetime.datetime.utcnow()
        }
        if mongo.is_connected and mongo.db is not None:
            mongo.db.resources.insert_one(doc)
        else:
            _MEMORY_DB['resources'][res_id] = doc
        return doc

    @staticmethod
    def get_group_resources(group_id):
        gid = str(group_id)
        if mongo.is_connected and mongo.db is not None:
            # Return list of resources (excluding large file_data payload in listing for speed)
            return list(mongo.db.resources.find({'group_id': gid}, {'file_data': 0}).sort('created_at', -1))
        return [
            {k: v for k, v in r.items() if k != 'file_data'}
            for r in _MEMORY_DB['resources'].values() if r.get('group_id') == gid
        ]

    @staticmethod
    def get_resource_by_id(resource_id):
        rid = str(resource_id)
        if mongo.is_connected and mongo.db is not None:
            doc = mongo.db.resources.find_one({'_id': rid})
            if not doc:
                try:
                    from bson.objectid import ObjectId
                    doc = mongo.db.resources.find_one({'_id': ObjectId(rid)})
                except Exception:
                    pass
            if not doc:
                doc = mongo.db.resources.find_one({'id': rid})
            return doc
        return _MEMORY_DB['resources'].get(rid)

    @staticmethod
    def delete_resource(resource_id):
        rid = str(resource_id)
        if mongo.is_connected and mongo.db is not None:
            res = mongo.db.resources.delete_one({'_id': rid})
            return res.deleted_count > 0
        else:
            return _MEMORY_DB['resources'].pop(rid, None) is not None


class ChatService:
    @staticmethod
    def post_message(group_id, user_id, username, text):
        msg_id = str(uuid.uuid4())
        doc = {
            '_id': msg_id,
            'group_id': str(group_id),
            'user_id': str(user_id),
            'username': username,
            'text': text,
            'timestamp': datetime.datetime.utcnow().strftime('%H:%M')
        }
        if mongo.is_connected and mongo.db is not None:
            mongo.db.messages.insert_one(doc)
        else:
            if str(group_id) not in _MEMORY_DB['messages']:
                _MEMORY_DB['messages'][str(group_id)] = []
            _MEMORY_DB['messages'][str(group_id)].append(doc)
        return doc

    @staticmethod
    def get_group_messages(group_id):
        gid = str(group_id)
        if mongo.is_connected and mongo.db is not None:
            msgs = list(mongo.db.messages.find({'group_id': gid}))
            return msgs
        return _MEMORY_DB['messages'].get(gid, [])


class TaskService:
    @staticmethod
    def get_group_tasks(group_id):
        gid = str(group_id)
        if mongo.is_connected and mongo.db is not None:
            return list(mongo.db.tasks.find({'group_id': gid}))
        return [t for t in _MEMORY_DB['tasks'].values() if t.get('group_id') == gid]

    @staticmethod
    def add_task(group_id, title, status='todo'):
        task_id = str(uuid.uuid4())
        doc = {
            '_id': task_id,
            'id': task_id,
            'group_id': str(group_id),
            'title': title,
            'status': status
        }
        if mongo.is_connected and mongo.db is not None:
            mongo.db.tasks.insert_one(doc)
        else:
            _MEMORY_DB['tasks'][task_id] = doc
        return doc

    @staticmethod
    def update_task_status(task_id, status):
        tid = str(task_id)
        if mongo.is_connected and mongo.db is not None:
            mongo.db.tasks.update_one({'_id': tid}, {'$set': {'status': status}})
        else:
            if tid in _MEMORY_DB['tasks']:
                _MEMORY_DB['tasks'][tid]['status'] = status

    @staticmethod
    def delete_task(task_id):
        tid = str(task_id)
        if mongo.is_connected and mongo.db is not None:
            res = mongo.db.tasks.delete_one({'_id': tid})
            return res.deleted_count > 0
        else:
            return _MEMORY_DB['tasks'].pop(tid, None) is not None


class WhiteboardService:
    @staticmethod
    def get_canvas_state(group_id):
        gid = str(group_id)
        if mongo.is_connected and mongo.db is not None:
            doc = mongo.db.whiteboards.find_one({'group_id': gid})
            return doc.get('data') if doc else ''
        return _MEMORY_DB['whiteboards'].get(gid, '')

    @staticmethod
    def save_canvas_state(group_id, data):
        gid = str(group_id)
        if mongo.is_connected and mongo.db is not None:
            mongo.db.whiteboards.update_one({'group_id': gid}, {'$set': {'data': data}}, upsert=True)
        else:
            _MEMORY_DB['whiteboards'][gid] = data


class FlashcardService:
    @staticmethod
    def get_group_cards(group_id):
        gid = str(group_id)
        if mongo.is_connected and mongo.db is not None:
            return list(mongo.db.flashcards.find({'group_id': gid}))
        return [f for f in _MEMORY_DB['flashcards'].values() if f.get('group_id') == gid]

    @staticmethod
    def add_card(group_id, question, answer):
        cid = str(uuid.uuid4())
        doc = {
            '_id': cid,
            'id': cid,
            'group_id': str(group_id),
            'question': question,
            'answer': answer
        }
        if mongo.is_connected and mongo.db is not None:
            mongo.db.flashcards.insert_one(doc)
        else:
            _MEMORY_DB['flashcards'][cid] = doc
        return doc


class AnalyticsService:
    @staticmethod
    def log_study_session(user_id, group_id, group_name, duration_minutes):
        uid = str(user_id)
        log_id = str(uuid.uuid4())
        xp_earned = duration_minutes * 10
        now = datetime.datetime.utcnow()
        today_date = datetime.date.today().isoformat()
        
        doc = {
            '_id': log_id,
            'id': log_id,
            'user_id': uid,
            'group_id': str(group_id),
            'group_name': group_name or 'Independent Study',
            'duration_minutes': duration_minutes,
            'xp_earned': xp_earned,
            'date': today_date,
            'timestamp': now.strftime('%Y-%m-%d %H:%M')
        }
        
        if mongo.is_connected and mongo.db is not None:
            mongo.db.study_logs.insert_one(doc)
            user_data = mongo.db.users.find_one({'_id': uid})
            if user_data:
                last_date = user_data.get('last_study_date')
                curr_streak = user_data.get('streak_count', 1)
                
                if last_date != today_date:
                    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
                    new_streak = (curr_streak + 1) if last_date == yesterday else 1
                else:
                    new_streak = curr_streak

                mongo.db.users.update_one(
                    {'_id': uid},
                    {
                        '$inc': {
                            'total_study_minutes': duration_minutes,
                            'xp_points': xp_earned
                        },
                        '$set': {
                            'streak_count': new_streak,
                            'last_study_date': today_date
                        }
                    }
                )
        else:
            _MEMORY_DB['study_logs'][log_id] = doc
            if uid in _MEMORY_DB['users']:
                _MEMORY_DB['users'][uid]['total_study_minutes'] = _MEMORY_DB['users'][uid].get('total_study_minutes', 0) + duration_minutes
                _MEMORY_DB['users'][uid]['xp_points'] = _MEMORY_DB['users'][uid].get('xp_points', 50) + xp_earned
        return doc

    @staticmethod
    def get_user_logs(user_id):
        uid = str(user_id)
        if mongo.is_connected and mongo.db is not None:
            return list(mongo.db.study_logs.find({'user_id': uid}).sort('date', -1))
        return [l for l in _MEMORY_DB['study_logs'].values() if l.get('user_id') == uid]

    @staticmethod
    def get_group_leaderboard(group_id):
        group = GroupService.get_by_id(group_id)
        if not group:
            return []
        members = group.get('members', [])
        leaderboard = []
        for m_id in members:
            user = User.get_by_id(m_id)
            if user:
                leaderboard.append({
                    'username': user.username,
                    'avatar_url': user.avatar_url,
                    'xp_points': user.xp_points,
                    'streak_count': user.streak_count,
                    'total_hours': round(user.total_study_minutes / 60.0, 1)
                })
        leaderboard.sort(key=lambda x: x['xp_points'], reverse=True)
        return leaderboard


class PollService:
    @staticmethod
    def create_poll(group_id, question, options, creator_name):
        poll_id = str(uuid.uuid4())
        doc = {
            '_id': poll_id,
            'id': poll_id,
            'group_id': str(group_id),
            'question': question,
            'creator': creator_name,
            'options': [{'text': opt, 'votes': 0} for opt in options],
            'voters': []
        }
        if mongo.is_connected and mongo.db is not None:
            mongo.db.polls.insert_one(doc)
        else:
            _MEMORY_DB['polls'][poll_id] = doc
        return doc

    @staticmethod
    def get_group_polls(group_id):
        gid = str(group_id)
        if mongo.is_connected and mongo.db is not None:
            return list(mongo.db.polls.find({'group_id': gid}))
        return [p for p in _MEMORY_DB['polls'].values() if p.get('group_id') == gid]

    @staticmethod
    def vote_poll(poll_id, option_idx, user_id):
        pid, uid = str(poll_id), str(user_id)
        if mongo.is_connected and mongo.db is not None:
            poll = mongo.db.polls.find_one({'_id': pid})
            if poll and uid not in poll.get('voters', []):
                mongo.db.polls.update_one(
                    {'_id': pid},
                    {
                        '$inc': {f'options.{option_idx}.votes': 1},
                        '$addToSet': {'voters': uid}
                    }
                )
        else:
            if pid in _MEMORY_DB['polls']:
                p = _MEMORY_DB['polls'][pid]
                if uid not in p.get('voters', []):
                    p['options'][option_idx]['votes'] += 1
                    p['voters'].append(uid)

    @staticmethod
    def delete_poll(poll_id):
        pid = str(poll_id)
        if mongo.is_connected and mongo.db is not None:
            res = mongo.db.polls.delete_one({'_id': pid})
            return res.deleted_count > 0
        else:
            return _MEMORY_DB['polls'].pop(pid, None) is not None


class CalendarService:
    @staticmethod
    def add_event(group_id, title, event_date, event_type):
        eid = str(uuid.uuid4())
        doc = {
            '_id': eid,
            'id': eid,
            'group_id': str(group_id),
            'title': title,
            'date': event_date,
            'type': event_type  # 'exam', 'meeting', 'deadline'
        }
        if mongo.is_connected and mongo.db is not None:
            mongo.db.calendar.insert_one(doc)
        else:
            _MEMORY_DB['calendar'][eid] = doc
        return doc

    @staticmethod
    def get_group_events(group_id):
        gid = str(group_id)
        if mongo.is_connected and mongo.db is not None:
            return list(mongo.db.calendar.find({'group_id': gid}).sort('date', 1))
        return [e for e in _MEMORY_DB['calendar'].values() if e.get('group_id') == gid]


class SearchService:
    @staticmethod
    def universal_search(query):
        q = query.strip().lower()
        if not q:
            return {'groups': [], 'resources': []}

        all_groups = GroupService.get_all_public_groups()
        matched_groups = [g for g in all_groups if q in g.get('name', '').lower() or q in g.get('category', '').lower() or q in g.get('description', '').lower()]
        
        all_resources = []
        if mongo.is_connected and mongo.db is not None:
            all_resources = list(mongo.db.resources.find().limit(50))
        else:
            all_resources = list(_MEMORY_DB['resources'].values())

        matched_resources = [r for r in all_resources if q in r.get('name', '').lower() or q in r.get('content', '').lower() or q in r.get('type', '').lower()]
        return {'groups': matched_groups, 'resources': matched_resources}


class DatabaseMonitor:
    @staticmethod
    def check_health():
        start_t = time.time()
        if mongo.is_connected and mongo.db is not None:
            try:
                mongo.client.admin.command('ping')
                latency_ms = round((time.time() - start_t) * 1000, 2)
                user_count = mongo.db.users.count_documents({})
                group_count = mongo.db.groups.count_documents({})
                return {
                    'status': 'Online (MongoDB Atlas Cloud)',
                    'latency_ms': latency_ms,
                    'users_count': user_count,
                    'groups_count': group_count,
                    'engine': 'PyMongo 4.x / Atlas Multi-Region Cluster'
                }
            except Exception as e:
                return {'status': f'Error ({e})', 'latency_ms': -1, 'users_count': 0, 'groups_count': 0, 'engine': 'Fallback Engine'}
        else:
            return {
                'status': 'Offline Fallback Engine',
                'latency_ms': 0.1,
                'users_count': len(_MEMORY_DB['users']),
                'groups_count': len(_MEMORY_DB['groups']),
                'engine': 'Local Memory Adapter'
            }

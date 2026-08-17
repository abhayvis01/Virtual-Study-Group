# 🎓 Virtual Study Group - Real-Time Collaborative Learning Platform

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Framework](https://img.shields.io/badge/Framework-Flask-black?logo=flask)
![Database](https://img.shields.io/badge/Database-MongoDB%20Atlas-green?logo=mongodb)
![Cloud Storage](https://img.shields.io/badge/Storage-Firebase-orange?logo=firebase)
![License](https://img.shields.io/badge/License-MIT-purple)

A state-of-the-art, real-time virtual study platform built for students and educators. Features interactive study rooms, WebRTC video calls, peer voice lounges, collaborative whiteboards, live code execution, AI-powered study assistance, study analytics, and milestone certificate generation.

---

## 🌟 Key Features & Architecture

### 📹 1. WebRTC Video Meetings & Voice Lounge
- **In-App HD Video Calls**: Embedded WebRTC video meeting rooms powered by Jitsi Meet SDK with screen sharing capabilities.
- **Peer Audio Lounge**: Lightweight, low-bandwidth voice channel for instant verbal collaboration.

### 🎨 2. Collaborative Whiteboard & Code Playground
- **Live Canvas Whiteboard**: Draw formulas, diagram software architectures, and save canvas states directly to cloud storage.
- **Code Playground**: Multi-language code editor (Python & JavaScript) with real-time runtime execution benchmarking in milliseconds.

### 🤖 3. AI Study Assistant & Smart Tools
- **AI Study Helper**: Generates practice exam questions, concept summaries, and step-by-step academic explanations.
- **Study Task Planner**: Interactive 3-column task board (To-Do, In Progress, Completed) with seamless non-reloading AJAX updates.
- **Room Polls & Calendar**: Real-time room voting and study deadline tracking.

### ⚡ 4. Masterclass DBMS & Gamification Engine
- **MongoDB Atlas Compound Indexing**: Automated index initialization for high-throughput queries on users, chat logs, and study sessions.
- **Daily Target Progress & Gamification**: Animated daily study target tracking, XP points system, daily streak counter, and downloadable **Milestone Certificates**.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Backend Core** | Python, Flask, Werkzeug, Flask-Login, Flask-WTF |
| **Database Engine** | MongoDB Atlas (PyMongo) with compound index optimization |
| **Cloud Services** | Firebase Admin SDK & Web JS SDK |
| **Real-Time Media** | WebRTC (Jitsi Meet External API) & Web Audio Synth API |
| **Frontend UI/UX** | Modern Vanilla CSS, Glassmorphic Design System, FontAwesome 6 |

---

## 🚀 Quick Start & Local Setup

### 1. Prerequisites
- Python 3.10 or higher installed on your system.
- MongoDB Atlas cluster URI (or local MongoDB).

### 2. Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/abhayvis01/Virtual-Study-Group.git
   cd Virtual-Study-Group
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables (`.env`)**:
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=virtual_study_group_secret_key_2026
   MONGO_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/virtual_study_group?retryWrites=true&w=majority
   MONGO_DBNAME=virtual_study_group
   FIREBASE_AUTH_DOMAIN=your-app.firebaseapp.com
   FIREBASE_PROJECT_ID=your-project-id
   ```

4. **Launch the Application**:
   ```bash
   python run.py
   ```
   Open **`http://localhost:5000`** in your browser!
---

## 📄 Terms of Service & Privacy
Includes an integrated Terms of Service agreement page (`/terms`) for academic integrity, encrypted data handling, and privacy compliance.

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for details.

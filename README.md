# 🎮 Game Management System

A full-featured Web-Based Mini-Game Platform built with Python 3 and Flask. The application features user authentication, flat-file persistent storage, real-time score tracking, dynamic leaderboards, an administrative management panel, and interactive browser mini-games.

---

## 🚀 Features

- 🔐 **Authentication & User Management**: User registration, secure login, persistent session state, and profile editing.
- 🛡️ **Admin Dashboard**: Dedicated administrative interface (`admin@gmail.com`) to inspect, monitor, and remove registered user accounts.
- 🏆 **Leaderboard & Score Aggregation**: Dynamic scoring system that reads game logs and ranks top players on a central leaderboard.
- 📁 **Flat-File Database Persistence**: Lightweight text-based storage system (`data/users.txt` and `data/scores/*.txt`) eliminating external database overhead.
- 🕹️ **Interactive Games**:
  - ✊ **Rock-Paper-Scissors (`rps.py`)**: Best-of-3 round logic with session saving and time-seeded move generation.
  - 🔤 **Hangman (`hangman.py`)**: Category hints, visual ASCII art stages, and difficulty choices (Easy, Medium, Hard).
  - 🧮 **Math Quiz (`math_quiz.py`)**: Dynamic arithmetic challenge module with automated evaluation.

---

## 🛠️ Tech Stack & Dependencies

- **Backend**: Python 3.12, Flask 3.1.1, Werkzeug 3.1.3, Jinja2 3.1.6, ItsDangerous 2.2.0, Click 8.2.1
- **Frontend**: HTML5, CSS3 (`static/css/style.css`), JavaScript (`static/js/app.js`), Jinja Templates
- **Storage**: Plain-Text / CSV Formatted File I/O (`data/`)

---

## 📂 Project Structure

```text
Game-Management-system/
├── data/                      # File-based database storage
│   ├── users.txt              # User profile records
│   └── scores/                # Player score text logs (*.txt)
├── games/                     # Game logic engines
│   ├── __init__.py
│   ├── hangman.py             # Hangman word-guess engine & ASCII art
│   ├── math_quiz.py           # Math quiz logic
│   └── rps.py                 # Rock-Paper-Scissors game engine
├── static/                    # Front-end static assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── templates/                 # Jinja2 HTML views
│   ├── admin.html             # Admin user management panel
│   ├── base.html              # Base layout template
│   ├── games.html             # Main game hub UI
│   ├── hangman.html           # Hangman UI
│   ├── index.html             # Homepage & summary dashboard
│   ├── login.html             # User login page
│   ├── math_quiz.html         # Math quiz UI
│   ├── modals.html            # UI modal dialogs
│   ├── profile.html           # Profile view and edit page
│   ├── rps.html               # Rock-Paper-Scissors UI
│   ├── scores.html            # Scoreboard and top players leaderboard
│   └── signup.html            # Registration form
├── admin.py                   # Admin authentication & logic
├── app.py                     # Main Flask routing application entrypoint
├── auth.py                    # User authentication handlers
├── game_menu.py               # Game selection routing helper
├── home.py                    # Leaderboard & score parsing logic
├── main_file.py               # Application startup script
├── user.py                    # User class and file I/O operations
├── user_profile.py            # User profile management utility
├── requirements.txt           # Python dependency file
├── .gitignore
├── .replit
└── README.md                  # Project documentation

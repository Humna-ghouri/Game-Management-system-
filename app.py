from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from user import User  # Import custom user class
from datetime import datetime
from games.hangman import HangmanGame  # Hangman game logic
from games.math_quiz import MathQuizGame  # Math quiz logic
from games.rps import RPSGame  # Rock-Paper-Scissors logic

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session handling

# Static admin credentials for admin login
ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "adminmain90@"


@app.route('/')
def index():
    # Home route - checks if user is logged in
    if 'user' in session:
        user = User.from_dict(session['user'])  # Load user from session dictionary
        top_players = User.get_top_players()    # Get top players from user data
        scores = user.get_scores()              # Get scores of the current user
        return render_template('index.html', user=user, top_players=top_players, scores=scores)
    return redirect(url_for('login'))  # If user not logged in, redirect to login page


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Handles both GET and POST login logic
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # If admin logs in with predefined credentials
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['admin'] = True  # Set admin session
            return redirect(url_for('admin_panel'))

        # Regular user authentication
        user = User.authenticate(email, password)
        if user:
            session['user'] = user.__dict__  # Store user info in session
            return redirect(url_for('index'))

        # If login fails, return with error
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')  # Show login form


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # User registration logic
    if request.method == 'POST':
        try:
            # Create new user object using form inputs
            user = User(
                request.form['name'],
                request.form['email'],
                request.form['password'],
                request.form.get('age', ''),
                request.form.get('gender', ''),
                request.form['nick']
            )
            user.save_to_file()  # Save user to text file
            session['user'] = user.__dict__  # Add user to session
            return redirect(url_for('index'))
        except Exception as e:
            return render_template('signup.html', error=str(e))
    return render_template('signup.html')  # Show registration form


@app.route('/logout')
def logout():
    # Clear all session data (logout both user and admin)
    session.clear()
    return redirect(url_for('login'))


@app.route('/games')
def games():
    # Simple page that lists all available games (must be logged in)
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('games.html')


@app.route('/games/hangman', methods=['GET', 'POST'])
def hangman_page():
    # Hangman game route
    if 'user' not in session:
        return redirect(url_for('login'))

    user = User.from_dict(session['user'])

    if request.method == 'GET':
        # Render game UI
        return render_template('hangman.html')

    if request.method == 'POST':
        try:
            data = request.get_json()
            if not data or 'action' not in data:
                return jsonify({"error": "Invalid request"}), 400

            action = data.get('action')

            if action == 'new':
                # Start new hangman game with selected level
                level = data.get('level', 'easy')
                game = HangmanGame(player_name=user.nick, level=level)
                session['hangman_game'] = game.to_dict()  # Save game state to session
                return jsonify(game.get_game_state())  # Send initial game state to frontend

            elif action == 'guess':
                # Make a guess in hangman
                if 'hangman_game' not in session:
                    return jsonify({"error": "No active game found"}), 400

                game = HangmanGame.from_dict(session['hangman_game'])
                letter = data.get('letter', '').lower()

                # Validate input (must be single alphabet character)
                if not letter.isalpha() or len(letter) != 1:
                    return jsonify({"error": "Invalid letter"}), 400

                state = game.guess_letter(letter)  # Process guess
                session['hangman_game'] = game.to_dict()  # Save updated game state

                if state.get("game_over"):
                    game.save_result()  # Save score if game ends

                return jsonify(state)

            return jsonify({"error": "Invalid action type"}), 400

        except Exception as e:
            return jsonify({"error": "Internal server error", "details": str(e)}), 500


@app.route('/games/math_quiz', methods=['GET', 'POST'])
def math_quiz():
    # Math quiz route
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = User.from_dict(session['user'])
    if not user:
        return redirect(url_for('login'))

    if 'math_quiz' not in session:
        session['math_quiz'] = {}  # Initialize empty game state

    game = MathQuizGame(user, session.get('math_quiz'))  # Restore existing game or new one

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        try:
            if data.get('action') == 'answer':
                # Validate answer to a question
                result = game.check_answer(data['question'], data['answer'])
                session['math_quiz'] = game.save_to_session()
                session.modified = True
                return jsonify(result)

            elif data.get('action') == 'new':
                # Start a new quiz with selected level
                result = game.new_quiz(data.get('level', 'Easy'))
                session['math_quiz'] = game.save_to_session()
                session.modified = True
                return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return render_template('math_quiz.html')  # Render quiz UI


@app.route('/games/rps', methods=['GET', 'POST'])
def rps():
    # Rock-Paper-Scissors game route
    if 'user' not in session:
        return redirect(url_for('login'))

    user = User.from_dict(session['user'])
    if not user:
        return redirect(url_for('login'))

    # Continue previous game or start new
    if 'rps_game' in session:
        game = RPSGame.from_dict(user, session['rps_game'])
    else:
        game = RPSGame(user)

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        if data.get('action') == 'play':
            if 'choice' not in data:
                return jsonify({"error": "Missing choice"}), 400

            result = game.play_round(data['choice'])  # Process round
            session['rps_game'] = game.to_dict()
            return jsonify(result)

        elif data.get('action') == 'new':
            game = RPSGame(user)  # New game instance
            session['rps_game'] = game.to_dict()
            return jsonify(game.new_game())

        return jsonify({"error": "Invalid action"}), 400

    return render_template('rps.html', user=user)  # Show game UI


@app.route('/profile')
def profile():
    # Show current user's profile
    if 'user' not in session:
        return redirect(url_for('login'))
    user = User.from_dict(session['user'])
    return render_template('profile.html', user=user)


@app.route('/profile/edit', methods=['POST'])
def edit_profile():
    # Edit profile and update user data
    if 'user' not in session:
        return redirect(url_for('login'))

    user = User.from_dict(session['user'])

    # Create updated user object with new data
    updated_user = User(
        request.form['name'],
        request.form['email'],
        request.form['password'],
        request.form['age'],
        request.form['gender'],
        user.nick  # Preserve nickname
    )

    User.update_user(user.nick, updated_user)  # Update user data in file
    session['user'] = updated_user.__dict__  # Refresh session with new info
    return redirect(url_for('profile'))


@app.route('/scores')
def scores():
    # Show user's score and leaderboard
    if 'user' not in session:
        return redirect(url_for('login'))
    user = User.from_dict(session['user'])
    scores = user.get_scores()
    top_players = User.get_top_players()
    return render_template('scores.html', scores=scores, top_players=top_players)


@app.route('/admin')
def admin_panel():
    # Admin dashboard to manage users
    if 'admin' not in session:
        return redirect(url_for('login'))
    users = User.load_users()
    return render_template('admin.html', users=users)


@app.route('/admin/delete_user', methods=['POST'])
def delete_user():
    # Delete a user from file (admin only)
    if 'admin' not in session:
        return redirect(url_for('login'))

    email = request.form['email']
    users = User.load_users()

    # Filter out the user to delete
    updated_users = [u for u in users if u.email != email]

    # Rewrite file without that user
    with open("data/users.txt", "w") as file:
        for user in updated_users:
            file.write(f"{user.name},{user.email},{user.password},{user.age},{user.gender},{user.nick}\n")

    return redirect(url_for('admin_panel'))


# if __name__ == '__main__':
#     # Ensure required folder exists before running
#     os.makedirs('data/scores', exist_ok=True)
#     app.run(debug=True)  # Run app in debug mode for development


# for replit

if __name__ == '__main__':
    os.makedirs('data/scores', exist_ok=True)
    app.run(host='0.0.0.0', port=81)

import os
from collections import defaultdict

class User:
    def __init__(self, name, email, password, age, gender, nick):
        # Initialize a user with all required attributes
        self.name = name
        self.email = email
        self.password = password
        self.age = age
        self.gender = gender
        self.nick = nick  # Unique nickname used as identifier

    def save_to_file(self):
        # Save user information to 'data/users.txt'
        os.makedirs('data', exist_ok=True)  # Create 'data' folder if it doesn't exist
        with open('data/users.txt', 'a', encoding='utf-8') as f:
            # Append user data in comma-separated format
            f.write(f"{self.name},{self.email},{self.password},{self.age},{self.gender},{self.nick}\n")

    @staticmethod
    def load_users():
        # Load all users from 'users.txt' into a list of User objects
        users = []
        if os.path.exists('data/users.txt'):
            with open('data/users.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) == 6:
                        users.append(User(*parts))  # Unpack user data directly into constructor
        return users

    @staticmethod
    def authenticate(email, password):
        # Check if given email/password match any user
        for user in User.load_users():
            if user.email == email and user.password == password:
                return user  # Return matched user
        return None  # If not found

    @staticmethod
    def load_user(nick):
        # Find and return user by nickname
        for user in User.load_users():
            if user.nick == nick:
                return user
        return None

    def get_scores(self):
        # Return list of lines (score entries) for this user
        score_file = f'data/scores/{self.nick}.txt'
        if os.path.exists(score_file):
            with open(score_file, 'r', encoding='utf-8') as f:
                return f.read().splitlines()  # Read scores line by line
        return ["No scores yet"]

    @staticmethod
    def get_top_players(limit=10):
        # Calculate and return top players based on score files
        player_scores = defaultdict(int)  # Holds total score for each user
        scores_dir = 'data/scores'

        if os.path.exists(scores_dir):
            for filename in os.listdir(scores_dir):
                if filename.endswith('.txt'):
                    nick = filename[:-4]  # Remove '.txt' to get nickname
                    try:
                        with open(os.path.join(scores_dir, filename), 'r', encoding='utf-8') as f:
                            for line in f:
                                score = 0

                                # Parse different game formats:
                                if 'Math Quiz' in line and 'Score:' in line:
                                    score = int(line.split('Score:')[1].split('/')[0].strip())  # e.g., Score: 3/5

                                elif 'Wins:' in line:
                                    score = int(line.split('Wins:')[1].split('|')[0].strip())  # e.g., Wins: 2 | Losses: 1

                                elif 'WON' in line:
                                    score = 1  # Hangman win counted as 1 point

                                if score:
                                    player_scores[nick] += score  # Add score to total
                    except Exception:
                        continue  # Skip errors silently

        # Return top `limit` players sorted by score in descending order
        return sorted(player_scores.items(), key=lambda x: x[1], reverse=True)[:limit]

    @staticmethod
    def update_user(old_nick, updated_user):
        # Update existing user info based on their nickname
        users = User.load_users()
        with open('data/users.txt', 'w', encoding='utf-8') as f:
            for user in users:
                if user.nick == old_nick:
                    # Overwrite old user record with updated values
                    f.write(f"{updated_user.name},{updated_user.email},{updated_user.password},{updated_user.age},{updated_user.gender},{updated_user.nick}\n")
                else:
                    # Keep other users as-is
                    f.write(f"{user.name},{user.email},{user.password},{user.age},{user.gender},{user.nick}\n")

    def to_dict(self):
        # Convert user object to dictionary (useful for session storage)
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "age": self.age,
            "gender": self.gender,
            "nick": self.nick
        }

    @staticmethod
    def from_dict(data):
        # Recreate User object from dictionary (used when restoring session)
        return User(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            age=data["age"],
            gender=data["gender"],
            nick=data["nick"]
        )

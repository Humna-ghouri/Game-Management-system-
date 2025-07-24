import random
import os
from datetime import datetime

class HangmanGame:
    def __init__(self, player_name, level='easy'):
        self.player_name = player_name  # Nickname of the player
        self.level = level  # Difficulty level: easy, medium, hard

        # Set max attempts based on difficulty level
        self.max_attempts = 6 if level == 'easy' else 5 if level == 'medium' else 4
        self.attempts_left = self.max_attempts  # Remaining attempts

        self.guessed_letters = []  # Stores letters guessed so far
        self.secret_word = self.select_word()  # Randomly select a word for this game
        self.game_status = "playing"  # Game status: 'playing', 'won', or 'lost'
        self.hint = self.get_hint()  # Provide a hint based on the word category

    def select_word(self):
        """Select a word based on difficulty level"""
        word_lists = {
            'easy': ['apple', 'banana', 'cherry', 'dog', 'cat', 'house', 'tree', 'water'],
            'medium': ['elephant', 'giraffe', 'bicycle', 'airport', 'kitchen'],
            'hard': ['extravaganza', 'juxtaposition', 'quintessential', 'xylophone']
        }
        return random.choice(word_lists[self.level])  # Randomly pick word from the selected level

    def get_hint(self):
        """Return a hint based on the word category"""
        # Categories help user identify the type of word
        categories = {
            'apple': 'fruit', 'banana': 'fruit', 'cherry': 'fruit',
            'dog': 'animal', 'cat': 'animal', 'elephant': 'animal', 'giraffe': 'animal',
            'house': 'place', 'tree': 'plant', 'water': 'liquid',
            'bicycle': 'vehicle', 'airport': 'place', 'kitchen': 'room',
            'extravaganza': 'event', 'juxtaposition': 'concept',
            'quintessential': 'adjective', 'xylophone': 'musical instrument'
        }
        return f"Category: {categories.get(self.secret_word, 'general')}"  # Default: 'general'

    def display_word(self):
        """Return the word with guessed letters revealed"""
        # Show guessed letters, hide others with "_"
        return ' '.join([letter if letter in self.guessed_letters else '_' for letter in self.secret_word])

    def get_hangman_drawing(self):
        """Return ASCII art of hangman based on attempts left"""
        # Visual stages from full health to full hang
        stages = [
            """
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |     / \\
            """,
            """
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |     / 
            """,
            """
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |      
            """,
            """
               --------
               |      |
               |      O
               |     \\|
               |      |
               |     
            """,
            """
               --------
               |      |
               |      O
               |      |
               |      |
               |     
            """,
            """
               --------
               |      |
               |      O
               |    
               |      
               |     
            """,
            """
               --------
               |      |
               |      
               |    
               |      
               |     
            """
        ]
        return stages[self.attempts_left]  # Return drawing based on remaining attempts

    def guess_letter(self, letter):
        """Process a letter guess"""
        if letter in self.guessed_letters:
            return {"error": "Letter already guessed"}  # Prevent repeating same letter

        self.guessed_letters.append(letter)  # Track guessed letter

        if letter not in self.secret_word:
            self.attempts_left -= 1  # Wrong guess, reduce attempts

        # Check if all letters in word have been guessed
        if all(l in self.guessed_letters for l in self.secret_word):
            self.game_status = "won"
        elif self.attempts_left <= 0:
            self.game_status = "lost"

        return self.get_game_state()  # Return updated game state

    def reset_game(self):
        """Reset the game state"""
        self.__init__(self.player_name, self.level)  # Re-initialize the game

    def get_game_state(self):
        """Return the current game state with extra keys for game_over and win check"""
        return {
            "status": self.game_status,  # 'playing', 'won', 'lost'
            "displayed_word": self.display_word(),  # Word progress with guessed letters
            "guessed_letters": self.guessed_letters,  # Letters guessed so far
            "attempts_left": self.attempts_left,  # Remaining chances
            "hangman_drawing": self.get_hangman_drawing(),  # Current drawing
            "hint": self.hint,  # Word category
            "level": self.level,  # Difficulty level
            "secret_word": self.secret_word if self.game_status != "playing" else "",  # Reveal word after game ends
            "game_over": self.game_status in ["won", "lost"],  # Boolean to check if game is over
            "won": self.game_status == "won"  # Boolean to check win
        }

    def to_dict(self):
        """Serialize game state to dict"""
        return self.__dict__  # Return full internal state

    @classmethod
    def from_dict(cls, data):
        """Deserialize game state from dict"""
        game = cls(data['player_name'], data['level'])  # Create new instance
        game.__dict__ = data  # Restore all values from saved data
        return game

    def save_result(self):
        """Save game result to file"""
        os.makedirs("data/scores", exist_ok=True)  # Make sure scores folder exists
        with open(f"data/scores/{self.player_name}.txt", "a", encoding="utf-8") as f:
            # Format: Game type | Level | Word | Status | Guessed letters | Date
            f.write(
                f"Hangman | Level: {self.level.capitalize()} | Word: {self.secret_word} | "
                f"Status: {self.game_status.upper()} | Guessed: {','.join(self.guessed_letters)} | "
                f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )

import os
from collections import defaultdict
from user import User
from typing import List, Tuple

class HomePage:
    def __init__(self):
        self.current_user = None  # Will hold the currently logged-in user

    def set_current_user(self, user):
        # Set the current user object (usually from session)
        self.current_user = user

    def get_scores(self) -> List[str]:
        """Read current user's score file and return list of lines"""
        # Construct path to the current user's score file
        score_file = f"data/scores/{self.current_user.nick}.txt"
        
        # If file exists, read all lines and return as list
        if os.path.exists(score_file):
            with open(score_file, "r") as f:
                return f.read().splitlines()
        
        # If file doesn't exist, return a message
        return ["No scores found"]

    def get_top_players(self) -> List[Tuple[str, int]]:
        """Calculate top 10 players by total score"""
        
        player_scores = defaultdict(int)  # Dictionary to hold player -> total score
        scores_dir = "data/scores"  # Directory where all score files are stored

        # If scores directory does not exist, return empty list
        if not os.path.exists(scores_dir):
            return []

        # Loop through all .txt files in the scores directory
        for filename in os.listdir(scores_dir):
            if filename.endswith(".txt"):
                player = filename.replace(".txt", "")  # Extract player name from filename
                
                # Open and read the score file
                with open(os.path.join(scores_dir, filename)) as f:
                    for line in f:
                        if "Score:" in line:
                            try:
                                # Math Quiz format: "Score: 3/5"
                                if "Math Quiz" in line:
                                    score = int(line.split("Score:")[1].split("/")[0].strip())

                                # Rock-Paper-Scissors format: "Wins: 2 | Losses: 1"
                                elif "Wins:" in line:
                                    score = int(line.split("Wins:")[1].split("|")[0].strip())

                                # Hangman win line format: "YOU WON"
                                elif "WON" in line:
                                    score = 1  # Each win counts as 1 point

                                else:
                                    continue  # Skip lines that don't match expected patterns

                                player_scores[player] += score  # Add score to player total
                            except:
                                continue  # Ignore any parsing errors and continue

        # Sort players by total score in descending order
        sorted_players = sorted(player_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Return top 10 players
        return sorted_players[:10]

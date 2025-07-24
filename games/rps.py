# import os
# import random
# from time import sleep

# class RPSGame:
#     def __init__(self, user):
#         self.user = user
#         self.choices = {
#             'rock': '✊', 
#             'paper': '✋', 
#             'scissors': '✌️',
#             'quit': '🚪',
#             'pause': '⏸'
#         }
#         self.wins = 0
#         self.rounds = 0
        
#     def save_score(self):
#         os.makedirs("data/scores", exist_ok=True)
#         with open(f"data/scores/{self.user.nick}.txt", "a") as f:
#             f.write(f"Rock Paper Scissors | Rounds: {self.rounds} | Wins: {self.wins}\n")

#     def play(self):
#         print("\n" + "="*40)
#         print("✊✋✌ WELCOME TO ROCK PAPER SCISSORS! ✌✋✊".center(40))
#         print("="*40)
#         print("\n💡 How to play:")
#         print("- First to 3 wins becomes champion!")
#         print("- Type 'rock', 'paper', or 'scissors'")
#         print("- Type 'pause' to pause the game")
#         print("- Type 'quit' to return to menu\n")
        
#         while self.wins < 3 and (self.rounds - self.wins) < 3:
#             self.rounds += 1
#             print(f"\nROUND {self.rounds} (You: {self.wins} - Computer: {self.rounds-self.wins-1})")
            
#             while True:
#                 user_choice = input("Your move: ").lower()
                
#                 if user_choice == 'pause':
#                     input("\n⏸ Game paused. Press Enter to continue...")
#                     continue
#                 elif user_choice == 'quit':
#                     print("\n🚪 Quitting game...")
#                     self.save_score()
#                     return
#                 elif user_choice in self.choices:
#                     break
#                 else:
#                     print("❌ Invalid choice! Choose rock/paper/scissors")
            
#             comp_choice = random.choice(['rock', 'paper', 'scissors'])
            
#             print(f"\nYou chose: {self.choices[user_choice]} {user_choice.upper()}")
#             print(f"Computer chose: {self.choices[comp_choice]} {comp_choice.upper()}")
#             sleep(1)
            
#             if user_choice == comp_choice:
#                 print("\n🤝 IT'S A TIE!")
#                 self.rounds -= 1  # Don't count ties as rounds
#             elif ((user_choice == 'rock' and comp_choice == 'scissors') or
#                   (user_choice == 'paper' and comp_choice == 'rock') or
#                   (user_choice == 'scissors' and comp_choice == 'paper')):
#                 print("\n🎉 YOU WIN THIS ROUND!")
#                 self.wins += 1
#             else:
#                 print("\n😞 COMPUTER WINS THIS ROUND!")
        
#         self.save_score()
#         if self.wins >= 3:
#             print("\n🏆 YOU ARE THE CHAMPION! 🏆")
#         else:
#             print("\n💻 COMPUTER WINS THE GAME!")
        
#         sleep(1)
#         print(f"\nFINAL SCORE: You {self.wins} - Computer {self.rounds-self.wins}")


import os
import time
from datetime import datetime

class RPSGame:
    def __init__(self, user):
        # ✅ Initializes a new Rock-Paper-Scissors game
        # Keeps track of rounds played, wins, and losses for the given user
        self.user = user
        self.rounds = 0
        self.wins = 0
        self.losses = 0

    def new_game(self):
        # ✅ Resets game statistics to start fresh
        self.rounds = 0
        self.wins = 0
        self.losses = 0
        return {"status": "new_game", "error": None}

    def play_round(self, user_choice):
        # ✅ This method handles one round of the game
        # Compares user choice with computer's and determines win/lose/tie

        choices = ['rock', 'paper', 'scissors']

        # ✅ Validate if user input is valid
        if user_choice not in choices:
            return {"error": "Invalid choice"}

        # ✅ Generate computer's move based on the current time
        computer_choice = choices[int(str(time.time())[-1]) % 3]

        # ✅ Determine round result: win, lose, or tie
        if user_choice == computer_choice:
            result = 'tie'
        elif (user_choice == 'rock' and computer_choice == 'scissors') or \
             (user_choice == 'paper' and computer_choice == 'rock') or \
             (user_choice == 'scissors' and computer_choice == 'paper'):
            result = 'win'
            self.wins += 1  # ✅ Add to win count if user wins
        else:
            result = 'lose'
            self.losses += 1  # ✅ Add to loss count if user loses

        self.rounds += 1  # ✅ Increment round counter

        # ✅ Check if game is over (first to 3 wins or 3 losses)
        game_over = self.wins >= 3 or self.losses >= 3
        if game_over:
            self.save_result()  # ✅ Save result to user file

        # ✅ Return round result and current stats
        return {
            "user_choice": user_choice,
            "computer_choice": computer_choice,
            "result": result,
            "rounds": self.rounds,
            "wins": self.wins,
            "losses": self.losses,
            "game_over": game_over,
            "error": None
        }

    def save_result(self):
        # ✅ This method saves the final result of the RPS game to a file
        os.makedirs('data/scores', exist_ok=True)

        # ✅ Game is considered won if user gets 3 or more wins
        result = "won" if self.wins >= 3 else "lost"

        # ✅ Append result to user’s score file with timestamp
        with open(f'data/scores/{self.user.nick}.txt', 'a') as f:
            f.write(f"RPS | Rounds: {self.rounds} | Result: {result} | Date: {datetime.now()}\n")

    def to_dict(self):
        # ✅ Convert current game state into dictionary (for saving in session)
        return {
            "rounds": self.rounds,
            "wins": self.wins,
            "losses": self.losses
        }

    @classmethod
    def from_dict(cls, user, data):
        # ✅ Create a game instance from previously saved state (session restore)
        game = cls(user)
        game.rounds = data.get("rounds", 0)
        game.wins = data.get("wins", 0)
        game.losses = data.get("losses", 0)
        return game

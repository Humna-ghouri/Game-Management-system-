# from games.hangman import HangmanGame
# from games.math_quiz import MathQuizGame
# from games.rps import RPSGame

# def play_game_menu(current_user):
#     while True:
#         print("\n🎮 Game Menu:")
#         print("1. Hangman")
#         print("2. Math Quiz")
#         print("3. Rock Paper Scissors")
#         print("4. Back to Home")
#         choice = input("Select a game (1-4): ")

#         if choice == "1":
#             game = HangmanGame(current_user)
#             game.play()
#         elif choice == "2":
#             game = MathQuizGame(current_user)
#             game.start()
#         elif choice == "3":
#             game = RPSGame(current_user)
#             game.play()
#         elif choice == "4":
#             break
#         else:
#             print("❌ Invalid game choice.")
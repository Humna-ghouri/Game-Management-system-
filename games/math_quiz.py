from datetime import datetime
import os
from pathlib import Path

class MathQuizGame:
    def __init__(self, user, state=None):
        # ✅ This constructor initializes the quiz for the current user
        # If previous state is provided (from session), it resumes the game
        self.user = user

        # ✅ All questions are grouped by level: Easy, Medium, Hard
        self.questions = {
            "Easy": [
                {"question": "5 + 3 = ", "answer": 8},
                {"question": "9 - 2 = ", "answer": 7},
                {"question": "4 × 3 = ", "answer": 12},
                {"question": "10 ÷ 2 = ", "answer": 5},
                {"question": "1 + 1 = ", "answer": 2}
            ],
            "Medium": [
                {"question": "12 + 15 = ", "answer": 27},
                {"question": "20 - 8 = ", "answer": 12},
                {"question": "7 × 4 = ", "answer": 28},
                {"question": "36 ÷ 6 = ", "answer": 6},
                {"question": "13 + 9 = ", "answer": 22}
            ],
            "Hard": [
                {"question": "45 + 28 = ", "answer": 73},
                {"question": "100 - 37 = ", "answer": 63},
                {"question": "12 × 8 = ", "answer": 96},
                {"question": "144 ÷ 12 = ", "answer": 12},
                {"question": "25 × 4 = ", "answer": 100}
            ]
        }

        # ✅ Load values from session if available, otherwise use defaults
        self.level = state.get('level', 'Easy') if state else 'Easy'
        self.current_question_index = state.get('current_question_index', 0) if state else 0
        self.score = state.get('score', 0) if state else 0
        self.time_limit = state.get('time_limit', 30) if state else 30

    def new_quiz(self, level='Easy'):
        # ✅ Starts a new quiz with selected level, resets everything
        self.level = level
        self.current_question_index = 0
        self.score = 0
        self.time_limit = 30 if level == "Easy" else 45 if level == "Medium" else 60

        # ✅ Return first question and initial game setup
        return {
            "question": self.questions[self.level][self.current_question_index]["question"],
            "level": self.level,
            "time_limit": self.time_limit,
            "error": None
        }

    def check_answer(self, question, answer):
        # ✅ Called when user submits an answer
        # It checks the answer, updates the score, and goes to the next question

        try:
            answer = int(answer)  # ensure answer is a number
        except ValueError:
            return {"error": "Please enter a valid number"}

        current_q = self.questions[self.level][self.current_question_index]
        is_correct = answer == current_q["answer"]

        # ✅ Log whether the answer was correct or not
        if is_correct:
            self.score += 1
            self._log_score_entry(current_q["question"], True)
        else:
            self._log_score_entry(current_q["question"], False)

        self.current_question_index += 1

        # ✅ If user has answered all questions in current level
        if self.current_question_index >= len(self.questions[self.level]):
            self.save_result()
            next_level = self._get_next_level()
            return self._build_level_complete_response(current_q, is_correct, next_level)

        # ✅ Otherwise return the next question
        return self._build_standard_response(current_q, is_correct)

    def _log_score_entry(self, question, correct):
        # ✅ Saves the result of each individual question (correct/incorrect) in user’s score file
        try:
            scores_dir = Path('data') / 'scores'
            scores_dir.mkdir(parents=True, exist_ok=True)
            filepath = scores_dir / f"{self.user.nick}.txt"
            with open(filepath, 'a', encoding='utf-8') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(
                    f"Math Quiz | Level: {self.level} | Question: {question.strip()} | "
                    f"Status: {'CORRECT' if correct else 'INCORRECT'} | Score: {self.score} | Date: {timestamp}\n"
                )
        except Exception as e:
            print(f"ERROR LOGGING SCORE ENTRY: {str(e)}")

    def save_result(self):
        # ✅ Saves the final result when quiz ends — total score, pass/fail, timestamp
        try:
            scores_dir = Path('data') / 'scores'
            scores_dir.mkdir(parents=True, exist_ok=True)
            filepath = scores_dir / f"{self.user.nick}.txt"
            with open(filepath, 'a', encoding='utf-8') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(
                    f"Math Quiz | Level: {self.level} | Final Score: {self.score}/{len(self.questions[self.level])} | "
                    f"Status: {'PASSED' if self.score >= len(self.questions[self.level]) // 2 else 'FAILED'} | "
                    f"Date: {timestamp}\n"
                )
        except Exception as e:
            print(f"ERROR SAVING FINAL RESULT: {str(e)}")

    def _get_next_level(self):
        # ✅ This helper decides the next level in the quiz
        # Easy → Medium → Hard → None
        if self.level == "Easy":
            return "Medium"
        elif self.level == "Medium":
            return "Hard"
        return None  # If already at Hard level

    def _build_level_complete_response(self, current_q, is_correct, next_level):
        # ✅ Builds and returns final result of the level with next level info
        response = {
            "correct": is_correct,
            "correct_answer": current_q["answer"],
            "is_last": next_level is None,
            "final_score": self.score,
            "total_questions": len(self.questions[self.level]),
            "error": None
        }

        # ✅ If there is a next level, add its details in response
        if next_level:
            response.update({
                "next_level": next_level,
                "next_question": self.questions[next_level][0]["question"],
                "time_limit": 45 if next_level == "Medium" else 60
            })
        return response

    def _build_standard_response(self, current_q, is_correct):
        # ✅ This response is returned after every normal question (not last one)
        return {
            "correct": is_correct,
            "correct_answer": current_q["answer"],
            "next_question": self.questions[self.level][self.current_question_index]["question"],
            "error": None
        }

    def save_to_session(self):
        # ✅ Used to save current game state in Flask session
        # So that it can be resumed if the page is reloaded
        return {
            "level": self.level,
            "current_question_index": self.current_question_index,
            "score": self.score,
            "time_limit": self.time_limit
        }

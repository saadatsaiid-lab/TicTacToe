import os
import json
import random
import time

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.core.window import Window


# ============================================================
# SCORE FILE
# ============================================================

SCORE_FILE = os.path.join(
    os.path.dirname(__file__),
    "tic_tac_toe_scores.json"
)


# ============================================================
# LOAD / SAVE SCORES
# ============================================================

def load_scores():

    default_scores = {
        "wins": 0,
        "losses": 0,
        "draws": 0
    }

    try:

        if os.path.exists(SCORE_FILE):

            with open(
                SCORE_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                for key in default_scores:

                    if key not in data:
                        data[key] = 0

                return data

    except Exception:
        pass

    return default_scores


def save_scores(scores):

    try:

        with open(
            SCORE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                scores,
                file,
                indent=4
            )

    except Exception as error:

        print("Could not save scores:", error)


# ============================================================
# MAIN GAME
# ============================================================

class TicTacToe(App):

    def build(self):

        Window.clearcolor = (
            0.035,
            0.04,
            0.06,
            1
        )

        self.scores = load_scores()

        self.board = [""] * 9

        self.player = "X"
        self.ai = "O"

        self.game_over = False
        self.ai_thinking = False

        self.difficulty = "Hard"

        self.buttons = []

        # ----------------------------------------------------
        # Main Layout
        # ----------------------------------------------------

        self.main = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        title = Label(
            text="TIC-TAC-TOE",
            font_size=32,
            bold=True,
            size_hint_y=0.10
        )

        self.main.add_widget(title)

        # ----------------------------------------------------
        # Score Board
        # ----------------------------------------------------

        score_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=0.10,
            spacing=5
        )

        self.wins_label = Label(
            text=f"Wins: {self.scores['wins']}",
            font_size=17
        )

        self.losses_label = Label(
            text=f"Losses: {self.scores['losses']}",
            font_size=17
        )

        self.draws_label = Label(
            text=f"Draws: {self.scores['draws']}",
            font_size=17
        )

        score_layout.add_widget(
            self.wins_label
        )

        score_layout.add_widget(
            self.losses_label
        )

        score_layout.add_widget(
            self.draws_label
        )

        self.main.add_widget(score_layout)

        # ----------------------------------------------------
        # Status
        # ----------------------------------------------------

        self.status = Label(
            text="Your turn - X",
            font_size=22,
            bold=True,
            size_hint_y=0.09
        )

        self.main.add_widget(self.status)

        # ----------------------------------------------------
        # Difficulty
        # ----------------------------------------------------

        difficulty_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=0.08,
            spacing=8
        )

        difficulty_label = Label(
            text="Difficulty:",
            font_size=18,
            size_hint_x=0.40
        )

        self.difficulty_spinner = Spinner(
            text="Hard",
            values=(
                "Easy",
                "Medium",
                "Hard"
            ),
            font_size=18,
            size_hint_x=0.60
        )

        self.difficulty_spinner.bind(
            text=self.change_difficulty
        )

        difficulty_layout.add_widget(
            difficulty_label
        )

        difficulty_layout.add_widget(
            self.difficulty_spinner
        )

        self.main.add_widget(
            difficulty_layout
        )

        # ----------------------------------------------------
        # Game Board
        # ----------------------------------------------------

        self.board_layout = GridLayout(
            cols=3,
            rows=3,
            spacing=7,
            size_hint_y=0.55
        )

        for index in range(9):

            button = Button(
                text="",
                font_size=50,
                bold=True,
                background_normal="",
                background_color=(
                    0.10,
                    0.12,
                    0.17,
                    1
                )
            )

            button.bind(
                on_press=lambda btn, i=index:
                self.player_move(i)
            )

            self.buttons.append(button)

            self.board_layout.add_widget(
                button
            )

        self.main.add_widget(
            self.board_layout
        )

        # ----------------------------------------------------
        # Buttons
        # ----------------------------------------------------

        control_layout = BoxLayout(
            orientation="horizontal",
            spacing=8,
            size_hint_y=0.10
        )

        new_game = Button(
            text="New Game",
            font_size=17
        )

        new_game.bind(
            on_press=self.new_game
        )

        reset_scores = Button(
            text="Reset Scores",
            font_size=17
        )

        reset_scores.bind(
            on_press=self.reset_scores
        )

        control_layout.add_widget(
            new_game
        )

        control_layout.add_widget(
            reset_scores
        )

        self.main.add_widget(
            control_layout
        )

        # ----------------------------------------------------
        # Start
        # ----------------------------------------------------

        self.new_game()

        return self.main

    # ========================================================
    # DIFFICULTY
    # ========================================================

    def change_difficulty(self, spinner, text):

        self.difficulty = text

        self.new_game()

    # ========================================================
    # PLAYER MOVE
    # ========================================================

    def player_move(self, index):

        if self.game_over:
            return

        if self.ai_thinking:
            return

        if self.board[index] != "":
            return

        self.make_move(
            index,
            "X"
        )

        result = self.check_game()

        if result:
            self.finish_game(result)
            return

        self.ai_thinking = True

        self.status.text = "AI is thinking..."

        # Small delay
        from kivy.clock import Clock

        Clock.schedule_once(
            self.ai_move,
            0.25
        )

    # ========================================================
    # MAKE MOVE
    # ========================================================

    def make_move(self, index, symbol):

        self.board[index] = symbol

        self.buttons[index].text = symbol

        if symbol == "X":

            self.buttons[index].background_color = (
                0.08,
                0.40,
                0.95,
                1
            )

        else:

            self.buttons[index].background_color = (
                0.95,
                0.12,
                0.20,
                1
            )

    # ========================================================
    # AI MOVE
    # ========================================================

    def ai_move(self, dt):

        if self.game_over:
            self.ai_thinking = False
            return

        move = self.get_ai_move()

        if move is not None:

            self.make_move(
                move,
                "O"
            )

        self.ai_thinking = False

        result = self.check_game()

        if result:

            self.finish_game(result)

        else:

            self.status.text = "Your turn - X"

    # ========================================================
    # AI DECISION
    # ========================================================

    def get_ai_move(self):

        empty = [
            i for i, value
            in enumerate(self.board)
            if value == ""
        ]

        if not empty:
            return None

        # ----------------------------------------------------
        # Easy
        # ----------------------------------------------------

        if self.difficulty == "Easy":

            return random.choice(empty)

        # ----------------------------------------------------
        # Medium
        # ----------------------------------------------------

        if self.difficulty == "Medium":

            # Try winning
            move = self.find_winning_move("O")

            if move is not None:
                return move

            # Block player
            move = self.find_winning_move("X")

            if move is not None:
                return move

            # Center
            if 4 in empty:
                return 4

            # Random
            return random.choice(empty)

        # ----------------------------------------------------
        # Hard
        # ----------------------------------------------------

        return self.minimax_best_move()

    # ========================================================
    # FIND WINNING MOVE
    # ========================================================

    def find_winning_move(self, symbol):

        for index in range(9):

            if self.board[index] == "":

                self.board[index] = symbol

                if self.winner(self.board) == symbol:

                    self.board[index] = ""

                    return index

                self.board[index] = ""

        return None

    # ========================================================
    # MINIMAX
    # ========================================================

    def minimax_best_move(self):

        best_score = -9999
        best_move = None

        for index in range(9):

            if self.board[index] == "":

                self.board[index] = "O"

                score = self.minimax(
                    self.board,
                    False
                )

                self.board[index] = ""

                if score > best_score:

                    best_score = score
                    best_move = index

        return best_move

    def minimax(self, board, maximizing):

        winner = self.winner(board)

        if winner == "O":
            return 10

        if winner == "X":
            return -10

        if "" not in board:
            return 0

        if maximizing:

            best_score = -9999

            for index in range(9):

                if board[index] == "":

                    board[index] = "O"

                    score = self.minimax(
                        board,
                        False
                    )

                    board[index] = ""

                    best_score = max(
                        best_score,
                        score
                    )

            return best_score

        else:

            best_score = 9999

            for index in range(9):

                if board[index] == "":

                    board[index] = "X"

                    score = self.minimax(
                        board,
                        True
                    )

                    board[index] = ""

                    best_score = min(
                        best_score,
                        score
                    )

            return best_score

    # ========================================================
    # CHECK GAME
    # ========================================================

    def check_game(self):

        winner = self.winner(
            self.board
        )

        if winner:
            return winner

        if "" not in self.board:
            return "Draw"

        return None

    # ========================================================
    # WINNER
    # ========================================================

    def winner(self, board):

        lines = [

            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),

            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),

            (0, 4, 8),
            (2, 4, 6)

        ]

        for a, b, c in lines:

            if (
                board[a] != "" and
                board[a] == board[b] and
                board[b] == board[c]
            ):

                return board[a]

        return None

    # ========================================================
    # FINISH GAME
    # ========================================================

    def finish_game(self, result):

        self.game_over = True

        if result == "X":

            self.scores["wins"] += 1

            self.status.text = "🏆 YOU WIN!"

            self.highlight_winner("X")

        elif result == "O":

            self.scores["losses"] += 1

            self.status.text = "🤖 AI WINS!"

            self.highlight_winner("O")

        else:

            self.scores["draws"] += 1

            self.status.text = "🤝 DRAW!"

        save_scores(
            self.scores
        )

        self.update_score_labels()

    # ========================================================
    # HIGHLIGHT WINNER
    # ========================================================

    def highlight_winner(self, symbol):

        lines = [

            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),

            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),

            (0, 4, 8),
            (2, 4, 6)

        ]

        for line in lines:

            a, b, c = line

            if (
                self.board[a] == symbol and
                self.board[b] == symbol and
                self.board[c] == symbol
            ):

                for index in line:

                    self.buttons[index].background_color = (
                        0.05,
                        0.80,
                        0.25,
                        1
                    )

                break

    # ========================================================
    # NEW GAME
    # ========================================================

    def new_game(self, *args):

        self.board = [""] * 9

        self.game_over = False

        self.ai_thinking = False

        for button in self.buttons:

            button.text = ""

            button.background_color = (
                0.10,
                0.12,
                0.17,
                1
            )

        self.status.text = "Your turn - X"

    # ========================================================
    # UPDATE SCORES
    # ========================================================

    def update_score_labels(self):

        self.wins_label.text = (
            f"Wins: {self.scores['wins']}"
        )

        self.losses_label.text = (
            f"Losses: {self.scores['losses']}"
        )

        self.draws_label.text = (
            f"Draws: {self.scores['draws']}"
        )

    # ========================================================
    # RESET SCORES
    # ========================================================

    def reset_scores(self, *args):

        self.show_reset_confirmation()

    # ========================================================
    # RESET CONFIRMATION
    # ========================================================

    def show_reset_confirmation(self):

        layout = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=15
        )

        message = Label(
            text="Are you sure you want to reset all scores?",
            font_size=18
        )

        buttons = BoxLayout(
            spacing=10
        )

        yes_button = Button(
            text="Yes",
            font_size=18
        )

        no_button = Button(
            text="Cancel",
            font_size=18
        )

        popup = Popup(
            title="Reset Scores",
            content=layout,
            size_hint=(0.85, 0.35),
            auto_dismiss=False
        )

        yes_button.bind(
            on_press=lambda x: self.confirm_reset(popup)
        )

        no_button.bind(
            on_press=popup.dismiss
        )

        buttons.add_widget(
            yes_button
        )

        buttons.add_widget(
            no_button
        )

        layout.add_widget(
            message
        )

        layout.add_widget(
            buttons
        )

        popup.open()

    # ========================================================
    # CONFIRM RESET
    # ========================================================

    def confirm_reset(self, popup):

        self.scores = {
            "wins": 0,
            "losses": 0,
            "draws": 0
        }

        save_scores(
            self.scores
        )

        self.update_score_labels()

        popup.dismiss()

        self.status.text = "Scores reset!"


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    TicTacToe().run()

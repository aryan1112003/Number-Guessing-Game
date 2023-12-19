import tkinter as tk
from tkinter import messagebox
import random
import time
import json
import tkinter.simpledialog
import secrets
import pyperclip

class NumberGuessingGame:
    def __init__(self, master):
        # Initialize attributes
        self.master = master
        self.master.title("Number Guessing Game")
        self.min_range = 1
        self.max_range = 100
        self.difficulty = tk.StringVar()
        self.difficulty.set("Normal")
        self.playing_with_friend = False
        self.time_limit = None
        self.show_secret_number = True

        # Styling
        self.background_color = "#000000"  # Background color
        self.text_color = "#ecf0f1"  # Text color
        self.button_color = "#2ecc71"  # Button color
        self.font = ("Helvetica", 12)

        # Header
        self.header_frame = tk.Frame(master, bg=self.background_color)
        self.header_frame.pack(pady=20)
        self.header_label = tk.Label(self.header_frame, text="Number Guessing Game", font=("Helvetica", 24, "bold"), bg=self.background_color, fg=self.text_color)
        self.header_label.pack()

        # Game State
        self.score_label = tk.Label(master, text="Score: 0", font=self.font, bg=self.background_color, fg=self.text_color)
        self.score_label.pack()

        self.history_label = tk.Label(master, text="History:", font=self.font, bg=self.background_color, fg=self.text_color)
        self.history_label.pack()

        self.timer_label = tk.Label(master, text="Time: 0s", font=self.font, bg=self.background_color, fg=self.text_color)
        self.timer_label.pack()

        self.reset_game()

        # Input and Buttons
        self.input_frame = tk.Frame(master, bg=self.background_color)
        self.input_frame.pack(pady=20)

        self.entry = tk.Entry(self.input_frame, font=self.font, width=10, bd=3)
        self.entry.pack(side=tk.LEFT, padx=10)

        # Improve button styling
        self.guess_button = tk.Button(self.input_frame, text="Guess", command=self.make_guess, font=self.font, bg=self.button_color, fg=self.text_color, padx=10, bd=5, relief=tk.RAISED)
        self.guess_button.pack(side=tk.LEFT, padx=(0, 10))

        self.reset_button = tk.Button(self.input_frame, text="Reset", command=self.reset_game, font=self.font, bg=self.button_color, fg=self.text_color, padx=10, bd=5, relief=tk.RAISED)
        self.reset_button.pack(side=tk.LEFT, padx=(0, 10))

        self.toggle_friend_button = tk.Button(self.input_frame, text="Play with Friend", command=self.toggle_friend_mode, font=self.font, bg=self.button_color, fg=self.text_color, padx=10, bd=5, relief=tk.RAISED)
        self.toggle_friend_button.pack(side=tk.LEFT)

        # Hint and Save/Load Buttons
        self.hint_button = tk.Button(master, text="Hint", command=self.provide_hint, font=self.font, bg=self.button_color, fg=self.text_color, pady=5, bd=5, relief=tk.RAISED)
        self.hint_button.pack(pady=10)

        self.save_button = tk.Button(master, text="Save Game", command=self.save_game, font=self.font, bg=self.button_color, fg=self.text_color, pady=5, bd=5, relief=tk.RAISED)
        self.save_button.pack()

        self.load_button = tk.Button(master, text="Load Game", command=self.load_game, font=self.font, bg=self.button_color, fg=self.text_color, pady=5, bd=5, relief=tk.RAISED)
        self.load_button.pack()

        # Number Line
        self.create_number_line()

        # Difficulty Dropdown
        self.difficulty_label = tk.Label(master, text="Difficulty:", font=self.font, bg=self.background_color, fg=self.text_color)
        self.difficulty_label.pack()
        self.difficulty_menu = tk.OptionMenu(master, self.difficulty, "Easy", "Normal", "Hard", command=self.change_difficulty)
        self.difficulty_menu.config(bg=self.button_color, fg=self.text_color)
        self.difficulty_menu.pack(pady=5)

        # Options
        self.options_frame = tk.Frame(master, bg=self.background_color)
        self.options_frame.pack()

        self.custom_range_button = tk.Button(self.options_frame, text="Custom Range", command=self.set_custom_range, font=self.font, bg=self.button_color, fg=self.text_color, padx=10)
        self.custom_range_button.pack(side=tk.LEFT)

        self.time_limit_button = tk.Button(self.options_frame, text="Set Time Limit", command=self.set_time_limit, font=self.font, bg=self.button_color, fg=self.text_color, padx=10)
        self.time_limit_button.pack(side=tk.LEFT)

        self.show_hide_button = tk.Button(self.options_frame, text="Show/Hide Number", command=self.toggle_show_hide_number, font=self.font, bg=self.button_color, fg=self.text_color, padx=10)
        self.show_hide_button.pack(side=tk.LEFT)
        
       # Unique code for friends
        self.player_code = None

        # Button to enter friend's code
        self.enter_code_button = tk.Button(self.input_frame, text="Enter Friend's Code", command=self.enter_friend_code,font=self.font, bg=self.button_color, fg=self.text_color, padx=10, bd=5, relief=tk.RAISED)
        self.enter_code_button.pack(side=tk.LEFT)

        # Button to copy the unique code to the clipboard
        self.copy_code_button = tk.Button(self.input_frame, text="Copy Code", command=self.copy_player_code,font=self.font, bg=self.button_color, fg=self.text_color, padx=10, bd=5, relief=tk.RAISED)
        self.copy_code_button.pack(side=tk.LEFT)

    def create_number_line(self):
        canvas_width = 400
        canvas_height = 30
        self.number_line_canvas = tk.Canvas(self.master, width=canvas_width, height=canvas_height, bg=self.background_color)
        self.number_line_canvas.pack()

        line_start = 10
        line_end = canvas_width - 10

        self.number_line_canvas.create_line(line_start, canvas_height // 2, line_end, canvas_height // 2, width=2, fill=self.text_color)
        self.number_line_canvas.create_text(line_start, canvas_height // 2 + 15, anchor=tk.W, text=str(self.min_range), font=self.font, fill=self.text_color)
        self.number_line_canvas.create_text(line_end, canvas_height // 2 + 15, anchor=tk.E, text=str(self.max_range), font=self.font, fill=self.text_color)

    def reset_game(self):
        self.secret_number = random.randint(self.min_range, self.max_range)
        self.attempts = 0
        self.max_attempts = self.get_max_attempts()
        self.guess_history = []
        self.start_time = time.time()
        self.update_score_label()
        self.update_history_label()
        self.update_timer()

    def make_guess(self):
        try:
            guess = int(self.entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number.")
            return

        self.attempts += 1
        feedback = self.evaluate_guess(guess)
        self.guess_history.append((guess, feedback))

        if feedback == "Correct!":
            elapsed_time = time.time() - self.start_time
            self.display_congratulatory_message(elapsed_time)
            self.update_score_label()
            self.reset_game()
        elif self.attempts == self.max_attempts:
            messagebox.showinfo("Game Over", f"Sorry, you've run out of attempts. The correct number was {self.secret_number}.")
            self.update_score_label()
            self.reset_game()
        else:
            self.update_history_label()
            self.update_timer()

    def evaluate_guess(self, guess):
        if guess == self.secret_number:
            return "Correct!"
        elif guess < self.secret_number:
            return "Too low. Try again."
        else:
            return "Too high. Try again."

    def update_score_label(self):
        self.score_label.config(text=f"Score: {self.calculate_score()}")

    def update_history_label(self):
        history_text = "\n".join([f"Attempt {i + 1}: {guess} - {feedback}" for i, (guess, feedback) in enumerate(self.guess_history)])
        self.history_label.config(text=f"History:\n{history_text}")

    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        self.timer_label.config(text=f"Time: {elapsed_time:.2f}s")
        self.master.after(100, self.update_timer)  # Update every 100 milliseconds

    def calculate_score(self):
        return max(0, 100 - self.attempts * 10)

    def get_max_attempts(self):
        difficulty_levels = {"Easy": 15, "Normal": 10, "Hard": 5}
        return difficulty_levels.get(self.difficulty.get(), 10)

    def change_difficulty(self, *args):
        self.max_attempts = self.get_max_attempts()

    def set_custom_range(self):
        try:
            range_str = messagebox.askstring("Custom Range", "Enter custom range (e.g., 10-100):")
            min_val, max_val = map(int, range_str.split('-'))
            if min_val < max_val:
                self.min_range = min_val
                self.max_range = max_val
                self.reset_game()
                self.create_number_line()
            else:
                messagebox.showerror("Error", "Invalid range. Please enter a valid number range.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number range.")

    def set_time_limit(self):
        try:
            time_limit_str = messagebox.askstring("Set Time Limit", "Enter time limit for each guess (in seconds):")
            self.time_limit = int(time_limit_str)
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Invalid input. Please enter a valid time limit (in seconds).")

    def toggle_show_hide_number(self):
        self.show_secret_number = not self.show_secret_number
        if self.show_secret_number:
            messagebox.showinfo("Show Number", f"The secret number is: {self.secret_number}")
        else:
            messagebox.showinfo("Hide Number", "The secret number is hidden.")

    def provide_hint(self):
        midpoint = (self.min_range + self.max_range) // 2
        messagebox.showinfo("Hint", f"The number is around {midpoint}.")

    def display_congratulatory_message(self, elapsed_time):
        score = self.calculate_score()
        if score > 80:
            messagebox.showinfo("Congratulations!", f"Wow! You're a master guesser!\nYour score: {score}\nTime: {elapsed_time:.2f}s")
        elif score > 50:
            messagebox.showinfo("Congratulations!", f"Good job! You've got the talent!\nYour score: {score}\nTime: {elapsed_time:.2f}s")
        elif score > 20:
            messagebox.showinfo("Congratulations!", f"Not bad! Keep practicing!\nYour score: {score}\nTime: {elapsed_time:.2f}s")
        else:
            messagebox.showinfo("Congratulations!", f"You can do better! Try again!\nYour score: {score}\nTime: {elapsed_time:.2f}s")

    def save_game(self):
        game_state = {
            "min_range": self.min_range,
            "max_range": self.max_range,
            "difficulty": self.difficulty.get(),
            "playing_with_friend": self.playing_with_friend,
            "time_limit": self.time_limit,
            "show_secret_number": self.show_secret_number,
            "secret_number": self.secret_number,
            "attempts": self.attempts,
            "max_attempts": self.max_attempts,
            "guess_history": self.guess_history,
            "start_time": self.start_time
        }

        with open("game_state.json", "w") as file:
            json.dump(game_state, file)

        messagebox.showinfo("Save Game", "Game state saved successfully.")

    def load_game(self):
        try:
            with open("game_state.json", "r") as file:
                game_state = json.load(file)

            self.min_range = game_state["min_range"]
            self.max_range = game_state["max_range"]
            self.difficulty.set(game_state["difficulty"])
            self.playing_with_friend = game_state["playing_with_friend"]
            self.time_limit = game_state.get("time_limit")
            self.show_secret_number = game_state["show_secret_number"]
            self.secret_number = game_state["secret_number"]
            self.attempts = game_state["attempts"]
            self.max_attempts = game_state["max_attempts"]
            self.guess_history = game_state["guess_history"]
            self.start_time = game_state["start_time"]

            self.update_score_label()
            self.update_history_label()
            self.update_timer()
            self.create_number_line()

            if self.show_secret_number:
                messagebox.showinfo("Show Number", f"The secret number is: {self.secret_number}")
            else:
                messagebox.showinfo("Hide Number", "The secret number is hidden.")

            messagebox.showinfo("Load Game", "Game state loaded successfully.")
        except FileNotFoundError:
            messagebox.showerror("Load Game", "No saved game state found.")

    def toggle_friend_mode(self):
        if not self.playing_with_friend:
            # Generate a unique player code
            self.player_code = secrets.token_hex(4)
            messagebox.showinfo("Your Friend's Code", f"Your friend's code is: {self.player_code}\nShare this code with your friend.")
            self.playing_with_friend = True
            messagebox.showinfo("Friend Mode", "Friend Mode enabled. Take turns guessing with your friend.")
        else:
            self.playing_with_friend = False
            messagebox.showinfo("Friend Mode", "Friend Mode disabled.")

    def enter_friend_code(self):
        if self.playing_with_friend:
            friend_code = tkinter.simpledialog.askstring("Enter Friend's Code", "Enter your friend's code:")
            if friend_code == self.player_code:
                messagebox.showinfo("Friend Mode", "Friend code accepted. Enjoy the game with your friend!")
            else:
                messagebox.showerror("Friend Mode", "Invalid friend code. Please enter the correct code.")

    def copy_player_code(self):
        if self.player_code:
            pyperclip.copy(self.player_code)
            messagebox.showinfo("Copy Code", "Friend code copied to clipboard.")
        else:
            messagebox.showwarning("Copy Code", "No friend code available. Generate a code first.")
def main():
    root = tk.Tk()
    app = NumberGuessingGame(root)
    root.configure(bg="#000000")  # Set background color
    root.geometry("600x500")
    root.resizable(False, False)
    root.mainloop()

if __name__ == "__main__":
    main()

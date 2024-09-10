import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import re
import os

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
RAT_MOVE_INCREMENT = 50
MAX_QUESTIONS = 10
HIGH_SCORE_FILE = "high_score.txt"

class MathsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Flow Computing")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        # Load and prepare images
        self.background_image = Image.open("background.jpg")
        self.rat_image = Image.open("runningrat.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image.resize((WINDOW_WIDTH, WINDOW_HEIGHT)))
        self.rat_photo = ImageTk.PhotoImage(self.rat_image.resize((100, 100)))

        # Create canvas for game visuals
        self.canvas = tk.Canvas(self.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.canvas.pack(fill="both", expand=True)

        # Initialize the game setup
        self.setup_name_entry()

    def setup_name_entry(self):
        """Set up the name entry screen."""
        self.name_entry_frame = tk.Frame(self.root, bg='lightblue')
        self.name_entry_frame.place(relwidth=1, relheight=1)

        # Label for entering name
        tk.Label(self.name_entry_frame, text="Enter Your Name:", font=("Arial", 18), bg='lightpink').pack(pady=20)
        
        # Additional label for the game objective
        tk.Label(self.name_entry_frame, text="Help the rat escape!", font=("Arial", 14), bg='lightpink').pack(pady=10)

        # Name entry field
        self.name_entry = tk.Entry(self.name_entry_frame, font=("Arial", 16))
        self.name_entry.pack(pady=10)

        # Submit button
        tk.Button(self.name_entry_frame, text="Submit", font=("Arial", 16), command=self.handle_name_entry).pack(pady=20)
        
        # Add quit button
        self.add_quit_button()

    def handle_name_entry(self):
        """Handle user name entry and validate."""
        self.user_name = self.name_entry.get().strip()

        if not self.user_name or len(self.user_name) > 15 or not re.match("^[A-Za-z0-9_]*$", self.user_name):
            messagebox.showerror("Invalid Name", "Name must be 1-15 characters long and contain only letters, numbers, or underscores.")
        else:
            self.name_entry_frame.destroy()
            self.setup_difficulty_buttons()

    def setup_difficulty_buttons(self):
        """Create difficulty selection buttons."""
        self.button_frame = tk.Frame(self.root, bg='lightblue')
        self.button_frame.place(relwidth=1, relheight=1)

        tk.Label(self.button_frame, text="Select Difficulty Level:", font=("Arial", 18), bg='lightpink').pack(pady=20)

        easy_button = tk.Button(self.button_frame, text="Easy (Addition & Subtraction)", font=("Arial", 16), width=30, height=2, command=lambda: self.start_game("easy"))
        easy_button.pack(pady=10)

        regular_button = tk.Button(self.button_frame, text="Regular (Multiplication)", font=("Arial", 16), width=30, height=2, command=lambda: self.start_game("regular"))
        regular_button.pack(pady=10)

        difficult_button = tk.Button(self.button_frame, text="Difficult (Division)", font=("Arial", 16), width=30, height=2, command=lambda: self.start_game("difficult"))
        difficult_button.pack(pady=10)

        self.add_quit_button()

    def start_game(self, difficulty):
        """Initialize and start the game based on selected difficulty."""
        self.difficulty = difficulty
        self.question_count = 0
        self.correct_answers = 0
        self.score = 0
        self.rat_x_position = 50
        self.rat_item = None

        self.button_frame.destroy()

        # Set background image for the game
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_photo)

        # Create score label
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Arial", 14), bg='white')
        self.score_label.place(x=10, y=10)

        # Create question label and answer buttons
        self.question_label = tk.Label(self.root, text="", font=("Arial", 18), bg='lightpink')
        self.question_label.place(x=300, y=100)

        self.answer_buttons = []
        for i in range(4):
            button = tk.Button(self.root, text="", font=("Arial", 16), width=10, height=2, bg="lightblue")
            button.place(x=300 + (i % 2) * 150, y=300 + (i // 2) * 100)
            self.answer_buttons.append(button)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 14), bg='lightblue')
        self.result_label.place(x=350, y=450)

        self.add_quit_button()

        # Generate the first question
        self.generate_question()

    def generate_question(self):
        """Generate and display a random math question."""
        self.question_count += 1

        if self.question_count <= MAX_QUESTIONS:
            question_types = {
                "easy": ["addition", "subtraction"],
                "regular": ["multiplication"],
                "difficult": ["division"]
            }

            question_type = random.choice(question_types[self.difficulty])

            if question_type == "multiplication":
                num1 = random.randint(1, 12)
                num2 = random.randint(1, 12)
                self.correct_answer = num1 * num2
                question = f"{num1} x {num2} = ?"

            elif question_type == "division":
                num1 = random.randint(1, 12)
                num2 = random.randint(1, 12)
                self.correct_answer = num1 * num2
                question = f"{self.correct_answer} ÷ {num1} = ?"
                self.correct_answer = num2

            elif question_type == "addition":
                num1 = random.randint(1, 50)
                num2 = random.randint(1, 50)
                self.correct_answer = num1 + num2
                question = f"{num1} + {num2} = ?"

            elif question_type == "subtraction":
                num1 = random.randint(1, 50)
                num2 = random.randint(1, 50)
                if num1 < num2:
                    num1, num2 = num2, num1
                self.correct_answer = num1 - num2
                question = f"{num1} - {num2} = ?"

            self.question_label.config(text=question)

            # Randomize answer button positions
            correct_pos = random.randint(0, 3)
            self.answer_buttons[correct_pos].config(text=str(self.correct_answer), command=lambda: self.check_answer(self.correct_answer))

            for i, btn in enumerate(self.answer_buttons):
                if i != correct_pos:
                    incorrect_answer = self.correct_answer + random.randint(-10, 10)
                    btn.config(text=str(incorrect_answer), command=lambda btn_text=btn.cget("text"): self.check_answer(int(btn_text)))

        else:
            self.end_game()

    def check_answer(self, selected_answer):
        """Check if the selected answer is correct and update the score."""
        if selected_answer == self.correct_answer:
            self.result_label.config(text="Correct!", fg="green")
            self.update_score(True)
        else:
            self.result_label.config(text="Incorrect", fg="red")
            self.update_score(False)

        # Move to the next question
        if self.question_count < MAX_QUESTIONS:
            self.root.after(1000, self.generate_question)
        else:
            self.root.after(1000, self.end_game)

    def update_score(self, is_correct):
        """Update score and move the rat if the answer is correct."""
        if is_correct:
            self.score += 100
            self.correct_answers += 1
            self.move_rat()
        self.score_label.config(text=f"Score: {self.score}")

    def move_rat(self):
        """Animate the rat moving across the screen."""
        if self.rat_item:
            self.canvas.delete(self.rat_item)
        self.rat_x_position += RAT_MOVE_INCREMENT
        if self.rat_x_position < WINDOW_WIDTH - 50:
            self.rat_item = self.canvas.create_image(self.rat_x_position, 400, anchor="nw", image=self.rat_photo)
        else:
            self.rat_item = None

    def save_high_score(self):
        """Save the current score if it's a high score."""
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, "r") as file:
                high_score = int(file.read().strip())
        else:
            high_score = 0

        if self.score > high_score:
            with open(HIGH_SCORE_FILE, "w") as file:
                file.write(str(self.score))

    def read_high_score(self):
        """Read the high score from the file."""
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, "r") as file:
                return int(file.read().strip())
        return 0

    def end_game(self):
        """Display the final score and game over message, and save the high score."""
        self.save_high_score()
        high_score = self.read_high_score()

        if self.correct_answers >= 9:
            messagebox.showinfo("Game Over", f"Congratulations! You scored {self.score}. The rat has escaped!")
        else:
            messagebox.showinfo("Game Over", f"Game Over! You scored {self.score}. Try again!")

        self.root.after(2000, self.setup_name_entry)

if __name__ == "__main__":
    root = tk.Tk()
    game = MathsGame(root)
    root.mainloop()

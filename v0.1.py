import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import re
import os

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

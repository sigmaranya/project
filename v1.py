import tkinter as tk
import random

class MathGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Math Game")
        
        self.score = 0
        self.question_count = 0
        self.rat_speed = 1
        
        self.label_question = tk.Label(self.master, text="Question")
        self.label_question.pack()
        
        self.entry_answer = tk.Entry(self.master)
        self.entry_answer.pack()
        
        self.button_check = tk.Button(self.master, text="Check Answer", command=self.check_answer)
        self.button_check.pack()
        
        self.label_feedback = tk.Label(self.master, text="")
        self.label_feedback.pack()
        
        self.label_score = tk.Label(self.master, text="Score: 0")
        self.label_score.pack()
        
        self.generate_question()
    
    def generate_question(self):
        # Generate random question
        num1 = random.randint(0, 100)
        num2 = random.randint(0, 100)
        
        operation = random.choice(['+', '-', '*', '/'])
        if operation == '+':
            self.answer = num1 + num2
            question_text = f"{num1} + {num2} = ?"
        elif operation == '-':
            self.answer = num1 - num2
            question_text = f"{num1} - {num2} = ?"
        elif operation == '*':
            self.answer = num1 * num2
            question_text = f"{num1} * {num2} = ?"
        elif operation == '/':
            if num2 == 0:
                num2 = 1  # Avoid division by zero
            self.answer = num1 // num2  # Integer division
            question_text = f"{num1} / {num2} = ?"
        
        self.label_question.config(text=question_text)
    
    def check_answer(self):
        user_answer = self.entry_answer.get()
        try:
            user_answer = int(user_answer)
            if user_answer == self.answer:
                self.score += 100
                self.label_feedback.config(text="Correct!")
                self.rat_speed += 1
            else:
                self.label_feedback.config(text="Incorrect!")
        except ValueError:
            self.label_feedback.config(text="Please enter a number!")
        
        self.question_count += 1
        self.label_score.config(text=f"Score: {self.score}")
        
        if self.question_count < 12:
            self.generate_question()
        else:
            self.end_game()
    
    def end_game(self):
        # Display final score and end game logic
        self.label_question.config(text="Game Over")
        self.label_feedback.config(text=f"Final Score: {self.score}")
        self.button_check.config(state=tk.DISABLED)

# Create the main Tkinter window
root = tk.Tk()
math_game = MathGame(root)
root.mainloop()

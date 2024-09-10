import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# Create main application window
root = tk.Tk()
root.title("Maths Game")
root.geometry("800x600")  # Adjusting the window size for better layout

# Initialize game variables
questions = []
current_question_index = 0
score = 0

# Create a Canvas to add the background image
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)

# Load and set the background image
background_img = Image.open("background.jpg")  # Replace with the correct path
background_img = background_img.resize((800, 600), Image.ANTIALIAS)
bg_image = ImageTk.PhotoImage(background_img)
canvas.create_image(0, 0, image=bg_image, anchor="nw")

# Load animated image for score increase (optional)
animated_img = Image.open("runningrat.png")  # Replace with your animated image path
animated_img = animated_img.resize((50, 50), Image.ANTIALIAS)
char_image = ImageTk.PhotoImage(animated_img)
char_id = canvas.create_image(-50, 550, image=char_image, anchor="nw")  # Starts outside the canvas

# Function to generate random questions
def generate_questions():
    global questions
    for i in range(10):
        question_type = random.choice(["multiplication", "division", "addition", "subtraction"])
        
        if question_type == "multiplication":
            num1 = random.randint(1, 12)
            num2 = random.randint(1, 12)
            question = f"What is {num1} x {num2}?"
            correct_answer = num1 * num2
        
        elif question_type == "division":
            num1 = random.randint(1, 12)
            num2 = random.randint(1, 12)
            dividend = num1 * num2  # Ensures the division has no remainder
            question = f"What is {dividend} ÷ {num1}?"
            correct_answer = dividend // num1
        
        elif question_type == "addition":
            num1 = random.randint(1, 50)
            num2 = random.randint(1, 50)
            question = f"What is {num1} + {num2}?"
            correct_answer = num1 + num2
        
        else:  # subtraction
            num1 = random.randint(20, 100)
            num2 = random.randint(1, 20)
            question = f"What is {num1} - {num2}?"
            correct_answer = num1 - num2

        # Generate 3 incorrect answers
        answers = [correct_answer]
        while len(answers) < 4:
            wrong_answer = correct_answer + random.randint(-10, 10)
            if wrong_answer != correct_answer and wrong_answer not in answers:
                answers.append(wrong_answer)

        random.shuffle(answers)
        questions.append((question, correct_answer, answers))

# Function to update the score label
def update_score():
    score_label.config(text=f"Score: {score}")

# Function to move the animated image when the score increases
def move_animated_image():
    global char_id
    for _ in range(50):
        canvas.move(char_id, 10, 0)  # Moves the image 10 pixels to the right
        root.update()
        root.after(50)

# Function to check the user's answer
def check_answer(selected_answer, correct_answer):
    global score
    if selected_answer == correct_answer:
        feedback_label.config(text="Correct! ✓", fg="green")
        score += 100
        move_animated_image()  # Move the image when the user gets a correct answer
    else:
        feedback_label.config(text="Incorrect! ✗", fg="red")
    update_score()
    next_question()

# Function to display the next question
def next_question():
    global current_question_index
    if current_question_index < 10:
        question, correct_answer, answers = questions[current_question_index]
        question_label.config(text=question)
        for i, answer in enumerate(answers):
            option_buttons[i].config(text=str(answer), command=lambda a=answer: check_answer(a, correct_answer))
        current_question_index += 1
    else:
        messagebox.showinfo("Quiz Finished", f"Your final score is {score} out of 1000")
        root.quit()

# GUI Elements
question_label = tk.Label(root, text="", font=("Arial", 16), bg="lightblue")
canvas.create_window(600, 450, window=question_label)  # Place question label in bottom right corner

# Creating a frame to hold the answer buttons in a 2x2 grid
button_frame = tk.Frame(root, bg="lightblue")
canvas.create_window(600, 500, window=button_frame)

option_buttons = [tk.Button(button_frame, text="", width=15, height=3, font=("Arial", 14)) for _ in range(4)]
for i in range(2):
    for j in range(2):
        option_buttons[i*2+j].grid(row=i, column=j, padx=5, pady=5)

# Feedback label for displaying correct or incorrect answer
feedback_label = tk.Label(root, text="", font=("Arial", 14), bg="lightblue")
canvas.create_window(600, 350, window=feedback_label)

# Score label
score_label = tk.Label(root, text=f"Score: {score}", font=("Arial", 14), bg="lightblue")
canvas.create_window(600, 100, window=score_label)

# Generate random questions and start the quiz
generate_questions()
next_question()

# Start the main event loop
root.mainloop()

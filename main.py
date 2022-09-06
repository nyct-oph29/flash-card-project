from tkinter import *
import pandas as pd
import random
BACKGROUND_COLOR = "#B1DDC6"
current_word = {}
try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original = pd.read_csv("data/french_words.csv")
    vocab = original.to_dict("records")
else:
    vocab = data.to_dict("records")

# ----------------- Change Word -------------------


def next_card():
    global current_word
    try:
        current_word = random.choice(vocab)
    except IndexError:
        canvas.itemconfig(language, text="Good Job", fill="black")
        canvas.itemconfig(word, text="You have memorized the words", fill="black")
        canvas.itemconfig(image, image=WHITE_FLASH)
    else:
        canvas.itemconfig(language, text="French", fill="black")
        canvas.itemconfig(word, text=current_word["French"], fill="black")
        canvas.itemconfig(image, image=WHITE_FLASH)
        timer = window.after(3000, check_answer)


def check_answer():
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(word, text=current_word["English"], fill="white")
    canvas.itemconfig(image, image=GREEN_FLASH)


def is_correct():
    try:
        vocab.remove(current_word)
    except ValueError:
        next_card()
    else:
        unlearnt_data = pd.DataFrame(vocab)
        unlearnt_data.to_csv("data/words_to_learn.csv")
        next_card()
# ----------------- UI Setup ----------------------


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
WHITE_FLASH = PhotoImage(file="images/card_front.png")
GREEN_FLASH = PhotoImage(file="images/card_back.png")
RIGHT = PhotoImage(file="images/right.png")
WRONG = PhotoImage(file="images/wrong.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
image = canvas.create_image(400, 263, image=WHITE_FLASH)
canvas.grid(column=0, row=0, columnspan=2)
language = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"), fill="black")
word = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"), fill="black")

right = Button(image=RIGHT, highlightthickness=0, command=is_correct)
right.grid(column=1, row=1)

wrong = Button(image=WRONG, highlightthickness=0, command=next_card)
wrong.grid(column=0, row=1)
next_card()

window.mainloop()

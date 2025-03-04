# import random

# print("Hi welcome to the game, This is a number guessing game.\nYou got 7 chances to guess the number. Let's start the game")

# number_to_guess = random.randrange(100)

# chances = 7

# guess_counter = 0

# while guess_counter < chances:

#     guess_counter += 1
#     my_guess = int(input('Please Enter your Guess : '))

#     if my_guess == number_to_guess:
#         print(f'The number is {number_to_guess} and you found it right !! in the {guess_counter} attempt')
#         break

#     elif guess_counter >= chances and my_guess != number_to_guess:
#         print(f'Oops sorry, The number is {number_to_guess} better luck next time')

#     elif my_guess > number_to_guess:
#         print('Your guess is higher ')

#     elif my_guess < number_to_guess:
#         print('Your guess is lesser')


import tkinter as tk
from tkinter import messagebox
import random

# List of words
WORDS = ['python', 'hangman', 'developer', 'interface', 'programming', 'challenge', 'function']

# Hangman stages
HANGMAN_PICS = [
    """\n +---+\n     |\n     |\n     |\n    ===\n""",
    """\n +---+\n O   |\n     |\n     |\n    ===\n""",
    """\n +---+\n O   |\n |   |\n     |\n    ===\n""",
    """\n +---+\n O   |\n/|   |\n     |\n    ===\n""",
    """\n +---+\n O   |\n/|\  |\n     |\n    ===\n""",
    """\n +---+\n O   |\n/|\  |\n/    |\n    ===\n""",
    """\n +---+\n O   |\n/|\  |\n/ \  |\n    ===\n"""
]

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        
        self.word = random.choice(WORDS)
        self.guessed_word = ['_'] * len(self.word)
        self.attempts = 0
        self.max_attempts = len(HANGMAN_PICS) - 1
        self.guessed_letters = set()
        
        # Hangman Canvas
        self.hangman_label = tk.Label(root, text=HANGMAN_PICS[self.attempts], font=("Courier", 14))
        self.hangman_label.pack()
        
        # Word Display
        self.word_label = tk.Label(root, text=' '.join(self.guessed_word), font=("Arial", 20))
        self.word_label.pack()
        
        # Letter Entry
        self.entry = tk.Entry(root, font=("Arial", 16))
        self.entry.pack()
        self.entry.bind("<Return>", self.make_guess)
        
        # Guess Button
        self.guess_button = tk.Button(root, text="Guess", command=self.make_guess, font=("Arial", 16))
        self.guess_button.pack()
        
    def make_guess(self, event=None):
        letter = self.entry.get().lower()
        self.entry.delete(0, tk.END)
        
        if not letter or len(letter) != 1 or not letter.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a single letter.")
            return
        
        if letter in self.guessed_letters:
            messagebox.showinfo("Already Guessed", f"You already guessed '{letter}'.")
            return
        
        self.guessed_letters.add(letter)
        
        if letter in self.word:
            for i, char in enumerate(self.word):
                if char == letter:
                    self.guessed_word[i] = letter
        else:
            self.attempts += 1
        
        self.hangman_label.config(text=HANGMAN_PICS[self.attempts])
        self.word_label.config(text=' '.join(self.guessed_word))
        
        if '_' not in self.guessed_word:
            messagebox.showinfo("Congratulations!", f"You won! The word was '{self.word}'.")
            self.root.quit()
        elif self.attempts == self.max_attempts:
            messagebox.showerror("Game Over", f"You lost! The word was '{self.word}'.")
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()

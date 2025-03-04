import random

# -------------------------------------------------------------------
# Sudoku Game
# -------------------------------------------------------------------

def generate_sudoku(difficulty="easy"):
    """Generates a Sudoku puzzle."""
    # This is a simplified generator.  A real Sudoku generator is much more complex.
    # For this example, we'll just use a pre-defined board and remove some numbers
    # based on the difficulty level.

    board = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ]

    num_to_remove = 0
    if difficulty == "easy":
        num_to_remove = 40
    elif difficulty == "medium":
        num_to_remove = 50
    elif difficulty == "hard":
        num_to_remove = 60

    puzzle = [row[:] for row in board]  # Create a copy of the board

    for _ in range(num_to_remove):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        puzzle[row][col] = 0  # Represent empty cells with 0

    return puzzle

def print_sudoku(board):
    """Prints the Sudoku board in a user-friendly format."""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")

        for j in range(9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

def is_valid_move(board, row, col, num):
    """Checks if a move is valid according to Sudoku rules."""

    # Check row
    for i in range(9):
        if board[row][i] == num:
            return False

    # Check column
    for i in range(9):
        if board[i][col] == num:
            return False

    # Check 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False

    return True

def solve_sudoku(board):
    """Solves a Sudoku puzzle using backtracking."""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid_move(board, row, col, num):
                        board[row][col] = num

                        if solve_sudoku(board):  # Recursive call
                            return True
                        else:
                            board[row][col] = 0  # Backtrack

                return False  # No solution found

    return True  # Puzzle is solved


def play_sudoku():
    """Plays a game of Sudoku."""
    difficulty = input("Choose difficulty (easy, medium, hard): ").lower()
    puzzle = generate_sudoku(difficulty)
    original_puzzle = [row[:] for row in puzzle] # Store the original puzzle

    print("Sudoku Puzzle:")
    print_sudoku(puzzle)

    while True:
        try:
            row = int(input("Enter row (1-9): ")) - 1
            col = int(input("Enter column (1-9): ")) - 1
            num = int(input("Enter number (1-9): "))

            if not (0 <= row < 9 and 0 <= col < 9 and 1 <= num <= 9):
                print("Invalid input. Row and column must be between 1 and 9, number between 1 and 9.")
                continue

            if original_puzzle[row][col] != 0:
                 print("You can't change this cell because it was already filled.")
                 continue

            if puzzle[row][col] != 0: # Check if the cell is already filled
                print("That cell is already filled. Please choose an empty cell.")
                continue


            if is_valid_move(puzzle, row, col, num):
                puzzle[row][col] = num
                print_sudoku(puzzle)

                # Check if the puzzle is solved
                solved_board = [row[:] for row in puzzle] # Create a copy
                if solve_sudoku(solved_board):
                    is_complete = True
                    for r in range(9):
                        for c in range(9):
                            if puzzle[r][c] == 0:
                                is_complete = False
                                break
                        if not is_complete:
                            break

                    if is_complete:
                        print("Congratulations! You solved the Sudoku puzzle!")
                        break


                else:
                    print("That move creates an invalid puzzle, although it looked fine for this cell.")
                    puzzle[row][col] = 0 # Undo the move


            else:
                print("Invalid move. That number already exists in the row, column, or 3x3 box.")

        except ValueError:
            print("Invalid input. Please enter numbers only.")


# -------------------------------------------------------------------
# Hangman Game
# -------------------------------------------------------------------

def choose_word():
    """Chooses a random word from a list."""
    words = ["python", "programming", "computer", "algorithm", "function", "variable"]
    return random.choice(words)

def display_word(word, guessed_letters):
    """Displays the word with correctly guessed letters and underscores for unguessed letters."""
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter
        else:
            display += "_"
    return display

def play_hangman():
    """Plays a game of Hangman."""
    word_to_guess = choose_word()
    guessed_letters = []
    tries_left = 6
    word_display = display_word(word_to_guess, guessed_letters)

    print("Welcome to Hangman!")
    print(word_display)

    while tries_left > 0 and "_" in word_display:
        guess = input("Guess a letter: ").lower()

        if not guess.isalpha() or len(guess) != 1:
            print("Invalid input. Please enter a single letter.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue

        guessed_letters.append(guess)

        if guess in word_to_guess:
            print("Correct guess!")
            word_display = display_word(word_to_guess, guessed_letters)
            print(word_display)
        else:
            tries_left -= 1
            print(f"Incorrect guess. You have {tries_left} tries left.")

        if tries_left == 0:
            print(f"You ran out of tries. The word was {word_to_guess}.")
        elif "_" not in word_display:
            print("Congratulations! You guessed the word!")

# -------------------------------------------------------------------
# Main Game Menu
# -------------------------------------------------------------------

def main_menu():
    """Presents a menu to choose a game."""
    while True:
        print("\nChoose a game:")
        print("1. Sudoku")
        print("2. Hangman")
        print("3. Quit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            play_sudoku()
        elif choice == "2":
            play_hangman()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

if __name__ == "__main__":
    main_menu()

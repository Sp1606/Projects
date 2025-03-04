import random

class Sudoku:
    def __init__(self, difficulty="Easy"):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.difficulty = difficulty
        self.generate_full_board()
        self.create_puzzle()

    def generate_full_board(self):
        """Generates a complete, valid Sudoku board using backtracking."""
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.solve(0, 0)  # Fill solution board

    def solve(self, row, col):
        """Backtracking Sudoku solver."""
        if row == 9:
            return True

        next_row, next_col = (row, col + 1) if col < 8 else (row + 1, 0)

        if self.solution[row][col] != 0:
            return self.solve(next_row, next_col)

        numbers = list(range(1, 10))
        random.shuffle(numbers)

        for num in numbers:
            if self.is_valid(row, col, num):
                self.solution[row][col] = num
                if self.solve(next_row, next_col):
                    return True
                self.solution[row][col] = 0

        return False

    def is_valid(self, row, col, num):
        """Checks if placing num at (row, col) is valid."""
        for i in range(9):
            if self.solution[row][i] == num or self.solution[i][col] == num:
                return False

        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.solution[box_row + i][box_col + j] == num:
                    return False

        return True

    def create_puzzle(self):
        """Removes numbers based on difficulty to create a puzzle."""
        self.board = [row[:] for row in self.solution]
        difficulty_levels = {
            "Easy": random.randint(20, 30),
            "Not So Easy": random.randint(31, 40),
            "A Bit Hard": random.randint(41, 50),
            "Hard": random.randint(51, 60)
        }
        blanks = difficulty_levels.get(self.difficulty, 30)  # Default to Easy

        while blanks > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                blanks -= 1

    def print_board(self):
        """Prints the Sudoku board."""
        for row in self.board:
            print(row)

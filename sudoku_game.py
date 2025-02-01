import random
import pygame
import sys

class Sudoku:
    def __init__(self, difficulty="Easy"):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.difficulty = difficulty
        self.generate_full_board()
        self.create_puzzle()
        self.original_board = [row[:] for row in self.board]
        self.total_cells = sum(1 for row in self.original_board for num in row if num != 0)
        self.correct_moves = 0
        self.wrong_moves = 0
        self.hints_used = 0  # Track hints used

    def generate_full_board(self):
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.solve(0, 0)

    def solve(self, row, col):
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
        self.board = [row[:] for row in self.solution]
        difficulty_levels = {
            "Easy": random.randint(20, 30),
            "Not So Easy": random.randint(31, 40),
            "A Bit Hard": random.randint(41, 50),
            "Hard": random.randint(51, 60)
        }
        blanks = difficulty_levels.get(self.difficulty, 30)
        while blanks > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                blanks -= 1

    def get_hint(self):
        """ Returns a random empty cell with its correct value from the solution. """
        empty_cells = [(r, c) for r in range(9) for c in range(9) if self.board[r][c] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)  # Pick a random empty cell
            return row, col, self.solution[row][col]
        return None

pygame.init()
WIDTH, HEIGHT = 540, 600
GRID_SIZE = 60
WHITE, BLACK, GREY, BLUE, RED = (255,255,255), (0,0,0), (200,200,200), (0,0,255), (255,0,0)
FONT = pygame.font.Font(None, 40)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Game")
game = None

def draw_text(text, pos, color=BLACK):
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, pos)

def select_difficulty():
    global game
    selecting = True
    while selecting:
        screen.fill(WHITE)
        draw_text("Select Difficulty:", (160, 100))
        draw_text("1. Easy", (200, 200))
        draw_text("2. Not So Easy", (200, 250))
        draw_text("3. A Bit Hard", (200, 300))
        draw_text("4. Hard", (200, 350))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game = Sudoku("Easy")
                elif event.key == pygame.K_2:
                    game = Sudoku("Not So Easy")
                elif event.key == pygame.K_3:
                    game = Sudoku("A Bit Hard")
                elif event.key == pygame.K_4:
                    game = Sudoku("Hard")
                else:
                    continue
                selecting = False

def draw_grid():
    for i in range(10):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (i * GRID_SIZE, 0), (i * GRID_SIZE, WIDTH), thickness)
        pygame.draw.line(screen, BLACK, (0, i * GRID_SIZE), (WIDTH, i * GRID_SIZE), thickness)

def draw_numbers():
    for row in range(9):
        for col in range(9):
            num = game.board[row][col]
            if num != 0:
                text = FONT.render(str(num), True, BLUE)
                screen.blit(text, (col * GRID_SIZE + 20, row * GRID_SIZE + 15))

def draw_stats():
    completed_percent = (game.correct_moves / game.total_cells) * 100 if game.total_cells else 0
    wrong_percent = (game.wrong_moves / game.total_cells) * 100 if game.total_cells else 0
    draw_text(f"Completed: {completed_percent:.1f}%", (10, 550))
    draw_text(f"Wrong: {wrong_percent:.1f}%", (300, 550), RED)
    draw_text(f"Hints Used: {game.hints_used}", (200, 570), GREY)

def main():
    global game
    select_difficulty()
    running = True
    while running:
        screen.fill(WHITE)
        draw_grid()
        draw_numbers()
        draw_stats()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:  # Press "H" for a hint
                    hint = game.get_hint()
                    if hint:
                        row, col, hint_num = hint
                        game.board[row][col] = hint_num
                        game.hints_used += 1  # Track hints used
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
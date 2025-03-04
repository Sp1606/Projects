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
        # Keep a copy of the initial puzzle so that given cells can be identified
        self.original_board = [row[:] for row in self.board]
        self.wrong_moves = 0
        self.selected_cell = None
        self.show_solution = False  # Track whether to show the solution

    def generate_full_board(self):
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
        # Copy full solution into board, then remove some cells based on difficulty.
        self.board = [row[:] for row in self.solution]
        blanks = {"Easy": 30, "Medium": 40, "Hard": 50, "Very Hard": 55}.get(self.difficulty, 30)
        while blanks > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                blanks -= 1

# Initialize Pygame and settings.
pygame.init()
WIDTH, HEIGHT = 540, 700  # Extra space for the solution button
GRID_SIZE = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
GREY  = (200, 200, 200)
FONT = pygame.font.Font(None, 40)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Game")
game = None  # Will be initialized after difficulty selection

# --- UI functions ---

def draw_button(text, x, y, width, height, color, hover_color, font_color=BLACK):
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, button_rect)
    else:
        pygame.draw.rect(screen, color, button_rect)
    draw_text(text, (x + 10, y + 10), font_color)

def draw_difficulty_menu():
    screen.fill(WHITE)
    draw_text("Select Difficulty Level", (130, 150))
    draw_button("Easy", 170, 250, 200, 50, GREEN, (100, 255, 100))
    draw_button("Medium", 170, 320, 200, 50, BLUE, (100, 100, 255))
    draw_button("Hard", 170, 390, 200, 50, RED, (255, 100, 100))
    draw_button("Very Hard", 170, 460, 200, 50, GREY, (200, 200, 200))
    pygame.display.flip()

def handle_difficulty_input(x, y):
    global game
    if 170 <= x <= 370:
        if 250 <= y <= 300:
            game = Sudoku("Easy")
        elif 320 <= y <= 370:
            game = Sudoku("Medium")
        elif 390 <= y <= 440:
            game = Sudoku("Hard")
        elif 460 <= y <= 510:
            game = Sudoku("Very Hard")
        else:
            return False
    return True

def draw_grid():
    # Draw the Sudoku grid with thicker lines for 3x3 sections.
    for i in range(10):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (i * GRID_SIZE, 0), (i * GRID_SIZE, 9 * GRID_SIZE), thickness)
        pygame.draw.line(screen, BLACK, (0, i * GRID_SIZE), (9 * GRID_SIZE, i * GRID_SIZE), thickness)

def draw_numbers():
    # Draw the numbers on the board. Given numbers (from original_board) are blue.
    for row in range(9):
        for col in range(9):
            num = game.board[row][col]
            if num != 0:
                # Given numbers in the puzzle are in blue; user-entered ones are in black.
                color = BLUE if game.original_board[row][col] != 0 else BLACK
                text = FONT.render(str(num), True, color)
                screen.blit(text, (col * GRID_SIZE + 20, row * GRID_SIZE + 15))

def draw_selected_cell():
    # If a cell is selected, draw a green rectangle around it.
    if game.selected_cell:
        row, col = game.selected_cell
        rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, GREEN, rect, 4)

def calculate_progress():
    # Only count cells that were originally blank.
    total_blank = sum(1 for row in range(9) for col in range(9) if game.original_board[row][col] == 0)
    solved = sum(1 for row in range(9) for col in range(9)
                 if game.original_board[row][col] == 0 and game.board[row][col] == game.solution[row][col])
    percent_solved = (solved / total_blank) * 100 if total_blank > 0 else 100
    return percent_solved

def draw_stats():
    # Display progress stats below the board.
    percent_solved = calculate_progress()
    draw_text(f"Solved: {percent_solved:.1f}%", (10, 555))
    draw_text(f"Wrong Moves: {game.wrong_moves}", (300, 555), RED)

def draw_text(text, pos, color=BLACK):
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, pos)

def handle_input(key):
    if game.selected_cell:
        row, col = game.selected_cell
        # Only allow input into cells that were originally blank.
        if game.original_board[row][col] == 0 and pygame.K_1 <= key <= pygame.K_9:
            num = key - pygame.K_0
            if num == game.solution[row][col]:
                game.board[row][col] = num
            else:
                game.wrong_moves += 1

def draw_solution_button():
    # Draw the "Solution" button at the bottom.
    pygame.draw.rect(screen, GREY, pygame.Rect(200, HEIGHT - 90, 220, 50))
    draw_text("Show Solution", (210, HEIGHT - 75), BLACK)

def handle_solution_button_click(x, y):
    if 200 <= x <= 340 and HEIGHT - 90 <= y <= HEIGHT - 40:
        game.show_solution = True

# --- Main game loop ---

def main():
    global game
    selecting_difficulty = True

    while True:
        if selecting_difficulty:
            draw_difficulty_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if handle_difficulty_input(x, y):
                        selecting_difficulty = False
                        break
        else:
            screen.fill(WHITE)
            draw_grid()
            draw_numbers()
            draw_selected_cell()  # Highlight the selected cell
            draw_stats()
            draw_solution_button()  # Draw the solution button
            if game.show_solution:
                # Reveal the solution when the button is pressed
                for row in range(9):
                    for col in range(9):
                        game.board[row][col] = game.solution[row][col]
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    # Handle click on the grid
                    if y < 9 * GRID_SIZE and x < 9 * GRID_SIZE:
                        game.selected_cell = (y // GRID_SIZE, x // GRID_SIZE)
                    # Handle click on the solution button
                    handle_solution_button_click(x, y)
                elif event.type == pygame.KEYDOWN:
                    handle_input(event.key)

if __name__ == "__main__":
    main()

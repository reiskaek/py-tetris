import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 480,640
CELL_SIZE = 30
COLUMNS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE
WHITE, BLACK, RED, GREEN, BLUE, YELLOW, CYAN, ORANGE = (
    (255, 255, 255), (0, 0, 0), (255, 0, 0), 
    (0, 255, 0), (0, 0, 255), (255, 255, 0), 
    (0, 255, 255), (255, 165, 0)
)

# Tetromino shapes
TETROMINOS = {
    "I": [[[1, 1, 1, 1]], [[1], [1], [1], [1]]],
    "O": [[[1, 1], [1, 1]]],
    "T": [[[0, 1, 0], [1, 1, 1]], [[1, 0], [1, 1], [1, 0]], 
          [[1, 1, 1], [0, 1, 0]], [[0, 1], [1, 1], [0, 1]]],
    "L": [[[0, 0, 1], [1, 1, 1]], [[1, 0], [1, 0], [1, 1]], 
          [[1, 1, 1], [1, 0, 0]], [[1, 1], [0, 1], [0, 1]]],
    "J": [[[1, 0, 0], [1, 1, 1]], [[1, 1], [1, 0], [1, 0]], 
          [[1, 1, 1], [0, 0, 1]], [[0, 1], [0, 1], [1, 1]]],
    "S": [[[0, 1, 1], [1, 1, 0]], [[1, 0], [1, 1], [0, 1]]],
    "Z": [[[1, 1, 0], [0, 1, 1]], [[0, 1], [1, 1], [1, 0]]],
}

# Color mapping
COLORS = {"I": CYAN, "O": YELLOW, "T": WHITE, "L": ORANGE, 
          "J": BLUE, "S": GREEN, "Z": RED}

# Game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Grid for tracking filled blocks
grid = [[None] * COLUMNS for _ in range(ROWS)]

class Tetromino:
    def __init__(self, name):
        self.name = name
        self.rotations = TETROMINOS[name]
        self.rotation = 0
        self.shape = self.rotations[self.rotation]
        self.x = COLUMNS // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.color = COLORS[name]

    def rotate(self):
        next_rotation = (self.rotation + 1) % len(self.rotations)
        next_shape = self.rotations[next_rotation]
        if not self.collides(next_shape, self.x, self.y):
            self.rotation = next_rotation
            self.shape = next_shape

    def move(self, dx, dy):
        if not self.collides(self.shape, self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
        elif dy == 1:
            place_piece(self)

    def collides(self, shape, x, y):
        for row_index, row in enumerate(shape):
            for col_index, cell in enumerate(row):
                if cell:
                    grid_x = x + col_index
                    grid_y = y + row_index
                    if grid_x < 0 or grid_x >= COLUMNS or grid_y >= ROWS or grid[grid_y][grid_x]:
                        return True
        return False

def place_piece(piece):
    """ Locks piece into grid and spawns new one. """
    for row_index, row in enumerate(piece.shape):
        for col_index, cell in enumerate(row):
            if cell:
                grid[piece.y + row_index][piece.x + col_index] = piece.color
    clear_lines()
    spawn_piece()

def clear_lines():
    """ Removes filled rows and shifts everything down. """
    global grid
    new_grid = [row for row in grid if any(cell is None for cell in row)]
    cleared_lines = ROWS - len(new_grid)
    new_grid = [[None] * COLUMNS for _ in range(cleared_lines)] + new_grid
    grid = new_grid

def spawn_piece():
    """ Generates a new piece and checks for game over. """
    global current_piece
    current_piece = Tetromino(random.choice(list(TETROMINOS.keys())))
    if current_piece.collides(current_piece.shape, current_piece.x, current_piece.y):
        game_over()

def game_over():
    """ Ends the game and resets everything. """
    global grid
    print("Game Over!")
    pygame.quit()
    exit()

def draw_grid():
    """ Draws the grid and placed blocks. """
    for y in range(ROWS):
        for x in range(COLUMNS):
            cell = grid[y][x]
            if cell:
                pygame.draw.rect(screen, cell, 
                                 (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, BLACK, 
                                 (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_piece(piece):
    """ Draws the currently falling tetromino. """
    for row_index, row in enumerate(piece.shape):
        for col_index, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, piece.color, 
                                 ((piece.x + col_index) * CELL_SIZE, 
                                  (piece.y + row_index) * CELL_SIZE, 
                                  CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, BLACK, 
                                 ((piece.x + col_index) * CELL_SIZE, 
                                  (piece.y + row_index) * CELL_SIZE, 
                                  CELL_SIZE, CELL_SIZE), 1)

# Start game
spawn_piece()
clock = pygame.time.Clock()

# Game loop
running = True
fall_timer = 0
fall_speed = 30  # Lower = faster falling

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_piece.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                current_piece.move(1, 0)
            elif event.key == pygame.K_DOWN:
                current_piece.move(0, 1)
            elif event.key == pygame.K_UP:
                current_piece.rotate()

    # Handle piece falling
    fall_timer += 1
    if fall_timer >= fall_speed:
        current_piece.move(0, 1)
        fall_timer = 0

    # Draw game state
    draw_grid()
    draw_piece(current_piece)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

import pygame
import random
import sys

pygame.init()

# Define colors
colors = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# Define font and screen size
FONT = pygame.font.SysFont('arial', 40)
GRID_SIZE = 4
TILE_SIZE = 100
MARGIN = 10
SCREEN_SIZE = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * MARGIN
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("2048")

def initialize_grid():
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    add_new_tile(grid)
    add_new_tile(grid)
    return grid

def add_new_tile(grid):
    empty_tiles = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] == 0]
    if empty_tiles:
        i, j = random.choice(empty_tiles)
        grid[i][j] = random.choice([2, 4])

def draw_grid(grid):
    screen.fill((187, 173, 160))  # Background color
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = grid[i][j]
            color = colors.get(value, (60, 58, 50))
            pygame.draw.rect(screen, color, (MARGIN + j * (TILE_SIZE + MARGIN), MARGIN + i * (TILE_SIZE + MARGIN), TILE_SIZE, TILE_SIZE))
            if value != 0:
                text = FONT.render(str(value), True, (119, 110, 101) if value <= 4 else (255, 255, 255))
                text_rect = text.get_rect(center=(MARGIN + j * (TILE_SIZE + MARGIN) + TILE_SIZE // 2,
                                                  MARGIN + i * (TILE_SIZE + MARGIN) + TILE_SIZE // 2))
                screen.blit(text, text_rect)

def compress(row):
    new_row = [num for num in row if num != 0]
    new_row += [0] * (GRID_SIZE - len(new_row))
    return new_row

def merge(row):
    for i in range(GRID_SIZE - 1):
        if row[i] == row[i + 1] and row[i] != 0:
            row[i] *= 2
            row[i + 1] = 0
    return row

def move_left(grid):
    new_grid = []
    for row in grid:
        new_row = compress(row)
        new_row = merge(new_row)
        new_row = compress(new_row)
        new_grid.append(new_row)
    return new_grid

def move_right(grid):
    new_grid = []
    for row in grid:
        new_row = compress(row[::-1])
        new_row = merge(new_row)
        new_row = compress(new_row)
        new_grid.append(new_row[::-1])
    return new_grid

def transpose(grid):
    return [list(row) for row in zip(*grid)]

def move_up(grid):
    grid = transpose(grid)
    grid = move_left(grid)
    return transpose(grid)

def move_down(grid):
    grid = transpose(grid)
    grid = move_right(grid)
    return transpose(grid)

def check_win(grid):
    return any(2048 in row for row in grid)

def check_game_over(grid):
    if any(0 in row for row in grid):
        return False
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE - 1):
            if grid[i][j] == grid[i][j + 1] or grid[j][i] == grid[j + 1][i]:
                return False
    return True

def play_game():
    grid = initialize_grid()
    draw_grid(grid)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                new_grid = None
                if event.key == pygame.K_UP:
                    new_grid = move_up(grid)
                elif event.key == pygame.K_DOWN:
                    new_grid = move_down(grid)
                elif event.key == pygame.K_LEFT:
                    new_grid = move_left(grid)
                elif event.key == pygame.K_RIGHT:
                    new_grid = move_right(grid)

                if new_grid and new_grid != grid:
                    add_new_tile(new_grid)
                    grid = new_grid
                    draw_grid(grid)
                    pygame.display.update()

                if check_win(grid):
                    print("Congratulations! You reached 2048!")
                    return

                if check_game_over(grid):
                    print("Game Over! No more possible moves.")
                    return

if __name__ == "__main__":
    play_game()

import pygame
import random

# Config
WIDTH, HEIGHT = 600, 640
ROWS, COLS = 30, 30
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (220, 220, 220)
PLAYER_COLOR = (255, 165, 0)

# Init
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze DFS Game with Score")

font = pygame.font.SysFont("arial", 20)

def make_grid():
    return [[1 if random.random() > 0.3 else 0 for _ in range(COLS)] for _ in range(ROWS)]

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(win, GREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(win, GREY, (0, y), (WIDTH, y))

def draw(maze, path=[], start=None, end=None, player=None, score=None, steps=None, optimal=None):
    win.fill(WHITE)
    for i in range(ROWS):
        for j in range(COLS):
            x, y = j * CELL_SIZE, i * CELL_SIZE
            if maze[i][j] == 0:
                pygame.draw.rect(win, BLACK, (x, y, CELL_SIZE, CELL_SIZE))
            elif (i, j) in path:
                pygame.draw.rect(win, BLUE, (x, y, CELL_SIZE, CELL_SIZE))
            if (i, j) == start:
                pygame.draw.rect(win, GREEN, (x, y, CELL_SIZE, CELL_SIZE))
            if (i, j) == end:
                pygame.draw.rect(win, RED, (x, y, CELL_SIZE, CELL_SIZE))
            if player == (i, j):
                pygame.draw.rect(win, PLAYER_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
    draw_grid()
    
    if score is not None:
        text = font.render(f"Skor: {score:.2f}  Langkahmu: {steps}  Optimal: {optimal}", True, (0, 0, 0))
        win.blit(text, (10, 610))  # Letakkan di bawah maze


    pygame.display.update()

def get_neighbors(pos, maze):
    i, j = pos
    neighbors = []
    for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < ROWS and 0 <= nj < COLS and maze[ni][nj] != 0:
            neighbors.append((ni, nj))
    return neighbors

def dfs(maze, start, end):
    stack = [start]
    visited = set()
    parent = {}

    while stack:
        current = stack.pop()
        if current == end:
            break
        for neighbor in get_neighbors(current, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    path = []
    node = end
    while node != start:
        if node in parent:
            path.append(node)
            node = parent[node]
        else:
            return []
    path.append(start)
    path.reverse()
    return path

def main():
    maze = make_grid()
    start = (0, 0)
    end = (ROWS - 1, COLS - 1)
    maze[start[0]][start[1]] = 1
    maze[end[0]][end[1]] = 1

    optimal_path = dfs(maze, start, end)
    if not optimal_path:
        print("Maze tidak dapat diselesaikan. Jalankan ulang.")
        return

    optimal_steps = len(optimal_path) - 1
    player = list(start)
    path_taken = []
    score = None
    reached_end = False

    run = True
    while run:
        draw(maze, [], start, end, tuple(player), score, len(path_taken), optimal_steps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if not reached_end:
            di, dj = 0, 0
            if keys[pygame.K_LEFT]: dj = -1
            elif keys[pygame.K_RIGHT]: dj = 1
            elif keys[pygame.K_UP]: di = -1
            elif keys[pygame.K_DOWN]: di = 1

            ni, nj = player[0] + di, player[1] + dj
            if 0 <= ni < ROWS and 0 <= nj < COLS and maze[ni][nj] == 1:
                player = [ni, nj]
                path_taken.append((ni, nj))

            if tuple(player) == end:
                reached_end = True
                player_steps = len(path_taken)
                score = (optimal_steps / player_steps) * 100 if player_steps > 0 else 0

        pygame.time.delay(100)

    pygame.quit()

if __name__ == "__main__":
    main()

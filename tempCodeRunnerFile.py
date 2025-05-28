import pygame
import random
from collections import deque

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 30, 30
CELL_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (220, 220, 220)

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver Game (DFS)")

# Create grid
def make_grid():
    return [[1 for _ in range(COLS)] for _ in range(ROWS)]

# Draw grid lines
def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(win, GREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(win, GREY, (0, y), (WIDTH, y))

# Draw entire board
def draw(maze, path=[], start=None, end=None):
    win.fill(WHITE)
    for i in range(ROWS):
        for j in range(COLS):
            x = j * CELL_SIZE
            y = i * CELL_SIZE
            if maze[i][j] == 0:
                pygame.draw.rect(win, BLACK, (x, y, CELL_SIZE, CELL_SIZE))
            elif (i, j) in path:
                pygame.draw.rect(win, BLUE, (x, y, CELL_SIZE, CELL_SIZE))
            if start == (i, j):
                pygame.draw.rect(win, GREEN, (x, y, CELL_SIZE, CELL_SIZE))
            if end == (i, j):
                pygame.draw.rect(win, RED, (x, y, CELL_SIZE, CELL_SIZE))
    draw_grid()
    pygame.display.update()

# Generate random maze
def generate_maze():
    maze = make_grid()
    for i in range(ROWS):
        for j in range(COLS):
            if random.random() < 0.3:
                maze[i][j] = 0  # wall
    return maze

# DFS algorithm
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

    # Reconstruct path
    path = []
    node = end
    while node != start:
        if node in parent:
            path.append(node)
            node = parent[node]
        else:
            return []  # no path
    path.append(start)
    path.reverse()
    return path

# Get valid neighbors
def get_neighbors(pos, maze):
    i, j = pos
    neighbors = []
    for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < ROWS and 0 <= nj < COLS and maze[ni][nj] != 0:
            neighbors.append((ni, nj))
    return neighbors

# Main loop
def main():
    maze = generate_maze()
    start = (0, 0)
    end = (ROWS-1, COLS-1)
    maze[start[0]][start[1]] = 1
    maze[end[0]][end[1]] = 1

    path = dfs(maze, start, end)

    run = True
    while run:
        draw(maze, path, start, end)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()

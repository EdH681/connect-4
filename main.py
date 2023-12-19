import pygame
from math import *


def squares(start, size):
    x = start[0]
    y = start[1]
    for i in range(7):
        for j in range(6):
            pygame.draw.rect(win, "white", (x + (size*i), y + (size*j), size, size), 1)


def counters(table, start):
    xpos = start[0] + 50
    ypos = start[1] + 50
    colours = {1: "red", 2: "blue"}
    for y in range(len(table)):
        for x in range(len(table[y])):
            if table[y][x] != 0:
                pygame.draw.circle(win, colours[table[y][x]], (xpos + (100*x), ypos + (100*y)), 45)


def cursor_to_column(mousePos):
    x = floor((mousePos[0] - 150) / 100) + 1
    if x < 1:
        x = 1
    if x > 7:
        x = 7
    return x


def column_marker(column):
    column = (150 + (100 * (column-1)))
    pygame.draw.rect(win, (10, 10, 10), (column, 200, 100, 600))


def bottom(column, table):
    column -= 1
    for r in range(len(table)-1):
        if table[r+1][column] != 0:
            return r
    return len(table) - 1


def checks(table):
    # horizontal
    for i in range(len(table)):
        for j in range(len(table[i])-3):
            if table[i][j] == table[i][j+1] == table[i][j+2] == table[i][j+3] and table[i][j] != 0:
                print(f"4 in a row horizontally starting at {j+1}, {6-(i+1)}")

    # vertical
    for i in range(len(table)-3):
        for j in range(len(table[i])):
            if table[i][j] == table[i+1][j] == table[i+2][j] == table[i+3][j] and table[i][j] != 0:
                print(f"4 in a row vertically starting at {j+1}, {6-(i+1)}")

    # diagonal down
    for i in range(len(table)-3):
        for j in range(len(table[i])-3):
            if table[i][j] == table[i+1][j+1] == table[i+2][j+2] == table[i+3][j+3] and table[i][j] != 0:
                print(f"4 in a row diagonally down starting at {j+1}, {6-(i+1)}")

    # diagonal up
    for i in range(2, len(table)):
        for j in range(len(table[i])-3):
            if table[i][j] == table[i-1][j+1] == table[i-2][j+2] == table[i-3][j+3] and table[i][j] != 0:
                print(f"4 in a row diagonally up starting at {j+1}, {6-(i+1)}")


pygame.init()
win = pygame.display.set_mode((1000, 900))
font = pygame.font.SysFont("Lucida Sans Typewriter", 30)

grid = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]

running = True
player = 0

while running:

    mouse = pygame.mouse.get_pos()

    win.fill("black")
    col = cursor_to_column(mouse)
    row = bottom(col, grid)
    column_marker(col)
    counters(grid, (150, 200))
    squares((150, 200), 100)
    text = font.render(f"Player {player + 1}", True, "white")
    win.blit(text, (150, 100))
    checks(grid)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            if grid[0][col-1] == 0:
                grid[row][col-1] = player + 1
                player = ((player + 1) % 2)

        if event.type == pygame.QUIT:
            running = False

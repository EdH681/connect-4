import pygame
from math import *
import random
import threading


def display(table):
    for r in table:
        for c in r:
            print(f"{c:<2}", end="")
        print()


def squares(start, size):
    x = start[0]
    y = start[1]
    for i in range(7):
        for j in range(6):
            pygame.draw.rect(win, "white", (x + (size * i), y + (size * j), size, size), 1)


def counters(table, start):
    xpos = start[0] + 50
    ypos = start[1] + 50
    colours = {1: "red", 2: "blue"}
    for y in range(len(table)):
        for x in range(len(table[y])):
            if table[y][x] != 0:
                pygame.draw.circle(win, colours[table[y][x]], (xpos + (100 * x), ypos + (100 * y)), 45)


def cursor_to_column(mouse_pos):
    x = floor((mouse_pos[0] - 150) / 100) + 1
    if x < 1:
        x = 1
    if x > 7:
        x = 7
    return x


def column_marker(column):
    column = (150 + (100 * (column - 1)))
    pygame.draw.rect(win, (50, 50, 50), (column, 200, 100, 600))


def bottom(column, table):
    column -= 1
    for r in range(len(table) - 1):
        if table[r + 1][column] != 0:
            return r
    return len(table) - 1


def checks(table):
    # horizontal
    for i in range(len(table)):
        for j in range(len(table[i]) - 3):
            if table[i][j] == table[i][j + 1] == table[i][j + 2] == table[i][j + 3] and table[i][j] != 0:
                start = (200 + (100 * j)), (150 + (100 * (i + 1)))
                end = (100 + (100 * (j + 4))), (150 + (100 * (i + 1)))
                pygame.draw.line(win, "yellow", start, end, 20)
                return table[i][j]

    # vertical
    for i in range(len(table) - 3):
        for j in range(len(table[i])):
            if table[i][j] == table[i + 1][j] == table[i + 2][j] == table[i + 3][j] and table[i][j] != 0:
                start = (200 + (100 * j)), (150 + (100 * (i + 1)))
                end = (100 + (100 * (j + 1))), (150 + (100 * (i + 4)))
                pygame.draw.line(win, "yellow", start, end, 20)
                return table[i][j]

    # diagonal down
    for i in range(len(table) - 3):
        for j in range(len(table[i]) - 3):
            if table[i][j] == table[i + 1][j + 1] == table[i + 2][j + 2] == table[i + 3][j + 3] and table[i][j] != 0:
                start = (200 + (100 * j)), (150 + (100 * (i + 1)))
                end = (100 + (100 * (j + 4))), (150 + (100 * (i + 4)))
                pygame.draw.line(win, "yellow", start, end, 20)
                return table[i][j]

    # diagonal up
    for i in range(2, len(table)):
        for j in range(len(table[i]) - 3):
            if table[i][j] == table[i - 1][j + 1] == table[i - 2][j + 2] == table[i - 3][j + 3] and table[i][j] != 0:
                start = (200 + (100 * j)), (150 + (100 * (i + 1)))
                end = (100 + (100 * (j + 4))), (150 + (100 * (i - 2)))
                pygame.draw.line(win, "yellow", start, end, 20)
                return table[i][j]


class AI:
    def __init__(self):
        self.playerMoves = []
        self.moves = 0
        self.colWeight = [2, 5, 10, 17, 10, 5, 2]
        self.columns = [0, 1, 2, 3, 4, 5, 6]
        self.blocks = []

    def grid_check(self):
        # checking for player moves
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                if grid[r][c] == 1 and (c, r) not in self.playerMoves:
                    self.playerMoves.append((c, r))

    @staticmethod
    def horizontal(table):
        openings = []
        for i in range(len(table)):
            for j in range(len(table[i]) - 2):
                if table[i][j] == table[i][j + 1] == table[i][j + 2] and table[i][j] != 0:

                    if j > 0:
                        if table[i][j - 1] == 0:
                            openings.append((i, j - 1))
                    if j < 6:
                        if table[i][j + 3] == 0:
                            openings.append((i, j + 3))
        return openings

    @staticmethod
    def vertical(table):
        openings = []
        for i in range(len(table) - 2):
            for j in range(len(table[i])):
                if table[i][j] == table[i + 1][j] == table[i + 2][j] and table[i][j] != 0:
                    if i > 0:
                        openings.append((i + 3, j))
        return openings

    @staticmethod
    def diagonal_up(table):
        openings = []
        for i in range(2, len(table)):
            for j in range(len(table[i]) - 3):
                if table[i][j] == table[i - 1][j + 1] == table[i - 2][j + 2] and table[i][j] != 0:
                    if j > 0 and i < 6:
                        openings.append((i-3, j+3))
                    if j < 6 and i > 0:
                        openings.append((i+1, j-1))
        return openings

    @staticmethod
    def diagonal_down(table):
        openings = []
        for i in range(len(table) - 3):
            for j in range(len(table[i]) - 3):
                if table[i][j] == table[i + 1][j + 1] == table[i + 2][j + 2] and table[i][j] != 0:
                    if i < 3 and j < 4:
                        openings.append((i+3, j+3))


    def update_open(self, data):
        if data:
            for o in data:
                if o not in self.blocks:
                    print(f"Opening at: {o}")
                    self.blocks.append(o)

    def three_checks(self):
        # horizontal check
        horizontal_open = self.horizontal(grid)
        self.update_open(horizontal_open)
        # vertical check
        vertical_open = self.vertical(grid)
        self.update_open(vertical_open)
        # diagonal up check
        h_up_open = self.diagonal_up(grid)
        self.update_open(h_up_open)

    def play(self):
        if self.moves == 0:
            column = int(random.choices(self.columns, weights=self.colWeight)[0])
            if grid[5][column] == 0:
                grid[5][column] = 2
            else:
                grid[4][column] = 2

        self.moves += 1

    def run(self):
        global player
        while True:
            self.grid_check()
            self.three_checks()
            if player == 2:
                player = 1
                # self.play()


pygame.init()
win = pygame.display.set_mode((1000, 900))
font = pygame.font.SysFont("Lucida Sans Typewriter", 30)

grid = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]

running = True
player = 1
clickable = True

bot = AI()
ai = threading.Thread(target=bot.run)
ai.start()

while running:
    win.fill("black")
    mouse = pygame.mouse.get_pos()

    if player == 1:
        col = cursor_to_column(mouse)
        row = bottom(col, grid)
        column_marker(col)

        if pygame.mouse.get_pressed()[0] and clickable:
            if grid[0][col - 1] == 0:
                grid[row][col - 1] = player
                player = 2
                clickable = False
                continue
        if not pygame.mouse.get_pressed()[0]:
            clickable = True

    squares((150, 200), 100)
    counters(grid, (150, 200))

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

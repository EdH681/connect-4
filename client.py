import pygame
import game
import sys
import threading
from connection import Player

# initialising game
pygame.init()
win = pygame.display.set_mode((1000, 900))
title = pygame.font.SysFont("Lucida Sans Typewriter", 30)
sub = pygame.font.SysFont("Lucida Sans Typewriter", 25)

# starting player class and requests
player = Player()
req = threading.Thread(target=lambda: player.request())
req.start()

# mainloop
while True:

    mouse = pygame.mouse.get_pos()

    win.fill("black")
    col = game.cursor_to_column(mouse)
    row = game.bottom(col, player.grid)
    game.column_marker(col)
    game.counters(player.grid, (150, 200))
    game.squares((150, 200), 100)
    text = title.render(f"Player {player.id}", True, "White")
    win.blit(text, (150, 60))
    if player.id == player.current:
        turn = sub.render("Your turn", True, "lightgrey")
        win.blit(turn, (150, 100))
    else:
        turn = sub.render(f"Player {player.current}'s turn", True, "lightgrey")
        win.blit(turn, (150, 100))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            if player.current == player.id:
                if player.grid[0][col - 1] == 0:
                    player.grid[row][col - 1] = player.id
                    player.send(f"m{row}/{col-1}")
        if event.type == pygame.QUIT:
            player.send("_disconnect")
            sys.exit()

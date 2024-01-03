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
announcement = pygame.font.SysFont("Lucida Sans Typewriter", 40)

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
    text = title.render(f"Player {player.id}", True, "white")
    win.blit(text, (150, 60))

    if player.winner is None:
        if player.id == player.current:
            turn = sub.render("Your turn", True, "lightgrey")
            win.blit(turn, (150, 100))
        else:
            turn = sub.render(f"Player {player.current}'s turn", True, "lightgrey")
            win.blit(turn, (150, 100))
    else:
        if int(player.winner[0]) == player.id:
            winAnnounce = announcement.render("You win", True, "white")
            win.blit(winAnnounce, (150, 100))
        else:
            winAnnounce = announcement.render(f"Player {player.winner[0]} wins", True, "white")
            win.blit(winAnnounce, (150, 100))

        row1 = int(player.winner[1])
        row1 = (((row1 + 1) * 100) + 150)
        col1 = int(player.winner[2])
        col1 = ((col1 * 100) + 200)

        row2 = int(player.winner[3])
        row2 = (((row2 + 1) * 100) + 150)
        col2 = int(player.winner[4])
        col2 = ((col2 * 100) + 200)

        start = (col1, row1)
        end = (col2, row2)

        pygame.draw.line(win, "Yellow", start, end, 10)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            if player.current == player.id:
                if player.grid[0][col - 1] == 0 and player.winner is None:
                    player.grid[row][col - 1] = player.id
                    player.send(f"m{row}/{col-1}")
        if event.type == pygame.QUIT:
            player.send("_disconnect")
            sys.exit()

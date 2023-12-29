import pygame
import game
import sys
import threading
from connection import Player

'''
Function of the client:
- Run the graphics of the game
- Take the input of each player
- Send the most recent move of the player
- Receive the result of the round
- Indicate if a player wins
'''

# initialising game
pygame.init()
win = pygame.display.set_mode((1000, 900))
font = pygame.font.SysFont("Lucida Sans Typewriter", 30)


player = Player()
req = threading.Thread(target=lambda: player.request())
req.start()
# pygame mainloop
while True:

    mouse = pygame.mouse.get_pos()

    win.fill("black")
    col = game.cursor_to_column(mouse)
    row = game.bottom(col, player.grid)
    game.column_marker(col)
    game.counters(player.grid, (150, 200))
    game.squares((150, 200), 100)
    text = font.render(f"Player {player.id}", True, "White")
    win.blit(text, (150, 100))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            if player.grid[0][col - 1] == 0:
                player.grid[row][col - 1] = int(player.id)
                player.send(f"m{row}/{col-1}")
        if event.type == pygame.QUIT:
            player.send("_disconnect")
            sys.exit()

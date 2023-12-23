import socket
import sys
import pygame
import threading
import game


def send(msg):
    message = str(msg).encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    if msg == "Start":
        result = client.recv(2048).decode(FORMAT)
        print(result)
        return int(result)

def recieve_grid():
    pass



'''
Function of the client:
- Run the graphics of the game
- Take the input of each player
- Send the most recent move of the player
- Receive the result of the round
- Indicate if a player wins
'''

# CONSTANTS
HEADER = 64
PORT = 8888
FORMAT = "utf-8"
DISCONNECT = "!DISCONNECT"
SERVER = "192.168.1.207"
ADDR = (SERVER, PORT)

# initialising connection with server
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
except TimeoutError:
    print("Connection timeout")
except ConnectionRefusedError:
    print("Server is not running")

# initialising game
pygame.init()
win = pygame.display.set_mode((1000, 900))
font = pygame.font.SysFont("Lucida Sans Typewriter", 30)

grid =[
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
        ]
player = 0
res = send("Start")
if res:
    player = res

# pygame mainloop
while True:

    mouse = pygame.mouse.get_pos()

    win.fill("black")
    col = game.cursor_to_column(mouse)
    row = game.bottom(col, grid)
    game.column_marker(col)
    game.counters(grid, (150, 200))
    game.squares((150, 200), 100)
    text = font.render(f"Player {player}", True, "White")
    win.blit(text, (150, 100))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            if grid[0][col - 1] == 0:
                grid[row][col - 1] = player
                send("g"+str(grid))
        if event.type == pygame.QUIT:
            sys.exit()

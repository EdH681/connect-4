import socket
import sys
import pygame

pygame.init()
win = pygame.display.set_mode((500, 500))
x, y = 250, 250

HEADER = 64
PORT = 8888
FORMAT = "utf-8"
DISCONNECT = "!DISCONNECT"
SERVER = "192.168.1.207"
ADDR = (SERVER, PORT)

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
except TimeoutError:
    print("Connection timeout")
    sys.exit()
except ConnectionRefusedError:
    print("Server is not running")


def send(msg):
    global x
    message = str(msg).encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(f"sent {msg}")
    result = client.recv(2048).decode(FORMAT)
    if result:
        x = int(result)
    else:
        x = 0





while True:

    win.fill("black")
    pygame.draw.circle(win, "white", (x, y), 5)
    pygame.display.update()

    send(input("> "))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
import socket
import sys
import threading

'''
Function of the server:
- Receive the current grid from the player who just played
- Update the grid stored on the server
- Check the grid for wins
- Send the updated grid to both players
- Send if there was a win + where the win was 
- Alternate between which player is moving
'''

# =constants=
HEADER = 64
PORT = 8888
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT = "!DISCONNECT"
CLOSE = "!CLOSE"
PLAYERS = [1, 2]

players = {}

grid = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
        ]

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

except TimeoutError:
    print("Error: server timeout")
    sys.exit()
except OSError:
    print(f"{ADDR} is already in use")
    sys.exit()


def handle_client(conn, addr):
    global players, grid
    print(f"\nNew connection: {addr}")
    connected = True
    while connected:

        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT:
                print(f"{addr} disconnected")
                connected = False
                break

            if msg == "Start" and len(PLAYERS) > 0:
                conn.send(str(PLAYERS[0]).encode(FORMAT))
                print(f"{addr} is player {PLAYERS[0]}")
                players[addr] = f"Player {PLAYERS[0]}"
                PLAYERS.remove(PLAYERS[0])

            if msg[0] == "g":
                msg = msg[1:]
                msg = msg.replace("(", "")
                msg = msg.replace(")", "")
                msg.split(",")
                print(f"Player {players[addr]}: made a move at {msg}")

                for player in players:
                    conn.send(msg.encode(FORMAT))

    conn.close()
    print()


def start():
    server.listen()
    print(f"Listening on ip {SERVER}, port {PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


print("Server starting...")
start()

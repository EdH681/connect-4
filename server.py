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
PLAYERS = ["1", "2"]

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
    print(f"\nNew connection: {addr}")
    connected = True
    while connected:
        msg = conn.recv(4096).decode()

        if msg == "!start":
            if len(PLAYERS) > 0:
                player = PLAYERS[0]
                players[addr] = PLAYERS[0]
                print(f"{addr} is player {PLAYERS[0]}")
                PLAYERS.remove(PLAYERS[0])
                conn.send(str.encode(player))
            else:
                conn.send(str.encode("_full"))

        elif msg == "!disconnect":
            conn.send(str.encode("Disconnecting..."))
            print(f"Player {players[addr]} disconnected")
            connected = False
            conn.close()

        else:
            print(f"Player {players[addr]}: {msg}")
            conn.send(str.encode(f"Received"))

    conn.close()
    print()


def start():
    server.listen()
    print(f"Listening on ip {SERVER}, port {PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


process = threading.Thread(target=start)

print("Server starting...")
process.start()
print("isdfjbhdfj")

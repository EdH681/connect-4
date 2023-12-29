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

Protocol:
_ is the prefix for a command
some special cases have a different character for the first letter
'''

# =constants=
HEADER = 64
PORT = 8888
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
PLAYERS = ["1", "2"]

players = {}
moves = {
    "1": None,
    "2": None
}

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
    global grid
    print(f"\nNew connection: {addr}")
    connected = True
    while connected:
        msg = conn.recv(4096).decode()

        if msg == "_start":
            if len(PLAYERS) > 0:
                player = PLAYERS[0]
                players[addr] = PLAYERS[0]
                print(f"{addr} is player {PLAYERS[0]}")
                PLAYERS.remove(PLAYERS[0])
                conn.send(str.encode(player))
            else:
                conn.send(str.encode("_full"))

        elif msg == "_disconnect":
            conn.send(str.encode("_disconnected"))
            print(f"Player {players[addr]} disconnected")
            connected = False
            conn.close()

        elif msg == "_request":
            conn.send(str.encode("_received"))
            player = players[addr]
            send = str(2 - ((int(player) + 1) % 2))
            data = moves[send]
            if data:
                conn.send(str.encode(f"{data}/{send}"))
            else:
                conn.send(str.encode("_"))

        elif msg[0] == "m":
            move = msg[1:]
            print(f"{players[addr]}: {move}")
            moves[players[addr]] = move
            print(moves)


            conn.send(str.encode("_received"))

        else:
            print(f"Player {players[addr]}: {msg}")
            conn.send(str.encode("Received"))

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

import socket
import sys
import threading

'''
In order to send more complex data as a string, I created my own protocol which turns a list into a string with each
index separated by '/'

Command prefixes:
_: general commands between the server and client
m: sent by the player with move data
r: sent by the server as a response do data requests

Game data sent by server:
Index   Data
0       row
1       column
2       player
3       current player  
4       did someone win?
5       row start for win
6       column start for win
7       row end for win
8       column end for win
9       winner


'''


# =constants=
HEADER = 64
PORT = 8888
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
PLAYERS = ["1", "2"]

turn = 1
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
    global grid, turn
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

        # if the client disconnects
        elif msg == "_disconnect":
            conn.send(str.encode("_disconnected"))
            print(f"Player {players[addr]} disconnected")
            connected = False
            conn.close()

        # if the client requests game data
        elif msg == "_request":
            player = players[addr]
            send = str(2 - ((int(player) + 1) % 2))
            data = moves[send]
            if data:
                conn.send(str.encode(f"r{data}/{send}/{str(turn)}"))
            else:
                conn.send(str.encode(f"r_/_/_/{str(turn)}"))

        # if the client submits move data
        elif msg[0] == "m":
            move = msg[1:]
            if len(move) > 3:
                move = move[:3]
            print(f"{players[addr]}: {move}")
            moves[players[addr]] = move
            print(moves)
            turn = 2 - ((turn + 1) % 2)
            print(f"Player {turn}'s turn")


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

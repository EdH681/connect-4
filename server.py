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
4       winner
5       row start for win
6       column start for win
7       row end for win
8       column end for win

'''

def package(data):
    pack = ""
    for i in range(len(data)):
        if i != len(data)-1:
            pack += f"{data[i]}/"
        else:
            pack += str(data[i])
    return f"r{pack}"

def display(table):
    for row in table:
        for column in row:
            print(f"{column:<3}", end="")
        print()
    print()

def win_check(table):
    # horizontal
    for i in range(len(table)):
        for j in range(len(table[i])-3):
            if table[i][j] == table[i][j+1] == table[i][j+2] == table[i][j+3] and table[i][j] != 0:
                return table[i][j], i, j, i, j+3

    # vertical
    for i in range(len(table)-3):
        for j in range(len(table[i])):
            if table[i][j] == table[i+1][j] == table[i+2][j] == table[i+3][j] and table[i][j] != 0:
                return table[i][j], i, j, i+3, j
    # diagonal down
    for i in range(len(table)-3):
        for j in range(len(table[i])-3):
            if table[i][j] == table[i+1][j+1] == table[i+2][j+2] == table[i+3][j+3] and table[i][j] != 0:
                return table[i][j], i, j, i+3, j+3

    # diagonal up
    for i in range(2, len(table)):
        for j in range(len(table[i])-3):
            if table[i][j] == table[i-1][j+1] == table[i-2][j+2] == table[i-3][j+3] and table[i][j] != 0:
                return table[i][j], i, j, i-3, j+3

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
            info = ["_", "_", "_", "_", "_", "_", "_", "_", "_"]
            if data:
                data = data.split("/")
                row = data[0]
                col = data[1]
                info[0] = row
                info[1] = col
                info[2] = send

            win = win_check(grid)
            if win:
                winner = win[0]
                row1 = win[1]
                col1 = win[2]
                row2 = win[3]
                col2 = win[4]

                info[4] = winner
                info[5] = row1
                info[6] = col1
                info[7] = row2
                info[8] = col2


            info[3] = turn


            info = package(info)
            conn.send(str.encode(info))

        elif msg[0] == "m":
            move = msg[1:]
            if len(move) > 3:
                move = move[:3]
            #print(f"{players[addr]}: {move}")
            moves[players[addr]] = move
            move = move.split("/")
            r = int(move[0])
            c = int(move[1])
            grid[r][c] = players[addr]
            #print(moves)
            turn = 2 - ((turn + 1) % 2)
            #print(f"Player {turn}'s turn")
            display(grid)


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



process = threading.Thread(target=start)

print("Server starting...")
process.start()

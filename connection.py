import socket
import sys
import threading

'''
Function of connection
- Make the connection to the server easier to replicate
- Allows the client to send data to the server in a simpler way
'''


class Player:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.11"
        self.port = 8888
        self.addr = (self.server, self.port)
        self.id = int(self.connect())
        self.current = 1
        self.grid = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.client.send(str.encode("_start"))
            res = self.client.recv(4096).decode()
            if res == "_full":
                print("Server full")
                sys.exit()
            else:
                return res
        except Exception as e:
            print(e)
            sys.exit()

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(4096).decode()
        except WindowsError:
            sys.exit()

    def request(self):
        while True:
            res = self.send("_request")
            if res[0] == "r":
                move = res[1:]
                move = move.split("/")
                print(move)
                self.current = int(move[3])
                if move[0] != "_":
                    row = int(move[0])
                    col = int(move[1])
                    player = int(move[2])
                    self.grid[row][col] = player


if __name__ == "__main__":
    n = Player()
    thread = threading.Thread(target=n.request)
    thread.start()
    while True:
        result = n.send(input("> "))
        if result == "_disconnected":
            print("Disconnected")
            sys.exit()
        else:
            print(result)

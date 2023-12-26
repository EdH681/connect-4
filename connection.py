import socket
import sys
import threading

'''
Function of connection
- Make the connection to the server easier to replicate
- Allows the client to send data to the server in a simpler way
'''
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.207"
        self.port = 8888
        self.addr = (self.server, self.port)
        self.id = self.connect()
        print(f"Player {self.id}")

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.client.send(str.encode("!start"))
            result = self.client.recv(4096).decode()
            if result == "_full":
                print("Server full")
                sys.exit()
            else:
                return result
        except Exception as e:
            print(e)
            sys.exit()

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(4096).decode()
        except WindowsError:
            sys.exit()


if __name__ == "__main__":
    n = Network()
    thread = threading.Thread(target=n.search())
    thread.start()
    while True:
        print(n.send(input("> ")))



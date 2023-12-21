import socket
import sys
import threading

# =constants=
HEADER = 64
PORT = 8888
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT = "!DISCONNECT"
CLOSE = "!CLOSE"

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

except TimeoutError:
    print("Error: server timeout")
    sys.exit()
except OSError:
    print(f"{ADDR} is already in use")
    sys.exit()


def sorted(enter):
    enter.sort()
    return str(enter)


def handle_client(conn, addr):
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

            if msg == CLOSE:
                print("Server closing...")
                sys.exit()

            print(f"{addr[0]}: {msg}")
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

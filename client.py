import socket
import threading

FORMAT = "utf-8"
HEADER_SIZE = 1024
PORT = 8000
SERVER = "localhost"

EXIT_MSG = "/exit"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((SERVER, PORT))


def receive():
    if server.recv(HEADER_SIZE).decode(FORMAT) == "/name":
        username = input("Enter your name please: ")
        server.send(username.encode(FORMAT))
    while True:
        msg = server.recv(HEADER_SIZE).decode(FORMAT)
        if msg == EXIT_MSG:
            break

        print(msg)


def write():
    while True:
        msg = "{}".format(input(""))
        server.send(msg.encode(FORMAT))

        if msg == EXIT_MSG:
            break


def main():
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()


if __name__ == "__main__":
    main()

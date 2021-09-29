import socket
import threading

FORMAT = "utf-8"
HEADER_SIZE = 1024
PORT = 8000
SERVER = "localhost"

CMDS_MSG = "/key"
EXIT_MSG = "/exit"
LIST_MSG = "/list"

server = None

clients = {}
username_list = []
chat_rooms = {"0": []}


def disconnect(client):
    name = list(clients.keys()).index(client)
    username_list.pop(name)
    chat_rooms[clients[client]].remove(client)
    clients.pop(client)


def broadcast(msg, room):
    for client in room:
        client.send(msg.encode(FORMAT))


def handle(client, address):
    while True:
        try:
            msg = client.recv(HEADER_SIZE).decode(FORMAT)
            username = username_list[list(clients.keys()).index(client)]

            # até a versão 3.10 do python não existia switch/case na languagem
            # então tem que fazer essa coisa feia aqui
            if EXIT_MSG == msg:
                print("{} left!".format(username))
                client.send(EXIT_MSG.encode(FORMAT))
                disconnect(client)
                break
            elif LIST_MSG == msg:
                client.send(("user list: " + ", ".join(username_list)).encode(FORMAT))
            elif CMDS_MSG == msg:
                commands_list = (
                    "/key - list commands\n"
                    + "/list - list users\n"
                    + "/exit - exits chat\n"
                )

                client.send(commands_list.encode(FORMAT))
            elif msg:
                broadcast(f"{username}: {msg}", chat_rooms[clients[client]])
            else:
                continue
        except:
            disconnect(client)
            break


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER, PORT))
    server.listen()
    print("Started server")

    while True:
        client, address = server.accept()
        print("new connection from address {}".format(address))

        client.send("/name".encode(FORMAT))
        username = client.recv(HEADER_SIZE).decode(FORMAT)
        username_list.append(username)
        clients[client] = "0"
        chat_rooms["0"].append(client)

        print("new connection set username as {}".format(username))
        broadcast("{} joined!".format(username), chat_rooms["0"])

        client.send("Welcome to the chat {}!".format(username).encode(FORMAT))

        # a função handle é responsável por controlar as mensagens e comandos
        # é executado em threads para que cada conexão seja processada 'paralelamente'
        thread = threading.Thread(target=handle, args=(client, address))
        thread.start()


if __name__ == "__main__":
    main()

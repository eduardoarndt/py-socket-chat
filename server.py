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

clients = []
username_list = []


def disconnect(client, username):
    username_list.remove(username)
    clients.remove(client)


def broadcast(msg):
    for client in clients:
        client.send(msg.encode(FORMAT))


def handle(client, username):
    client.send("welcome to the chat {}!".format(username).encode(FORMAT))

    while True:
        try:
            msg = client.recv(HEADER_SIZE).decode(FORMAT)

            # até a versão 3.10 do python não existia switch/case na languagem
            # então tem que fazer essa coisa feia aqui
            if EXIT_MSG == msg:
                broadcast("{} left!".format(username))
                client.send(EXIT_MSG.encode(FORMAT))
                disconnect(client, username)
                break
            elif LIST_MSG == msg:
                user_list = ("user list: " + ", ".join(username_list))
                client.send(user_list.encode(FORMAT))
            elif CMDS_MSG == msg:
                commands_list = ("- /key - list commands\n- /list - list users\n- /exit - exits chat")
                client.send(commands_list.encode(FORMAT))
            elif msg:
                broadcast("{}: {}".format(username, msg))
            else:
                continue
        except:
            disconnect(client, username)
            break


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER, PORT))
    server.listen()
    print("started server")

    while True:
        client, address = server.accept()
        print("new connection from address {}".format(address))

        client.send("/name".encode(FORMAT))
        username = client.recv(HEADER_SIZE).decode(FORMAT)
        username_list.append(username)
        clients.append(client)

        print("new connection set username as {}".format(username))
        broadcast("{} joined!".format(username))

        # a função handle é responsável por controlar as mensagens e comandos
        # é executado em threads para que cada conexão seja processada 'paralelamente'
        thread = threading.Thread(target=handle, args=[client, username])
        thread.start()


if __name__ == "__main__":
    main()

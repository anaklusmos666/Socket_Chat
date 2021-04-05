import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())   #ipconfig
PORT = 9060

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
names = []

print(f'loading server...')

def broadcast(msg):
    for client in clients:
        client.send(msg)

def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            print(f'{names[clients.index(client)]}: {msg}')
            broadcast(msg)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = names[index]
            print(f'{nickname} disconnected!')
            names.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f'{str(address)} connected :)')

        client.send('NAME: '.encode('utf-8'))
        name = client.recv(1024)
        names.append(name)
        clients.append(client)

        print(f'Names of clients {names}')
        broadcast(f'{name} connected!\n'.encode('utf-8'))
        client.send(f'Connected to the SERVER'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()

print(f'server running >>>')
receive()
import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

clients = []
names = []

def broadcast(message, prefix=""):
    for client in clients:
        client.send(f'{prefix}{message}'.encode())

def handle(client):
    name = client.recv(1024).decode().split(" ")[-1]
    names.append(name)
    broadcast(f'{name} joined the chat!', prefix='[INFO] ')
    client.send(f'Welcome {name}!'.encode())
    while True:
        message = client.recv(1024).decode()
        if message:
            broadcast(f'{name}: {message}', prefix='[MESSAGE] ')
        else:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            broadcast(f'{names[index]} left the chat...', prefix='[INFO] ')
            name_index = names.index(name)
            names.pop(name_index)
            break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f'Server listening on {HOST}:{PORT}...')

while True:
    client, address = server.accept()
    print(f'Accepted connection from {address}')
    client.send('NAMEREQUIRED'.encode())
    name = client.recv(1024).decode().split(" ")[-1]
    print(f'Name of client is {name}!')
    client.send(f'Welcome {name}!'.encode())
    clients.append(client)
    print(f'Connected clients: {clients}')
    client_thread = threading.Thread(target=handle, args=(client,))
    client_thread.start()

server.close()
import socket
import threading

# Define the host and port for the chat room
HOST = "127.0.0.1"
PORT = 50007

# Create a list to store the client sockets
clients = []

# Function to handle a new client
def handle_client(client_socket, client_address):
    # Add the client socket to the list of clients
    clients.append(client_socket)

    while True:
        try:
            # Receive a message from the client
            message = client_socket.recv(1024).decode("utf-8")

            # If the message is empty, the client has disconnected
            if not message:
                clients.remove(client_socket)
                client_socket.close()
                break

            # Broadcast the message to all clients
            for client in clients:
                client.send(message.encode("utf-8"))
        except:
            client_socket.close()
            break

# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Start listening for clients
server_socket.listen(5)

print("Waiting for clients...")

# Continuously accept new clients
while True:
    client_socket, client_address = server_socket.accept()
    print("Accepted client from", client_address)

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()

# Close the server socket
server_socket.close()

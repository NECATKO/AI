import socket

def main():
    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 5000))

    # Send and receive messages
    while True:
        message = input("-> ")
        client_socket.send(message.encode('utf-8'))
        data = client_socket.recv(1024).decode('utf-8')
        print("Received from server: " + data)

if __name__ == '__main__':
    main()

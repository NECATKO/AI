import socket

def broadcast_data(sock, message):
    for socket in connections:
        if socket != server_socket and socket != sock:
            try:
                socket.send(message)
            except:
                socket.close()
                connections.remove(socket)

def main():
    # Create the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", 5000))
    server_socket.listen(100)

    # List to keep track of all connected clients
    connections = [server_socket]

    print("Chat server started on port 5000")

    while True:
        # Get the list of read sockets
        read_sockets, write_sockets, error_sockets = select.select(connections, [], [])

        for sock in read_sockets:
            # New connection
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                connections.append(sockfd)
                print("Client (%s, %s) connected" % addr)
                broadcast_data(sockfd, "[%s:%s] entered the chat room\n" % addr)
            # New message from a client
            else:
                try:
                    data = sock.recv(1024)
                    if data:
                        broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)
                except:
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print("Client (%s, %s) is offline" % addr)
                    sock.close()
                    connections.remove(sock)
                    continue
    server_socket.close()

if __name__ == '__main__':
    main()

import tkinter as tk
import socket

# Define the host and port for the chat room
HOST = "127.0.0.1"
PORT = 50007

# Create the GUI window
root = tk.Tk()
root.title("Chat Room")
root.geometry("1920x1080")

# Create a vertical layout to hold the messages and input
layout = tk.Frame(root)
layout.pack(side="top", fill="both", expand=True)

# Create a scrollable area for messages
scroll = tk.Scrollbar(layout)
scroll.pack(side="right", fill="y")

# Create a text view for messages
text_view = tk.Text(layout, yscrollcommand=scroll.set)
text_view.pack(side="left", fill="both", expand=True)
text_view.config(state="disabled")

# Connect the scrollbar to the text view
scroll.config(command=text_view.yview)

# Create a text entry for input
text_entry = tk.Entry(root)
text_entry.pack(side="bottom", fill="x")

# Function to handle receiving messages
def receive_message():
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break

            # Display the message in the text view
            text_view.config(state="normal")
            text_view.insert("end", message + "\n")
            text_view.config(state="disabled")
        except:
            client_socket.close()
            root.quit()

# Function to handle sending messages
def send_message(*args):
    # Get the text from the entry
    text = text_entry.get()

    # Send the message to the server
    client_socket.send(text.encode("utf-8"))

    # Clear the text from the entry
    text_entry.delete(0, "end")

# Connect the signal for sending messages on enter
text_entry.bind("<Return>", send_message)

# Create a socket for connecting to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
try:
    client_socket.connect((HOST, PORT))
except socket.error as msg:
    print("Connect failed. Error Code : " + str(msg[0]) + " Message " + msg[1])
    sys.exit()

# Start a thread to receive messages
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

# Start the GUI event loop
root.mainloop()

# Close the socket
client_socket.close()

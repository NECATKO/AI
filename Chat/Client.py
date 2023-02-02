import socket
import threading
import tkinter as tk

HOST = '0.tcp.eu.ngrok.io'
PORT = 17211
name = 'Nigga'

def receive_message():
    while True:
        try:
            message = s.recv(1024).decode()
            if message:
                chat_area.insert(tk.END, f'\n{message}')
        except:
            break

def send_message(event=None):
    message = entry_field.get()
    entry_field.delete(0, tk.END)
    s.send(message.encode())
    if message == 'bye':
        root.quit()

root = tk.Tk()
root.title("Chat App")

frame = tk.Frame(root)
scrollbar = tk.Scrollbar(frame)
chat_area = tk.Listbox(frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_area.pack(side=tk.LEFT, fill=tk.BOTH)
frame.pack()

entry_field = tk.Entry(root, width=50)
entry_field.bind("<Return>", send_message)
entry_field.pack()
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.send(f'name {name}'.encode())

receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

tk.mainloop()

s.close()
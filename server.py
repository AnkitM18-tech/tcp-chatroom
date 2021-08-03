# import libraries
import socket
import threading

#defining the host
host = "127.0.0.1"         #Local Host, if you are running it on a web server put the ip address of the server here
port = 55555               # don't choose any reserved ports like 80 or 21/22 choose beyond 10000

#Creating the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

#function for broadcasting the message
def broadcast(message):
    for client in clients:
        client.send(message)


#function to handle clients broadcasting and removing clients
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = client.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break


#function to receive the message
def receive():
    while True:
        client,address = server.accept()                   # running the accept method to accept the clients all the time and get their address
        print(f'Connected with {str(address)}')

        #getting the nickname and appending the nickname and client to lists
        client.send("NICKNAME".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)

        #Server admin message
        print(f"Nickname of the client is {nickname}!")
        #Broadcast to every client
        broadcast(f"{nickname} joined the chat!".encode('ascii'))
        #send the particular client that he/she has connected successfully
        client.send("Connected to the server!".encode('ascii'))

        #defining and running the thread
        thread = threading.Thread(target = handle, args=(client,))
        thread.start()

receive()
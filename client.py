# Importing Libraries
import socket
import threading

nickname = input("Choose a nickname: ")

#Creating the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connecting the client to the server
client.connect(('127.0.0.1',55555))

#will receive the messages continuosly from server
def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICKNAME":
                client.send(nickname.encode("ascii"))
            else:
                print(message)
        except:
            print("An Error occurred!")
            client.close()
            break


def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode("ascii"))

receiving_thread = threading.Thread(target= receive)
receiving_thread.start()

writing_thread = threading.Thread(target= write)
writing_thread.start()
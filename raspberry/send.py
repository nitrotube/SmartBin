import socket
import os

def send():
    host = '127.0.0.1'
    port = 5000

    client = socket.socket()
    client.connect((host, port))

    file = input("Enter name of file with image: ")
    data = open(file, 'rb').read()
    data+=b'\r\n\r\n'
    client.send(data)
    response = client.recv(1024).decode('utf-8')

    print("Response: " + response)

    client.close()

if __name__ == '__main__':
    send()

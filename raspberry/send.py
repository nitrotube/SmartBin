import socket

def send(file):

    host = '127.0.0.1'
    port = 5000

    client = socket.socket()
    client.connect((host, port))

    data = open(file, 'rb').read()
    data+=b'\r\n\r\n'
    client.send(data)

    response = client.recv(1024).decode('utf-8')
    client.close()

    return response

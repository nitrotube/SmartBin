import socket

def get_class(file):

    host = '192.168.0.133'
    port = 5000

    client = socket.socket()
    client.connect((host, port))

    data = open(file, 'rb').read()
    data+=b'\r\n\r\n'
    client.send(data)

    response = client.recv(1024).decode('utf-8')
    client.close()

    return response

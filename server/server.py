
import config as cfg

import socket

import label_image

def main():

    host = '0.0.0.0'
    port = 6006
    print("LOG:server started at " + host + ":" + str(port) + "\n")
    image_path = cfg.PATH['current_img']
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))

    server.listen(1)

    while 1:
        client, addr = server.accept()
        print("LOG:"+str(addr)+" connected\n")
    
        print("LOG:Recieving image...")
        request = b""


        while 1:
            temp = client.recv(1024)
            if not temp:
                break
            request+=temp
            eor = request.find(b'\r\n\r\n')
            if(eor != -1):
                break

        data = request[:eor+1]

        print("LOG:Complete\n")

        print("LOG:Saving image...")
        open(image_path, 'wb').write(data)
        print("LOG:Complete\n")

        print("LOG:start recognizing...")
        answer = label_image.get_class()
        #answer = 'test'
        print("LOG:%s recognized"%answer+"\n")

        client.send(answer.encode('utf-8'))
        client.close()

if __name__ == '__main__':
    main()

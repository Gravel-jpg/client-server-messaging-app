import socket,time
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((socket.gethostname(),8000))
#port 8000, local ip
sock.listen(5)
print('listening')
while True:
    time.sleep(2.5)
    clientsocket, address = sock.accept()
    print(f'connection from {address} has been established')
    clientsocket.send(bytes('connected to server','utf-8'))
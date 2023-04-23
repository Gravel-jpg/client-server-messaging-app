import socket
import os
import threading
from time import sleep

Host = '192.168.0.8'
# Host = '192.168.0.181'
# laptop "client"s ip is 192.168.0.18
Port = 666
# Port = 9100
# Initializes s
s = socket.socket()
# Links server to given port on ip, any traffic to that port is redirected to ME!
s.bind((Host,Port))
print(f'bound to :{Host}:{Port}')
# opens server to outside connections i think :/
backlog = []
s.listen()
def client_connection(client,address):
    while True:
        Server_recv = client.recv(1024).decode()
        if not Server_recv:
            print(f'connection with {address} Terminated')
            break 
        print(f'from{address}:{Server_recv}')
        backlog.append(Server_recv)
def backlog_Andy():
    while True:
        if len(backlog) > 0:
            for i in backlog:
                x = i.split(';')
                try:
                    z = x[1].split(',')
                    if x[0] == 'verify_login':
                        if z[0] == 'True':
                            print(f'{x[0]} is {z[0]} for {z[1]}')
                            backlog.remove(i)
                except:
                    pass
        else:
            sleep(1)
t = threading.Thread(target = backlog_Andy)
t.start()
while True:
    client,address = s.accept()
    print(f'connection from {address}')
    t = threading.Thread(target =client_connection,args =(client,address,))
    t.start()


#data send through any socket must be in bytes() format, strings can be turned into bytes, therefore: turn datatype into string, into bytes, send, recieve, into string, .eval()
# if you can use asynchronus functions while setblocking thatd be cool 
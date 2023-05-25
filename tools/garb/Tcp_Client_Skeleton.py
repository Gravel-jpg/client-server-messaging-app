import socket
import time
# host = '192.168.0.8'
host = '67.193.151.25'
# port = 666
# host = '192.168.0.181'
port = 9100
s = socket.socket()
s.connect((host,port))
message = 'verify_login;John Pork,return my calls'
s.send(message.encode())
s.close()
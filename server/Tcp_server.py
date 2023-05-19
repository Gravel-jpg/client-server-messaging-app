import socket
import threading
from time import sleep
import sqlite3
from server_functions import *

Host = '192.168.0.181'
Port = 9100

s = socket.socket()
# Links server to given port on ip, any traffic to that port is redirected to here
s.bind((Host,Port))
print(f'bound to :{Host}:{Port}')

# opens server to outside connections
s.listen()
def client_connection(client,address):
    db_name = os.path.join(here,'server_database.db')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    print('connection to database established')
    client_id = None
    x = cursor.execute(f"SELECT * FROM main WHERE uid = '4'").fetchall()
    send_string(f"server_keys;{x[0][3]}",None,cursor,client,False)
    while True:
        print(f'The client_id is {client_id}')
        Server_recv = process_string(client)
        if not Server_recv:
            print(f'connection with {address} Terminated')
            break
        command = Server_recv.split(';',1)[0]
        args = Server_recv.split(';',1)[1]
        args = args.split(',')
        if command == 'login_attempt':
            x = cursor.execute(f"SELECT * FROM main WHERE username = '{args[0]}' AND password = '{args[1]}'").fetchall()
            if x != []:
                client_id = x[0][2]
                send_string('login_attempt;True',client_id,cursor,client,True)
            else:
                print(f'Error: There is no user with the username {args[0]} and the password {args[1]}')
                send_string('login_attempt;False',None,cursor,client,False)
        elif command == 'key_request':
            #Recieves a key request for an existing user based off of username (maybe change to username or uid?), returns users public keys
            recipient = args[0]
            x = cursor.execute(f"SELECT * FROM main WHERE username = '{args[0]}'").fetchall()[0][3]
            print(f'x:{x}')
            if x != []:
                send_string(f'key_request;{x}',client_id,cursor,client,True)
                ciphertext = process_string(client)
                ciphertext = ciphertext.split(';')[1]
                print(f'final ciphertext to db {ciphertext}')
                cursor.execute("INSERT INTO backlog (outgoing ciphertext,recipient) VALUES (?, ?)", (f'{ciphertext}',f'{recipient}'))
                conn.commit()
                # Commit the outgoing ciphertext and username to backlog in the DB
            else:
                print(f'Error: There is no user with the username: {args[0]}')
                send_string('key_request;False',client_id,cursor,client,True)
        elif command == 'create_acc':
            x = cursor.execute(f"SELECT * FROM main WHERE username = '{args[0]}'").fetchall()
            if x!= []:
                send_string('create_acc;False',client_id,cursor,client,True)
                print('Error: username already taken')
            else:
                cursor.execute("INSERT INTO main (username, password,keys) VALUES (?, ?, ?)", (f'{args[0]}', f'{[1]}',f'{args[2]},{args[3]}'))
                conn.commit()
                # Not sure if the line below will do what i want
                client_id = cursor.execute(f"SELECT uid FROM main where username = '{args[0]}'").fetchall()[0][0]
                send_string('create_acc;True',client_id,cursor,client,True)
                print('username and password created')
        elif command == 'update_keys':
            x = cursor.execute(f"SELECT rowid FROM main WHERE uid = '{client_id}'").fetchall()
            if x != []:
                cursor.execute(f"UPDATE main SET keys = '{args[0]+','+args[1]}' WHERE rowid = '{x[0][0]}'")
                conn.commit()
                send_string('update_keys;True',client_id,cursor,client,True)
                print(f'Succesfully updated keys to {args[0]},{args[1]}')
            print(f'Error: command "{command}" not recognised ')
while True:
    client,address = s.accept()
    print(f'connection from {address}')
    t = threading.Thread(target =client_connection,args =(client,address,))
    t.start()


#data send through any socket must be in bytes() format, strings can be turned into bytes, therefore: turn datatype into string, into bytes, send, recieve, into string, .eval()
# if you can use asynchronus functions while setblocking thatd be cool
#encrypt all messages sent to server with a public key, decrypt with a private key when reaches server
#Then, when talking to each user after login has concluded, encrypt the messages using their stored public key

import socket
import threading
from time import sleep
import sqlite3
from server_functions import *

Host = '192.168.0.19'
Port = 9100

s = socket.socket()
# Links server to given port on ip, any traffic to that port is redirected to ME!
s.bind((Host,Port))
print(f'bound to :{Host}:{Port}')

# opens server to outside connections i think :/
s.listen()
def client_connection(client,address):
    db_name = os.path.join(here,'server_database.db')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    print('connection to database established')
    client_id = None
    x = cursor.execute(f"SELECT * FROM main WHERE uid = '4'").fetchall()
    send_string(f"server_keys;{x[0][3]}",None,cursor,client,False)
    # Can reduce this string into cursor.execute(f"SELECT * FROM main WHERE uid = '4'").fetchall()[0][3]
    while True:
        print(f'The client_id is {client_id}')
        # Server_recv = client.recv(4096).decode()
        Server_recv = process_string(client)
        if not Server_recv:
            print(f'connection with {address} Terminated')
            break
        # Server_recv = process_string(Server_recv)
        command = Server_recv.split(';',1)[0]
        args = Server_recv.split(';',1)[1]
        args = args.split(',')
        
        if command == 'login_attempt':
            #Recives username, pass, sends back either T/F and flags this thread with the users unique uid.
            x = cursor.execute(f"SELECT * FROM main WHERE username = '{args[0]}' AND password = '{args[1]}'").fetchall()
            if x != []:
                client_id = x[0][2]
                # send_string('login_attempt;True',client_id,cursor,client)
                send_string('login_attempt;True',client_id,cursor,client,True)
                ###send back something to verify the login
            else:
                ###send something to verify that login was incorrect
                print(f'Error: There is no user with the username {args[0]} and the password {args[1]}')
                # client.send('login_attempt;False'.encode())
                send_string('login_attempt;False',None,cursor,client,False)

        elif command == 'key_request':
            #Recieves a key request for an existing user based off of username (maybe change to username or uid?), returns users public keys
            x = cursor.execute(f"SELECT * FROM main WHERE username = '{args[0]}'").fetchall()
            if x != []:
                keys = x[0][3]
                print(f'keys : {keys}')
                # client.send(keys.encode())
                send_string(keys,client_id,cursor,client,True)
            else:
                print(f'Error: There is no user with the username {args[0]}')
                # client.send('key_request;False'.encode())
                send_string('key_request;False',client_id,cursor,client,True)
        elif command == 'send_cipher':
            pass
        elif command == 'create_acc':
            #create_acc;username,pass
            x = cursor.execute(f"SELECT * FROM main WHERE username = '{args[0]}'").fetchall()
            if x!= []:
                # client.send(f'create_acc;False'.encode())
                send_string('create_acc;False',client_id,cursor,client,True)
                print('Error: username already taken')
            else:
                #Code to insert new user into database and also have users submit keys.
                cursor.execute("INSERT INTO mytable (username, password,keys) VALUES (?, ?, ?)", (f'{args[0]}', f'{[1]}',f'{args[2]},{args[3]}'))
                conn.commit()
                ###CODE HERE TO GRAB UID### client_uid = querey
                # client.send('create_acc;True'.encode())
                send_string('create_acc;True',client_id,cursor,client,True)
                print('username and password created')
#             If the username is taken return false
#             If not, submit te account, grant it a unique uid, set the threads uid == and then return True
        elif command == 'update_keys':
            x = cursor.execute(f"SELECT rowid FROM main WHERE uid = '{client_id}'").fetchall()
            if x != []:
                cursor.execute(f"UPDATE main SET keys = '{args[0]+','+args[1]}' WHERE rowid = '{x[0][0]}'")
                conn.commit()
                send_string('update_keys;True',client_id,cursor,client,True)
            else:
                print('Error: update_keys could not find a user who matches the current client, despite them already logging in')
        # elif command == 'update_keys':
        #     if args[0][-2:] == ';;':
        #         #Piece it back together and then start chunkin as normal!
        #         args = process_string_pieces(args,client).split(',')
        #         x = cursor.execute(f"SELECT rowid FROM main where uid = '{client_id}").fetchall()
        #         if x != []:
        #             cursor.execute(f"UPDATE main SET keys = '{args[0]+','+args[1]}' WHERE rowid = '{x[0][0]}'")
        #             conn.comit()
        #             send_string(f'update_keys;True',client_id,cursor,client,True)
        #         else:
        #             print('Error: This shouldnt be possible')
        #     else:
        #         print('Error: This shouldnt be possible')
        #         print(args[0][-2:])
        else:
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

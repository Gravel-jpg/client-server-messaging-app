import socket
import threading
from time import sleep
import sqlite3
from server_functions import *

# ///TODO/// 
# encrypt all information in the database (SEE)
# put databases keys in Sjson.json
# above or find a better solution, maybe a file type that cant be accessed remotely? (I heard that might be something I can do)
# design ui for server?
# 


Port = 9100
timeout = 5
database_lock = threading.Lock()
s = socket.socket()
# Links server to given port on ip, any traffic to that port is redirected to here
s.bind((socket.gethostbyname(socket.gethostname()),Port))
print(f'bound to :{socket.gethostbyname(socket.gethostname())}:{Port}')

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
        try:
            print(f'The client_id is {client_id}')
            Server_recv = process_string(client)
            if not Server_recv:
                print(f'connection with {address} Terminated')
                break
            command = Server_recv.split(';',1)[0]
            args = Server_recv.split(';',1)[1]
            args = args.split(',')
            if command == 'login_attempt':
                database_lock.acquire()
                x = cursor.execute(f"SELECT * FROM main WHERE username = '{args[0]}' AND password = '{args[1]}'").fetchall()
                database_lock.release()
                if x != []:
                    client_id = x[0][2]
                    send_string('login_attempt;True',client_id,cursor,client,True)
                    client.settimeout(timeout)
                else:
                    print(f'Error: There is no user with the username {args[0]} and the password {args[1]}')
                    send_string('login_attempt;False',None,cursor,client,False)
            elif command == 'key_request':
                #Recieves a key request for an existing user based off of username (maybe change to username or uid?), returns users public keys
                database_lock.acquire()
                x = cursor.execute(f"SELECT * FROM main WHERE username = '{args[0]}'").fetchall()[0]
                database_lock.release()
                recipient = x[2]
                x = x[3]
                print(f'x:{x}')
                if x != []:
                    send_string(f'key_request;{x}',client_id,cursor,client,True)
                    ciphertext = process_string(client)
                    ciphertext = ciphertext.split(';')[1]
                    print(f'final ciphertext to db {ciphertext}')
                    database_lock.acquire()
                    cursor.execute("INSERT INTO backlog ('outgoing_ciphertext','recipient') VALUES (?, ?)", (f'{ciphertext}',f'{recipient}'))
                    conn.commit()
                    database_lock.release()
                    send_string('send_cipher;True',client_id,cursor,client,True)
                    # send_string('test test, recieve me in screen 3',client_id,cursor,client,True)
                else:
                    print(f'Error: There is no user with the username: {args[0]}')
                    send_string('key_request;False',client_id,cursor,client,True)
            elif command == 'create_acc':
                database_lock.acquire()
                x = cursor.execute(f"SELECT * FROM main WHERE username = '{args[0]}'").fetchall()
                database_lock.release()
                if x!= []:
                    send_string('create_acc;False',client_id,cursor,client,True)
                    print('Error: username already taken')
                else:
                    database_lock.acquire()
                    cursor.execute("INSERT INTO main ('username', 'password','keys') VALUES (?, ?, ?)", (f'{args[0]}', f'{args[1]}',f'{args[2]},{args[3]}'))
                    conn.commit()
                    client_id = cursor.execute(f"SELECT uid FROM main where username = '{args[0]}'").fetchall()[0][0]
                    database_lock.release()
                    send_string('create_acc;True',client_id,cursor,client,True)
                    print('username and password created')
                    client.settimeout(timeout)
            elif command == 'update_keys':
                database_lock.acquire()
                x = cursor.execute(f"SELECT rowid FROM main WHERE uid = '{client_id}'").fetchall()
                database_lock.release()
                if x != []:
                    database_lock.acquire()
                    cursor.execute(f"UPDATE main SET keys = '{args[0]+','+args[1]}' WHERE rowid = '{x[0][0]}'")
                    conn.commit()
                    database_lock.release()
                    send_string('update_keys;True',client_id,cursor,client,True)
                    print(f'Succesfully updated keys to {args[0]},{args[1]}')
            else:  
                print(f'Error: command "{command}" not recognised ')
        except TimeoutError:
            try:
                database_lock.acquire()
                x = cursor.execute(f"SELECT outgoing_ciphertext FROM backlog WHERE recipient = '{client_id}'").fetchall()
                database_lock.release()
                if x == []:
                    raise Empty_Backlog
                print(f'x:{x}')
                for i in x:
                    print(f'Type:{type(i[0])},i:{i[0]}')
                    send_string(i[0],client_id,cursor,client,True)
                database_lock.acquire()
                cursor.execute(f"DELETE FROM backlog where recipient = '{client_id}'")
                database_lock.release()
            except Empty_Backlog:
                print(f'no messages for client with client_id: {client_id}')
            except Exception as ERROR:
                print(f'unknown Exception : {ERROR}')
        except ConnectionResetError or ValueError:
            print(f'connection with {address} Terminated\n due to either "ConnectionResetError" or "ValueError"')
            break
        except Exception as ERROR:
            print(f'unknown Exception : {ERROR}')

while True:
    client,address = s.accept()
    print(f'connection from {address}')
    t = threading.Thread(target =client_connection,args =(client,address,))
    t.start()
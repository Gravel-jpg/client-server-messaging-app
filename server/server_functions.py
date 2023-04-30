import json, os, linecache,socket
def crypt(base,exponent,mod):
    oldbase = base
    exponent = bin(exponent)
    for i in range(3,len(exponent)):
        if exponent[i] == '0':
            base = (base**2)%mod
        else:
            base = ((base**2)*oldbase)%mod
    return(base%mod)


here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, 'Sjson.json')


# def process_string(string):
#     print(f'precrypted:{string}')
#     with open(filename,'r') as f:
#         data = json.load(f)
#     string = int(string)
#     text = str(crypt(string,data['keys']['d'],data['keys']['n']))
#     print(f'crypted:{text}')
#     text = [text[i:i+2] for i in range(0, len(text), 2)]
#     translated = ''
#     for i in text:
#         translated += data['int_to_str'][i]
#     return translated

# def send_string(string,client_uid,cursor,c):
#     # find users keys
#     selected = cursor.execute(f"SELECT keys FROM main WHERE uid = '{client_uid}'").fetchall()
#     n,e = selected[0][0].split(',')[0],selected[0][0].split(',')[1]
#     # load shift cipher
#     with open(filename,'r') as f:
#         data = json.load(f)
#     Msg =  ''
#     # Shift
#     for i in string:
#         i = str(i)
#         x = str(data['str_to_int'][i])
#         Msg += x
#     # encrypt
#     text = crypt(int(Msg),int(e),int(n))
#     c.send(str(text).encode())

# Server Send
def send_string(string,client_uid,cursor,c,encoding):
    if encoding:
    # find users keys
        selected = cursor.execute(f"SELECT keys FROM main WHERE uid = '{client_uid}'").fetchall()
        n,e = selected[0][0].split(',')[0],selected[0][0].split(',')[1]
        # load shift cipher
        with open(filename,'r') as f:
            data = json.load(f)
        Msg =  ''
        # Shift
        for i in string:
            i = str(i)
            x = str(data['str_to_int'][i])
            Msg += x
        # encrypt
        text = crypt(int(Msg),int(e),int(n))
        buffer = len(text)
        c.send(buffer.encode())
        c.send(str(text).encode())
    else:
        buffer = len(string)
        c.send(buffer.encode())
        c.send(string.encode())

# Server Recv
def process_string(c):
    buffer = c.recv(4).decode()
    string = c.recv(buffer).decode()
    if ';' in string:
        return string
    else:
        print(f'precrypted:{string}')
        with open(filename,'r') as f:
            data = json.load(f)
        string = int(string)
        text = str(crypt(string,data['keys']['d'],data['keys']['n']))
        print(f'crypted:{text}')
        text = [text[i:i+2] for i in range(0, len(text), 2)]
        translated = ''
        for i in text:
            translated += data['int_to_str'][i]
        return translated




def update_json_keys(n,d):
    with open (filename,'r') as f:
        data = json.load(f)
    data['keys']['n'] = n
    data['keys']['d'] = d
    with open(filename,'w') as f:
        json.dump(data,f)

def process_string_pieces(args,client):
    mended_message = args[0][:-2]
    while True:
        i = process_string(client.recv(4096).decode())
        print(f'translated string:{i}')
        if i[-2:] != ';;':
            mended_message += i
            break
        else:
            mended_message += i[:-2]
    return mended_message



def split_string(string):
    length = len(string)
    strings = []
    while string != '':
        x = string[:100]
        strings.append(x +';;')
        string = string[100:]
    strings[-1] = strings[-1][:-2]
    return strings




def send_string_pieces(strings,client_uid,cursor,c):
    for i in strings:
        send_string(i,client_uid,cursor,c)
# an example application would look like send_string_pieces(split_string(f'whatever function needs keys{n},{e}')client_uid,cursor,client)
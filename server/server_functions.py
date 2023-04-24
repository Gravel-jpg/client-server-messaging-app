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


def process_string(string):
    with open(filename,'r') as f:
        data = json.load(f)
    string = int(string)
    text = str(crypt(string,data['keys']['d'],data['keys']['n']))
    text = [text[i:i+2] for i in range(0, len(text), 2)]
    translated = ''
    for i in text:
        translated += data['int_to_str'][i]
    return translated

def send_string(string,client_uid,cursor,c):
    selected = cursor.execute(f"SELECT keys FROM main WHERE uid = '{client_uid}'").fetchall()
    n,e = selected[0][0].split(',')[0],selected[0][0].split(',')[1]
    with open(filename,'r') as f:
        data = json.load(f)
    Msg =  ''
    for i in string:
        i = str(i)
        x = str(data['str_to_int'][i])
        Msg += x
    text = crypt(int(Msg),int(e),int(n))
    c.send(str(text).encode())

def update_json_keys(n,d):
    with open (filename,'r') as f:
        data = json.load(f)
    data['keys']['n'] = n
    data['keys']['d'] = d
    with open(filename,'w') as f:
        json.dump(data,f)

def process_string_pieces(args,client):
    mended_message = args[1]
    while True:
        x = process_string(client.recv(1024).decode())
        if x[-2:] != ';;':
            mended_message += x
            break
        else:
            mended_message += x
    return mended_message
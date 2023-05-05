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

# Server Send
def send_string(string,client_uid,cursor,c,encoding):
    if encoding:
    # find users keys
        selected = cursor.execute(f"SELECT keys FROM main WHERE uid = '{client_uid}'").fetchall()
        n,e = selected[0][0].split(',')[0],selected[0][0].split(',')[1]
        # load shift cipher
        with open(filename,'r') as f:
            data = json.load(f)
        strings = split_string(string)
        for i in strings:
            Msg = ''
            for j in i:
                x = str(data['str_to_int'][str(j)])
                Msg += x
            text = str(crypt(int(Msg),int(e),int(n)))
            buffer = str(len(text)).rjust(4,'0')
            print(f'send buffer:{buffer}')
            c.send(buffer.encode())
            print(f'send text:{text}')
            c.send(text.encode())
    else:
        buffer = str(len(string)).rjust(4,'0')
        c.send(buffer.encode())
        c.send(string.encode())

# Server Recv
def process_string(c):
    buffer = int(c.recv(4).decode())
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
        print(f'translated:{translated}')
        if translated[-2:] == ';;':
            mended_message = translated[:-2]
            print(f'Mended_message:{mended_message}')
            while True:
                buffer = int(c.recv(4))
                print(f'buffer:{buffer}')
                i = int(c.recv(buffer))
                print(f'precrypted recieved:{i}')
                i = str(crypt(i,data['keys']['d'],data['keys']['n']))
                i = [i[j:j+2] for j in range(0,len(i),2)]
                Msg = ''
                for j in i:
                    Msg += data['int_to_str'][j]
                
                print(f'Part:{Msg}')
                if Msg[-2:] != ';;':
                    mended_message += Msg
                    break
                else:
                    mended_message += Msg[:-2]
            print(f'Whole message:{mended_message}')
            return mended_message
        else:
            return translated

def update_json_keys(n,d):
    with open (filename,'r') as f:
        data = json.load(f)
    data['keys']['n'] = n
    data['keys']['d'] = d
    with open(filename,'w') as f:
        json.dump(data,f)

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
        send_string(i,client_uid,cursor,c,True)
# an example application would look like send_string_pieces(split_string(f'whatever function needs keys{n},{e}')client_uid,cursor,client)
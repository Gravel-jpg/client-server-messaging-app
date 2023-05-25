import json, linecache, random, os

def crypt(base,exponent,mod):
    oldbase = base
    exponent = bin(exponent)
    for i in range(3,len(exponent)):
        if exponent[i] == '0':
            base = (base**2)%mod
        else:
            base = ((base**2)*oldbase)%mod
    return(base%mod)

def generate_keys():
    p = random.randint(1,44)
    q = random.randint(1,44)
    p = linecache.getline('300 digit primes.txt',p)
    q = linecache.getline('300 digit primes.txt',q)
    while p == q:
        q = random.randint(1,44)
        q = linecache.getline('300 digit primes.txt',q)
    p,q = int(p), int(q)
    n = p*q
    m = (p-1)*(q-1)
    e = 65537
    gen1 = [1,0,e,None]
    gen2 = [0,1,m,None]
    gen3 = [None,None,None,None]
    while True:
        gen3[3] = int((gen1[2]//gen2[2]))
        gen3[0] = gen1[0] - (gen2[0]*gen3[3])
        gen3[1] = gen1[1] - (gen2[1]*gen3[3])
        gen3[2] = gen1[2] - (gen2[2]*gen3[3])
        if gen3[2] == 0:
            break
        gen1 = gen2.copy()
        gen2 = gen3.copy()
    d = gen2[0]+m
    return int(n),int(d),int(e)

here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, 'Cjson.json')

# Client Send
def send_string(string,s,n,e,encoding):
    if encoding:
        with open(filename,'r') as f:
            data = json.load(f)
        strings = split_string(string)
        for i in strings:
            Msg = ''
            for j in i:
                Msg += str(data['str_to_int'][j])
            text = str(crypt(int(Msg),int(e),int(n)))
            buffer = str(len(text)).rjust(4,'0')
            s.send(buffer.encode())
            s.send(text.encode())
    else:
        buffer = str(len(string)).rjust(4,'0')
        s.send(buffer.encode())
        s.send(string.encode())

# Client recv
def process_string(s):
    buffer = int(s.recv(4).decode())
    string = s.recv(buffer).decode()
    if ';' in string:
        return string
    else:
        with open(filename,'r') as f:
            data = json.load(f)
        string = int(string)
        text = str(crypt(string,data['keys']['d'],data['keys']['n']))
        text = [text[i:i+2] for i in range(0, len(text), 2)]
        translated = ''
        for i in text:
            translated += data['int_to_str'][i]
        if translated[-2:] == ';;':
            mended_message = translated[:-2]
            while True:
                buffer = int(s.recv(4))
                i = int(s.recv(buffer))
                i = str(crypt(i,data['keys']['d'],data['keys']['n']))
                i = [i[j:j+2] for j in range(0,len(i),2)]
                Msg = ''
                for j in i:
                    Msg += data['int_to_str'][j]
                if Msg[-2:] != ';;':
                    mended_message += Msg
                    break
                else:
                    mended_message += Msg[:-2]
            return mended_message
        return translated

def update_json_keys(n,d):
    with open (filename,'r') as f:
        data = json.load(f)
    data['keys']['n'] = n
    data['keys']['d'] = d
    with open(filename,'w') as f:
        json.dump(data,f)
        
# This function breaks down an input string into multiple smaller segments, all of which are to be translated and sent individually.
# This is in order to avoid breaking the character limit of the rsa algorithm 
def split_string(string):
    # length = len(string) Possible useless line if it is remove it in server_functions as well.
    strings = []
    while string != '':
        x = string[:100]
        strings.append(x +';;')
        string = string[100:]
    strings[-1] = strings[-1][:-2]
    return strings

# Implement this later maybe to cut down on repeated lines
# This function turns characters into an int for the purpose of locally encrypting/decrypting a users messages
# def shift(inp,n,e,dict):
#     with open(filename,'r') as f:
#         data = json.load(f)
#         strings = split_string(inp)
#         for i in strings:
#             Msg = ''
#             for j in i:
#                 Msg += str(data[dict][j])
#             text = str(crypt(int(Msg),int(e),int(n)))
#             return text
#     elif dict == '':
# pass
        
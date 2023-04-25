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
    return str(n),str(d),str(e)

here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, 'Cjson.json')

#encrypts outgoing messages using servers provided public key
def send_string(string,s,n ,e):
    with open(filename,'r') as f:
        data = json.load(f)
    Msg =  ''
    for i in string:
        i = str(i)
        x = str(data['str_to_int'][i])
        Msg += x
    text = crypt(int(Msg),int(e),int(n))
    print(f'sent:{text}')
    s.send(str(text).encode())

#decrypts incoming messages locally using own private key
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

def send_string_pieces(strings,s,n,e):
    for i in strings:
        send_string(i,s,n,e)

def process_string_pieces(args,s):
    mended_message = args[1]
    while True:
        x = process_string(s.recv(1024).decode())
        if x[-2:] != ';;':
            mended_message += x
            break
        else:
            mended_message += x[:-2]
    return mended_message
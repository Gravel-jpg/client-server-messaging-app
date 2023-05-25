import json
#Will encrypt string, filter impossible characters, and then send it
def crypt(base,exponent,mod):
    oldbase = base
    exponent = bin(exponent)
    for i in range(3,len(exponent)):
        if exponent[i] == '0':
            base = (base**2)%mod
        else:
            base = ((base**2)*oldbase)%mod
    return(base%mod)




def send_string(string,s,n ,e):
    with open('json.json','r') as f:
        data = json.load(f)
    Msg =  ''
    for i in string:
        x = data['str_to_int'][i]
        Msg += x
        Msg = int(Msg)
    text = crypt(Msg,)
    
    
    
#every character in string is lowered, cant eval true. maybe allow for upper case characters to be sent in dictionary?

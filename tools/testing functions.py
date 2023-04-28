# import json, os, linecache
# Original_message = 'update_keys;402589019676744063899831551574076740886205075517654560684618008841217280866980616137203592633581480782376371723375590275003977997402199204701216462543801319007142606429196269472512617229338103494993390279119370528352036884258397396766819792800581032694861035024110148298818886271002172781293724298666134123449801631939139707551973682512533710160234159416322336031570932803491074281521134479163624099003774130314380550222849874375860794840590620572445949112289238026236618742332712423234789281826319738720876807038884159170031489988928310902871346774744045449108626340823908728218995883237662598017623,317976340472211162849184134216227998512178362207918473911193402072843281039985315670690900796375760100983385408503451171170955537780643566732518542970456195366994563934792353887203726225524943943289178037109662887515243072460860650454566015147725345917330542379922999319342692067776759230329539815246177899536800873635365612262602639423488619303075936292572033191500876372464746441725833149142620351334446765130684169973655785266960377472746981287924061125961597451051524287155651100318232811922479420566581396477286581718543569085984676802143213602698578833357897146383218576180773734621623014777593'


# def crypt(base,exponent,mod):
#     oldbase = base
#     exponent = bin(exponent)
#     for i in range(3,len(exponent)):
#         if exponent[i] == '0':
#             base = (base**2)%mod
#         else:
#             base = ((base**2)*oldbase)%mod
#     return(base%mod)

# here = os.path.dirname(os.path.abspath(__file__))
# filename = os.path.join(here, 'Sjson.json')
# # not calling this func at the right place
# def process_string(string):
#     with open(filename,'r') as f:
#         data = json.load(f)
#     string = int(string)
#     text = str(crypt(string,data['keys']['d'],data['keys']['n']))
#     text = [text[i:i+2] for i in range(0, len(text), 2)]
#     translated = ''
#     for i in text:
#         translated += data['int_to_str'][i]
#     return translated
# # Try to get this func working in the context of this file. just aiming to text encryption/deceyption without any socket issues

# # Version for testing
# def process_string_pieces(messages):
#     mended_message = ''
#     for i in messages:
#         i = process_string(i)
#         if i[-2:] != ';;':
#             mended_message += i
#             break
#         else:
#             # add the string but remove the last two digits (';;')
#             mended_message += i[:-2]
#     return mended_message
# # Version for live recieving
# def process_string_pieces(args,client):
#     mended_message = args[0]
#     while True:
#         i = process_string(client.recv(1024).decode())
#         if i[-2:] != ';;':
#             mended_message += i
#             break
#         else:
#             mended_message += i[:-2]
#     return mended_message

# def split_string(string):
#     length = len(string)
#     strings = []
#     while string != '':
#         x = string[:100]
#         strings.append(x +';;')
#         string = string[100:]
#     strings[-1] = strings[-1][:-2]
#     return strings

# def send_string(string):
#     with open(filename,'r') as f:
#         data = json.load(f)
#     Msg =  ''
#     for i in string:
#         i = str(i)
#         x = str(data['str_to_int'][i])
#         Msg += x
#     text = crypt(int(Msg),65537,int(data['keys']['n']))
#     return str(text)




# # take big message
# # split into little
# messages = split_string(Original_message)
# print(f'Step One: {messages}')
# encrypted_messages = []
# for i in messages:
#     # encrypt little
#     encrypted_messages.append(send_string(i))
# print(f'Step Two: {encrypted_messages}')
# # process ittle, piece together little
# Final_message = process_string_pieces(encrypted_messages)
# # do big message
# print(f'-----------\n{Final_message}')
# # Grofit!








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
# Client recv
def process_string(s):
    buffer = s.recv(4).decode()
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
        return translated
# Client Send
def send_string(string,s,n ,e,encoding):
    if encoding:
        with open(filename,'r') as f:
            data = json.load(f)
        Msg =  ''
        for i in string:
            i = str(i)
            x = str(data['str_to_int'][i])
            Msg += x
        print(f'string:{string}')
        text = crypt(int(Msg),int(e),int(n))
        print(f'sent:{text}')
        print(f'length:{len(str(text))}')
        buffer = len(text)
        s.send(buffer.encode())
        s.send(str(text).encode())
    else:
        buffer = len(string)
        s.send(buffer.encode())
        s.send(string.encode())




# List of every .send and .recv that need to be replaced

# Client
# Upload_Account, line 114 (.send) -Encoding = True
# Upload_Account, line 115 (if eval .recv)
# Login_Function, line 66 (x = .recv) 
# Upload_Keys, line 13 (x = .recv) 
# Main, line 160 (n,e = .recv) 


# Server
# client_connection, line 24 ({keys} .send) -Encoding = False
# client_connection, line 27 (Server_Recv = .recv)
# login_attempt, line 46 ('login_attempt;False'.send) -Encoding = False (should be set to true once this is done)
# key_request, line 54 (keys.send) -Encoding = True (multiple strings, simple stuff to be completed first)
# key_request, line 57 ('key_request;False'.send) -Encoding = True
# create_acc, line 64 ('create_acc;False'.send) -Encoding = True
# create_acc, line 70 ('create_acc;True'.send) -Encoding = True

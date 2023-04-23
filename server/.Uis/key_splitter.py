from client_functions import *
ciphertext = '143048841911415197001690017211194681238051502165655683179110968652092350299688753827576316756314021249972242410940286988082510672331691482014616586582943296189118314803714964886367255776970181089902986437210367164768919144399794156535151845310894294257765450995540218798530186100944465172881445277343659251775448198817234521772116120905042270098120890511096613537672304628286230511374648094911006729507078502551924549891128255387564234928140773391033379433132318029319087681953152887355546930848428498109079150050075627551974206007078198068705884336801149020041680369288225099368351092371535446568018'
#Client function, most likely universal! Turns huge string into pieces, returns list of strings to be sent
def split_string(ciphertext):
    length = len(ciphertext)
    strings = []
    while ciphertext != '':
        x = ciphertext[:100]
        strings.append(x +';;')
        ciphertext = ciphertext[100:]
    strings[-1] = strings[-1][:-2]
    return strings
#combines a list of pieces of cipher into a complete string of ciphertext

def mend_string(ciphertext):
    combine = ''
    for i in ciphertext:
        combine += i
    return combine
#Client function, sends strings in pieces
def send_string_pieces(strings,c,n,e):
    for i in strings:
        send_string(i,c,n,e)
x = split_string(ciphertext)
print(x[-1:])
#Server function, need an alternative for client when recieving keys from server
def process_string_pieces(args,client):
    mended_message = args[1]
    while True:
        x = process_string(client.recv(1024).decode())
        mended_message += x
        if mended_message[-2:] != ';;':
            break
    return mended_message
#Test github changes
import json
import socket

# Configuration stuff
HOST = '35.197.236.148'  
PORT = 9877              
PLAYER = 'teamath'


# Returns the length of the string in the appropriate format
def payload_len(s):
    return bytearray(len(s).to_bytes(4, "little"))

# Send the json payload to the server. Returns the server response as a dict
def send_json(s, json_str):
    prefix = payload_len(json_str)
    s.send(prefix)
    s.send(json_str.encode())
    msg_length = int().from_bytes(s.recv(4), "little")
    msg = s.recv(msg_length)

    return json.loads(msg.decode())

# Login to the server
def login(s, tourney=False):
    login = {
        'type' : 'login',
        'player' : PLAYER,
        'tournament': tourney
    }
    login_str = json.dumps(login)
    
    return send_json(s, login_str)



# Connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

r = login(s)

print(r)

def game_engine(s):
    while True:
        # Listen to the server for message
        response_length = int().from_bytes(s.recv(4), "little")
        response = json.loads(s.recv(msg_length))


        if response['type'] == 'auction':
            send_auction_resp()
        elif response['type'] == 'bet':
            send_bet_resp()
        else:
            'etc'


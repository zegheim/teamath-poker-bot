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


def send_auction(s, response, superpower, bid):
    auc_resp = {
        'type' : 'auction_response',
        'token' : response['token']
    }

    if superpower is not None:
        auc_resp['superPower'] = superpower
        auc_resp['bid'] = bid

    auc_resp_str = json.dumps(auc_resp)
    
    return send_json(s, auc_resp_str)

def send_bet(s, response, status, stake):
    bet_resp = {
        'type' : 'bet_response',
        'token': response['token'],
        'action': decide_action(),
        'useReserve': False
    }

    if bet_resp['action'] == 'raise':
        bet_resp['stake'] = stake
    
    bet_resp_str = json.dumps(bet_resp)

    return send_json(s, bet_resp_str)


def decide_action():
    return 'call'


def game_engine(s):
    status = {}
    summary = {}
    while True:
        # Listen to the server for message
        response_length = int().from_bytes(s.recv(4), "little")
        response = json.loads(s.recv(response_length))

        if response['type'] == 'status':
            status = response
            print('Status: {}'.format(status))
        elif response['type'] == 'auction':
            print('Auction result: {}'.format(send_auction(s, response, None, None)))
        elif response['type'] == 'bet':
            print('Bet result: {}'.format(send_bet(s, response, status, 100)))
        elif response['type'] == 'summary':
            summary = response
            print('Summary: {}'.format(summary))
        else:
            print('Response: {}'.format(response))

# Connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

r = login(s)

print(r)

game = game_engine(s)





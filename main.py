import json
import logging
import socket

# Configuration stuff
HOST = '35.197.236.148'  
PORT = 9877              
PLAYER = 'teamath'
FORMAT = '%(asctime)s.%(msecs)03d %(levelname)-5s - %(message)s'
DATE_FORMAT = '%m/%d/%Y %H:%M:%S'

logging.basicConfig(level=logging.DEBUG,
                    format=FORMAT,
                    datefmt=DATE_FORMAT,
                    filename='game.log',
                    filemode='w')

# Returns the length of the string in the appropriate format
def payload_len(s):
    return bytearray(len(s).to_bytes(4, "little"))

# Send the json payload to the server. Returns the server response as a dict
def send_json(s, json_str):
    # Tell the server the length of payload to expect
    prefix = payload_len(json_str)
    s.send(prefix)
    
    # Send the expected payload
    s.send(json_str.encode())
    logging.debug('Sent: %s', json_str)

    # Receive the server's response
    msg_length = int().from_bytes(s.recv(4), "little")
    msg = s.recv(msg_length)
    logging.debug('Received: %s', msg.decode())

    return json.loads(msg.decode())

# Login to the server
def send_login(s, tourney=False):
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
        'action': decide_action(status),
        'useReserve': False
    }

    if bet_resp['action'] == 'raise':
        bet_resp['stake'] = stake
    
    bet_resp_str = json.dumps(bet_resp)

    return send_json(s, bet_resp_str)


def decide_action(status):
    card_ranks = []
    for card in status['pocketCards']:
        card_ranks.append(card['rank'])

    for card in status['communityCards']:
        card_ranks.append(card['rank'])

    if len(card_ranks) != len(set(card_ranks)):
        return 'call'
    else:
        return 'fold'
    

def game_engine():
    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # Login to the lobby
    send_login(s)

    # Initialise status and summary dicts
    status = {}
    summary = {}

    while True:
        # Listen to the server for message
        response_length = int().from_bytes(s.recv(4), "little")
        response = json.loads(s.recv(response_length))
        logging.debug('Received: %s', response)

        # Handle different types of messages
        if response['type'] == 'status':
            status = response
        elif response['type'] == 'auction':
            send_auction(s, response, None, None)
        elif response['type'] == 'bet':
            send_bet(s, response, status, 100)
        elif response['type'] == 'summary':
            summary = response
                

# Run the game
game_engine()





import json

from logger import logger

import game_logic

# Send the json payload to the server. Returns the server response as a dict
def send_json(s, json_str):
    # Tell the server the length of payload to expect
    prefix = bytearray(len(json_str).to_bytes(4, "little"))
    s.send(prefix)
    
    # Send the expected payload
    s.send(json_str.encode())
    logger.debug('Sent: %s', json_str)

    # Receive the server's response
    msg_length = int().from_bytes(s.recv(4), "little")
    msg = s.recv(msg_length)
    logger.debug('Received: %s', msg.decode())

    return json.loads(msg.decode())


# Login to the server
def send_login(s, tourney=False):
    login = {
        'type' : 'login',
        'player' : 'teamath',
        'tournament': tourney
    }

    login_str = json.dumps(login)
    
    return send_json(s, login_str)


# Send auction response to the server
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


# Send bet response to the server
def send_bet(s, response, status, stake):
    bet_resp = {
        'type' : 'bet_response',
        'token': response['token'],
        'action': game_logic.decide_action(status),
        'useReserve': False
    }

    if bet_resp['action'] == 'raise':
        bet_resp['stake'] = stake
    
    bet_resp_str = json.dumps(bet_resp)

    return send_json(s, bet_resp_str)
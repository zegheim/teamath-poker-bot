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
    with open('game.message', 'w') as f:
        while True:
            # Listen to the server for message
            response_length = int().from_bytes(s.recv(4), "little")
            response = json.loads(s.recv(response_length))

            if response['type'] == 'status':
                status = response
                title = 'Status (Hand: {})\n'.format(status['hand'])
                f.write(title)
                f.write('-' * len(title))

                f.write('\n\nPot size: {}\n'.format(status['pot']))
                f.write('Current stake: {}\n\n'.format(status['stake']))

                f.write('Our cards\n')
                f.write('---------\n')
                for card in status['pocketCards']:
                    f.write('{} of {}\n'.format(card['rank'], card['suit']))

                f.write('Community cards\n')
                f.write('---------------\n')
                for card in status['communityCards']:
                    f.write('{} of {}\n'.format(card['rank'], card['suit']))
                    
                f.write('Superpowers\n')
                f.write('-----------\n')
                for power in status['superPowers']:
                    f.write('{}: {}\n'.format(power, status['superPowers'][power]))
                
                f.write('Players\n')
                f.write('-------\n')
                for idx, player in enumerate(status['activePlayers']):
                    f.write('Player #{}\n'.format(idx + 1))
                    f.write('---------\n')
                    f.write('Player ID: {}\n'.format(player['playerId']))
                    f.write('Stake: {}\n'.format(player['stake']))
                    f.write('Folded? :{}\n'.format(player['folded']))
                    f.write('# of chips: {}\n'.format(player['chips']))
            elif response['type'] == 'auction':
                f.write('\nWon: {} from auction\n'.format(send_auction(s, response, None, None)['superPower']))
            elif response['type'] == 'bet':
                send_bet(s, response, status, 100)
                print('\nSent bet.\n')
            elif response['type'] == 'summary':
                summary = response
                f.write('Summary for Hand #{}\n'.format(summary['hand']))
                f.write('--------------------\n')
                for idx, winner in enumerate(summary['winners']):
                    f.write('Player ID: {}\n'.format(winner['playerId']))
                    f.write('# of chips won: {}\n'.format(winner['chips']))
                    f.write('Best hand: {}\n'.format(winner['bestHand']))
            else:
                print('Response: {}'.format(response))

# Connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

login_response = login(s)

with open('login.details', 'w') as f:
    f.write('Player ID: {}\n'.format(login_response['playerId']))
    f.write('# of chips: {}\n'.format(login_response['chips']))

    f.write('\nSuperpowers\n')
    f.write('-----------\n')
    for power in login_response['superPowers']:
       f.write('{}: {}\n'.format(power, login_response['superPowers'][power]))

    f.write('\nSuperpowers reserve\n')
    f.write('-------------------\n')
    for power in login_response['superPowersReserve']:
       f.write('{}: {}\n'.format(power, login_response['superPowersReserve'][power]))

    f.write('\nChips\' reserve: {}\n'.format(login_response['chipsReserve']))
    f.write('Tournament scores: {}\n'.format(login_response['tournamentsScores']))


game = game_engine(s)





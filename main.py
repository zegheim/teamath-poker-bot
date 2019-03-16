import json
import socket
import sys

from logger import logger
from sender import send_auction, send_bet, send_login

# Configuration settings
HOST = '35.197.236.148'  
PORT = 9877              


# Main game engine
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
        try:
            response = json.loads(s.recv(response_length))
        except json.decoder.JSONDecodeError as e:
            logger.error(e)
            sys.exit(1)
        logger.debug('Received: %s', json.dumps(response, indent=4))

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





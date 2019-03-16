from treys import Card, Evaluator
# Decide what action to take

def decide_action(status):
    hand = []
    board = []
    pocket_cards = status['pocketCards']
    common_cards = status['communityCards']

    for card in pocket_cards:
        if card['rank'] == "10":
            rank = "T"
        elif len(card['rank']) > 1:
            rank = card['rank'][0].upper()
        else:
            rank = card['rank']
        
        suit = card['suit'][0]
        hand.append(Card.new('{}{}'.format(rank, suit)))
    
    for card in common_cards:
        if card['rank'] == "10":
            rank = "T"
        elif len(card['rank']) > 1:
            rank = card['rank'][0].upper()
        else:
            rank = card['rank']
        
        suit = card['suit'][0]
        board.append(Card.new('{}{}'.format(rank, suit)))
    
    return 'call'
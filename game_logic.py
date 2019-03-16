# Decide what action to take
def decide_action(status):
    if len(status['communityCards']) == 0:
        return 'call'
    else:
        return 'fold'
    
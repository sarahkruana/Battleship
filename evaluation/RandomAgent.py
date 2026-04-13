import random

class RandomAgent:

    '''
    Constructs just a basic agent that randomly picks an open cell to attack
    '''
    def __init__(agent):
        pass

    '''
    Picks a random open cell to attack
    Returns (tuple[int, int]) representing the chosen (row, col)
    @param opponentBoard (Board) represents the opponent's board
    '''
    def chooseAttack(agent, opponentBoard):
        avail = []

        for row in range(opponentBoard.size):
            for col in range(opponentBoard.size):

                if (row, col) not in opponentBoard.attacks:
                    avail.append((row,col))

        return random.choice(avail)
import random
from model.Player import Player
from model.MonteCarloAgent import MonteCarloAgent

class AIPlayer(Player):

    '''
    Constructor to create the AI player. Inherits everything from the standard player class
    and adds AI-specific behavior 
    @param name (str) represents the name of the AI player
    @param size (int) represents the size of the board
    '''
    def __init__(ai, name, size):
        super().__init__(name, size)
        ai.agent = MonteCarloAgent(simulations=1000)

    '''
    Places all of the ships randomly on the board. For each ship, it will pick the first 
    valid location that it gets.
    '''
    def placeShipsRand(ai):
        for ship in ai.fleet:
            havePlaced = False
            while not havePlaced:
                pos = ai.generatePos(ship.size)
                havePlaced = ai.board.placeShip(ship, pos)
    
    '''
    Generates a randome list of positions for a designated ship size. Picks a random starting
    cell and a random direction then builds a list
    Returns (list[tuple[int, int]]) representing the positins picked
    @param size (int) represents the size of the ship
    '''
    def generatePos(ai, size):
        direction = random.choice(["hori", "vert"])
        
        if direction == "hori":
            row = random.randint(0, ai.board.size - 1)
            col = random.randint(0, ai.board.size - size)
            pos = [(row, col + i) for i in range(size)]
        else:
            row = random.randint(0, ai.board.size - size)
            col = random.randint(0, ai.board.size - 1)
            pos = [(row + i, col) for i in range(size)]

        return pos
    
    '''
    Chooses a random cell to attack using the Monte Carlo agent. Will pass through the opponent's
    board and unsunk ships so that the agent can build a probability map for best targets
    Returns a position (tuple[int, int]) representing the chosen (row, col)
    @param opponentBoard (Board) represents the opponent's board
    '''
    def chooseAttack(ai, opponentBoard):
        unsunk = [ship for ship in opponentBoard.ships if not ship.isSunk()]

        return ai.agent.chooseAttack(opponentBoard, unsunk)

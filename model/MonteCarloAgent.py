import random
from model.Board import Board

class MonteCarloAgent:

    '''
    Contructor to initializae the Monte Carlo agent with a set number of simulations
    @param simulations (int) represents how many random boards to simulate per turn
    '''
    def __init__(agent, simulations = 1000):
        agent.simulations = simulations


    '''
    Picks the best cell to attack based on what we know from the probability map
    Picks the unattacked cell with the highest probability (decision threshold)
    Returns the cell (tuple[int,int]) that represents the chosen (row, col)
    @param opponentBoard (Board) represents the opponents board
    @param unsunk (list[Ship]) represents the ships still in play
    '''
    def chooseAttack(agent, opponentBoard, unsunk):
        probMap = agent.probabilityMap(opponentBoard, unsunk)

        minUnsunk = min(ship.size for ship in unsunk)
        agent.applyFilter(probMap, opponentBoard, minUnsunk)

        bestCell = None
        bestProb = -1

        for row in range(opponentBoard.size):
            for col in range(opponentBoard.size):
                if (row, col) not in opponentBoard.attacks:
                    if probMap[row][col] > bestProb:
                        bestProb = probMap[row][col]
                        bestCell = (row, col)
        
        return bestCell

    '''
    Actually builds the probability map of the opponents board. For each simulation, the remaining 
    ships that haven't been sunk yet are randomly placed on the board (respecting what we alr know 
    eg: misses are blocked, hits must be covered)
    then, each cell will accumulate a count representing how often a ships lands there across the sims.
    Then it gives us a probability that represents the cells count divided by total simulations

    Returns (list[list[float]]) that represents a 2d grid where each cells value represents it's 
    probability that it contains a ship
    @param opponentBoard (Board) represents the opponen'ts board
    @param unsunk (list[Ship]) represents the ships that haven't been sunk yet
    '''
    def probabilityMap(agent, opponentBoard, unsunk):
        counts = [[0 for _ in range(opponentBoard.size)] for _ in range(opponentBoard.size)]
        successfulSims = 0

        for _ in range(agent.simulations):
            simGrid = agent.runSim(opponentBoard, unsunk)

            if simGrid is None:
                continue

            for row in range(opponentBoard.size):
                for col in range(opponentBoard.size):
                    if simGrid[row][col]:
                        counts[row][col] += 1
            
            successfulSims += 1
            
            probMap = [[0.0 for _ in range(opponentBoard.size)] for _ in range(opponentBoard.size)]
            if successfulSims > 0:
                for row in range(opponentBoard.size):
                    for col in range(opponentBoard.size):
                        probMap[row][col] = counts[row][col] / successfulSims
        
        return probMap
    

    '''
    Runs one simulation by placing the rest of the unsunk ships randomly on a copy of the board.
    Returns (list[list[bool]]) representing a 2d grid where True means that a ship occupies the cell
    or returns None if the simulation failed to place the ships respecting what we already know
    @param opponentBoard (Board) represents the opponent's board
    @param unsunk (list[Ship]) represents the ships that haven't been sunk yet
    '''
    def runSim(agent, opponentBoard, unsunk):
        size = opponentBoard.size
        simGrid = [[False for _ in range(size)] for _ in range(size)]

        for ship in opponentBoard.ships:
            if ship.isSunk():
                for row, col in ship.positions:
                    simGrid[row][col] = True

        for ship in unsunk:
            havePlaced = False
            attempts = 0

            while not havePlaced and attempts < 100:
                attempts += 1
                pos = agent.generatePos(ship.size, size)

                if agent.isValid(pos, opponentBoard, simGrid):
                    for row, col in pos:
                        simGrid[row][col] = True
                    havePlaced = True
            
            if not havePlaced:
                return None
        
        for row in range(size):
            for col in range(size):
                if opponentBoard.grid[row][col] == Board.HIT:
                    if not simGrid[row][col]:
                        return None

        return simGrid
    

    '''
    Checks if a set of pos is valid. Its invalid if it lands on something thats already known
    (eg. lands on a miss or a misses a hit) or if it overlaps with another ship that's 
    already been placed. 
    Returns (boolean) represetning if it is valid or not
    @param pos (list[tuple[int,int]]) represents the proposes positions
    @param opponentBoard (Board) represents the opponents board
    @param simGrid (list[list[bool]]) represents teh current simulation's placed ships
    '''
    def isValid(agent, pos, opponentBoard, simGrid):
        for row, col in pos:
            if opponentBoard.grid[row][col] == Board.MISS:
                return False
            if simGrid[row][col]:
                return False
            
        return True
    

    '''
    Generates a randome list of positions for a designated ship size. Picks a random starting
    cell and a random direction then builds a list
    Returns (list[tuple[int, int]]) representing the positins picked
    @param shipSize (int) represents the size of the ship
    @param boardSize represents the size of the board
    '''
    def generatePos(agent, shipSize, boardSize):
        direction = random.choice(["hori", "vert"])
        
        if direction == "hori":
            row = random.randint(0, boardSize - 1)
            col = random.randint(0, boardSize - shipSize)
            pos = [(row, col + i) for i in range(shipSize)]
        else:
            row = random.randint(0, boardSize - shipSize)
            col = random.randint(0, boardSize - 1)
            pos = [(row + i, col) for i in range(shipSize)]

        return pos
    
    '''
    Looks at the probability map to filter impossible locations. 
    (eg if a spot has no open neibors up, down,left, or right then it's impossible 
    to fit the smallest unsunk ship and its probability would be 0). 
    @param probMap (list[list[float]]) represents the porbability map
    @param opponentBoard (Board) represents the opponent's board
    @param minUnsunk (int) represents the size of the smallest unsunk ship
    '''
    def applyFilter(agent, probMap, opponentBoard, minUnsunk):
        for row in range(opponentBoard.size):
            for col in range(opponentBoard.size):
                if (row, col) in opponentBoard.attacks:
                    continue

                fitsHori = False
                for start in range(col - minUnsunk + 1, col + 1):
                    if start < 0 or start + minUnsunk > opponentBoard.size:
                        continue
                    if all(
                        opponentBoard.grid[row][start + i] != Board.MISS and
                        (row, start + i) not in opponentBoard.attacks
                        for i in range(minUnsunk)
                    ):
                        fitsHori = True
                        break
 
                fitsVert = False
                for start in range(row - minUnsunk + 1, row + 1):
                    if start < 0 or start + minUnsunk > opponentBoard.size:
                        continue
                    if all(
                        opponentBoard.grid[start + i][col] != Board.MISS and
                        (start + i, col) not in opponentBoard.attacks
                        for i in range(minUnsunk)
                    ):
                        fitsVert = True
                        break
 
                if not fitsHori and not fitsVert:
                    probMap[row][col] = 0.0


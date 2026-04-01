from model.Board import Board
from model.Ship import Ship
from model.Player import Player

class BattleshipGame:

    '''
    Basic constructor to initialize a game
    @param redPlayer (str) is a string representing the name of the first player
    @param bluePlayer (str) is a string representing the name of the second player 
    @param size (int) represents teh designated board size. 
    The model does not handle size restrictions
    '''
    def __init__(game, redPlayer, bluePlayer, size):
        game.size = size
        game.redPlayer = Player(redPlayer, size)
        game.bluePlayer = Player(bluePlayer, size)
        game.current = 0
        game.winner = None
        game.started = False
    
    '''
    Returns the player that whose current turn is on
    '''
    def getCurrent(game) -> Player:
        if game.current % 2 == 0:
            return game.redPlayer
        else:
            return game.bluePlayer
        
    '''
    Returns whatever the opponent of the current player is
    '''
    def getOpponent(game) -> Player:
        if game.getCurrent() == game.redPlayer:
            return game.bluePlayer
        else:
            return game.redPlayer

    '''
    Places a single ship on the board. If the game has already been started,it throws an error
    @param player (Player) represents the player whose board the ship is getting placed onto
    @param ship (Ship) represents the designated ship to be placed
    @param positions (list[tuple[int, int]]) represents the list of positions to place the ship on
    @returns (boolean) whether or not the ship was able to be placed
    '''
    def placeShip(game, player, ship, positions) -> bool:
        if game.checkStarted("notStarted") == False:
            raise RuntimeError("Game has already been started")
        
        return player.board.placeShip(ship, positions)
    
    '''
    Returns (boolean) if all of the designated players ships have been placed
    @param player (Player) represents the player whose fleet placement is being checked
    '''
    def allPlaced(game, player) -> bool:
        return player.board.allPlaced(player.fleet)
    
    '''
    'Starts' the game. Checks if either the game has already been started, 
    or if either players fleet is not entirely placed
    '''
    def gameStart(game):
        if game.checkStarted("notStarted") == False:
            raise RuntimeError("Game has already been started")

        if game.allPlaced(game.redPlayer) == False:
            raise RuntimeError("redPlayer has not placed all ships")
        if game.allPlaced(game.bluePlayer) == False:
            raise RuntimeError("bluePlayer has not placed all ships")
        
        game.started = True

    '''
    Attacks the opponent of the current player at a designated location. 
    Updates the current player after each turn is taken
    @param row (int) represents the row of the designated location
    @param col (int) represents the col of the designated location
    @returns (str) what happened (miss, sunk, hit, etc)
    '''
    def attack(game, row, col) -> str:
        attackResult = game.getOpponent().board.attacked(row, col)

        if attackResult == "sunk":
            if game.getOpponent().board.allSunk() == True:
                game.winner = game.getCurrent()

        game.current += 1
        return attackResult
    
    '''
    Returns (int) the total amount of sunken ships for a player.
    @param player represents the designated player
    '''
    def totalAttacks(game, player) -> int:
        score = 0
        for ship in player.fleet:
            if ship.isSunk():
                score += ship.size

        return score

    '''
    Returns (boolean) if the game is over. Also updates who won the game. 
    The game is over when a players entire fleet is sunk.
    '''
    def isOver(game) -> bool:
        if game.redPlayer.board.allSunk():
            game.winner = game.bluePlayer
            return True
        if game.bluePlayer.board.allSunk():
            game.winner = game.redPlayer
            return True
        return False

    '''
    Returns (boolean) whether or not the game has been started.
    @param flag (str) designates the state of the game at the time of the method call
    '''
    def checkStarted(game, flag) -> bool:
        if flag == "notStarted" and game.started == True:
            return False
        if flag == "started" and game.started == False:
            return False
        
        return True

    

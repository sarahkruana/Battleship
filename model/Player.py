from model.board import Board
from model.ship import createShips

class Player:
    '''
    Constructor to create a basic player
    @param name (str) represents the name of the player
    @param size (int) represents the size of the board.
    Does not need to handle invalid inputs
    '''
    def __init__(player, name, size):
        player.name = name
        player.board = Board(size)
        player.fleet = createShips()
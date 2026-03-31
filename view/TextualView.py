from model.board import Board
from model.ship import Ship
from model.player import Player

class TextualView:
    def printBoard(view, board: Board, hideShip: bool = False):
        size = board.size
        header = ""
        for col in range(size):
            header += " " + (col + 1) + " "
        print(header)
        print("   " + "--" * size)

        for row in range(size):
            rowBuilder = (row + 1) + " |"
            

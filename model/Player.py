from model.board import Board
from model.ship import createShips

class Player:
    def __init__(player, name: str, size: int):
        player.name = name
        player.board = Board(size)
        player.fleet = createShips()
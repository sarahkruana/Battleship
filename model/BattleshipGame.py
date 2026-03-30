from model.board import Board
from model.ship import Ship
from model.player import Player

class BattleshipGame:
    def __init__(game, redPlayer: str, bluePlayer: str, size: int):
        game.size = size
        game.redPlayer = Player(redPlayer, size)
        game.bluePlayer = Player(bluePlayer, size)
        game.current = 0
        game.winner = None
        game.started = False
    
    def getCurrent(game) -> Player:
        if game.current % 2 == 0:
            return game.redPlayer
        else:
            return game.bluePlayer
        
    def getOpponent(game) -> Player:
        if game.getCurrent() == game.redPlayer:
            return game.bluePlayer
        else:
            return game.redPlayer

    def placeShip(game, player: Player, ship: Ship, positions: list[tuple[int, int]]) -> bool:
        if game.checkStarted("notStarted") == False:
            raise RuntimeError("Game has already been started")
        
        return player.board.placeShip(ship, positions)
    
    def allPlaced(game, player: Player) -> bool:
        return player.board.allPlaced(player.fleet)
    
    def gameStart(game):
        if game.checkStarted("notStarted") == False:
            raise RuntimeError("Game has already been started")

        if game.allPlaced(game.redPlayer) == False:
            raise RuntimeError("redPlayer has not placed all ships")
        if game.allPlaced(game.bluePlayer) == False:
            raise RuntimeError("bluePlayer has not placed all ships")
        
        game.started = True

    def attack(game, row: int, col: int) -> str:
        attackResult = game.getOpponent().board.attacked(row, col)

        if attackResult == "sunk":
            if game.getOpponent.board.allSunk() == True:
                game.winner = game.getCurrent

        game.current += 1
        return attackResult
    
    def totalAttacks(game, player: Player) -> int:
        score = 0
        for ship in player.fleet:
            if ship.isSunk():
                score += ship.size

        return score

    def isOver(game) -> bool:
        return not game.winner == None

    def checkStarted(game, flag: str) -> bool:
        if flag == "notStarted" and game.started == True:
            return False
        if flag == "started" and game.started == False:
            return False
        
        return True

    

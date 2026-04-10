from model.BattleshipGame import BattleshipGame
from model.Player import Player
from model.AIPlayer import AIPlayer
from view.TextualView import TextualView
from controller.GameController import GameController

if __name__ == "__main__":
    print("Welcome to Battleship!")

    redName = input("Please enter the name of redPlayer: ").strip()

    flag = False
    size = 0
    while not flag:
        boardSize = input("Please enter the board size (5-10): ").strip()

        if not boardSize.isdigit():
            print("Please enter a valid integer for the size")
            continue

        boardSize = int(boardSize)

        if boardSize < 5 or boardSize > 10:
            print("Size is not within the valid range")
            continue

        size = boardSize
        flag = True

    redPlayer = Player(redName, size)
    bluePlayer = AIPlayer("Monte", size)

    game = BattleshipGame(redPlayer, bluePlayer, size)
    view = TextualView()
    controller = GameController(game, view)
    
    controller.runGame()

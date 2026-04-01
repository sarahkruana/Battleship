from model.game import BattleshipGame
from view.display import TextualView
from controller.controller import GameController

if __name__ == "__main__":
    print("Welcome to Battleship!")

    redPlayer = input("Please enter the name of redPlayer: ").strip()
    bluePlayer = input("Please enter the name of bluePlayer: ").strip()

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

    game = BattleshipGame(redPlayer, bluePlayer, size)
    view = TextualView()
    controller = GameController(game, view)
    
    controller.runGame()

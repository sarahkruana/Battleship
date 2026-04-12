import os
from model.BattleshipGame import BattleshipGame
from view.TextualView import TextualView
from model.AIPlayer import AIPlayer

class GameController:

    '''
    Constructor to initialize the controller with both a game and a view
    @param game (BattleshipGame) represents the game model
    @param view (TextualView) represents the players view
    '''
    def __init__(cont, game, view):
        cont.game = game
        cont.view = view

    '''
    Runs the game (placing the ships and then playing the battle)
    '''
    def runGame(cont):
        cont.runShipPlacement()
        cont.runBattle()

    '''
    Runs the portion of the game that is placing the ships for both players
    Note: AI players will place their ships without prompt, but human players will be prompted
    '''
    def runShipPlacement(cont):
        for player in [cont.game.redPlayer, cont.game.bluePlayer]:
            cont.clearScreen()
            
            if isinstance(player, AIPlayer):
                player.placeShipsRand()
                print(f"{player.name} ships have all been placed")
            else:
                print(f"{player.name}, please place your ships")
                for ship in player.fleet:
                    cont.placeShip(player, ship)
        
        cont.game.gameStart()
    
    '''
    Gets the human player to place a ship until the operation is successful 
    @param player (Player) represents the player placing the ship
    @param ship (Ship) represents the ship being placed
    '''
    def placeShip(cont, player, ship):
        while True:
            cont.view.printBoard(player.board, False)
            print(f"\n Please place {ship.name} (size: {ship.size})")
            print(f" Please enter positions as row,col row,col")

            pos = cont.getLocationInput(ship.size)
            if pos is None:
                print("Given locations is invalid. Please try again")
                continue

            convertedPos = [] 
            for row, col in pos:
                convertedPos.append((row - 1, col - 1))

            if cont.game.placeShip(player, ship, convertedPos):
                break
            else:
                print("Invalid ship location")

    '''
    Parses the 1-based indexing that the user gives.
    Returns a list (list[tuple[int, int]]) representing the seperate locations on the board
    or it returns (None) if the input isn't valid
    @param size (int) represents the size of the ship
    '''
    def getLocationInput(cont, size):
        userInput = input(" > ").strip().split()

        for token in userInput:
            if token.lower() == "quit":
                print("Thanks for playing Battleship!")
                exit()

        if len(userInput) != size:
            return None
        
        locations = []
        for loc in userInput:
            parts = loc.split(",")

            if len(parts) != 2:
                return None
            
            if parts[0].isdigit() == False or parts[1].isdigit() == False:
                return None
        
            row = int(parts[0])
            col = int(parts[1])
            locations.append((row, col))

        return locations
    
    '''
    Runs the actual playing of the game. 
    Note: only waits for the human player to press enter, not for the ai player
    '''
    def runBattle(cont):
        while not cont.game.isOver():
            cont.clearScreen()
            current = cont.game.getCurrent()
            opponent = cont.game.getOpponent()

            if not isinstance(current, AIPlayer):
                cont.view.printView(current, opponent)

            cont.runTurn(current, opponent)
            input("\n Please press enter to continue")

        cont.clearScreen()
        cont.view.showWinner(cont.game.winner)

    '''
    Handles a turn (prompts the input, processes the attack, etc)
    Note: only human players are prompted for input (ai automatically chooses the best one)
    @param current (Player) represebts the current player
    @param opponent (Player) represents the opponent
    '''
    def runTurn(cont, current, opponent):
        if isinstance(current, AIPlayer):
            row, col = current.chooseAttack(opponent.board)
            attackResult = cont.game.attack(row, col)
            cont.view.showAttackResult(current.name, row, col, attackResult)
        else:
            print(f"\n {current.name}, please enter your attack in the format row,col")
            row, col = cont.getAttackInput()
            attackResult = cont.game.attack(row - 1, col - 1)
            cont.view.showAttackResult(current.name, row - 1, col - 1, attackResult)

    '''
    Parses the input that the user gives as an attack
    Returns (int, int) that represents the attack as a location
    '''
    def getAttackInput(cont):
        while True:
            userInput = input(" > ").strip()

            if "quit" in userInput.lower().split():
                print("Thanks for playing Battleship!")
                exit()

            parts = userInput.split(",")

            if userInput.lower() == "quit":
                print("Thanks for playing Battlship!")
                exit()

            if len(parts) != 2:
                print("Invalid row and column")
                continue

            if parts[0].isdigit() == False or parts[1].isdigit() == False:
                print("Coordinates given are not valid ints")
                continue

            row = int(parts[0])
            col = int(parts[1])
            size = cont.game.size

            if row < 1 or row > size:
                print(f"Invalid row location. It must be between 1 and {size}")
                continue
            
            if col < 1 or col > size:
                print(f"Invalid col location. It must be between 1 and {size}")
                continue

            if (row - 1, col - 1) in cont.game.getOpponent().board.attacks:
                print(f"({row}, {col}) has already been attacked")
                continue

            return row, col


    '''
    Clears the screen in between turns to make everything look clean
    '''
    def clearScreen(cont):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

from model.Board import Board
from model.Ship import Ship
from model.Player import Player

class TextualView:
    
    '''
    Prints the board of a designated player.
    @param board (Board) represents the players board
    @param hideShips (boolean) represents if the ships should be hidden 
    (eg. to not show the other players ships)
    '''
    def printBoard(view, board, hideShips):
        size = board.size
        
        header = ""
        for col in range(size):
            header += " " + str(col + 1) + " "
        print(header)
        print("   " + "--" * size)

        for row in range(size):
            print(str(row + 1) + " |", end=" ")

            for col in range(size):
                cell = board.grid[row][col]

                if hideShips == True and cell == Board.SHIP:
                    cell = Board.EMPTY

                print(cell, end=" ")
            
            print()

        print()

    '''
    Prints what the entire view looks like including the current players board, 
    the state of the current players fleet, as well as the opponent players board
    @param currPlayer (Player) represents the current player
    @param opponent (Player) represents the opponent
    '''
    def printView(view, currPlayer, opponent):
        print(f"\n {currPlayer.name}'s board:")
        view.printBoard(currPlayer.board, False)

        print(f"\n {currPlayer.name}'s Fleet:")
        for ship in currPlayer.fleet:
            print("\n" + ship.__str__())
        
        print(f"\n {opponent.name}'s board:")
        view.printBoard(opponent.board, True)

    '''
    Prints the winner of the game
    '''
    def showWinner(view, player):
        print(f"{player.name} has won the game!")

    '''
    Displays what happens after an attack on a ship.
    Rows and columns are converted to 1-based for easier reading
    @param attacker (str) represents whoever the attacker was
    @param row (int) represents 0-based row number of the attack
    @param col (int) represents 0-based col number of the attack
    @param result (str) represents what happened after the attack
    @param ship (Ship) represents the ship that was attacked
    '''
    def showAttackResult(view, attacker, row, col, result):
        loc = f"({row + 1}, {col + 1})"

        if result == "hit":
            print(f"  {attacker} fired at {loc} — HIT!")
        elif result == "miss":
            print(f"  {attacker} fired at {loc} — miss.")
        elif result == "sunk":
            print(f"  {attacker} fired at {loc} — HIT! Ship has been sunk!")
        elif result == "already_attacked":
            print(f"  {loc} has already been attacked. Please pick a different spot.")
        elif result == "invalid":
            print(f"  {loc} is off the board. Please pick a valid location.")


    '''
    Prints a prompt message to the user for their turn
    '''
    def promptTurn(view):
        print("Please enter an integer for the row and col")


    
    



            

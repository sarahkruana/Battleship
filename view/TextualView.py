from model.Board import Board
from model.Ship import Ship
from model.Player import Player

class TextualView:

    '''
    Prints the board of a designated player.
    Returns an array (list[str]) representing each line of a player's board
    @param board (Board) represents the players board
    @param hideShips (boolean) represents if the ships should be hidden 
    (eg. to not show the other players ships)
    '''
    def buildBoardLines(view, board, hideShips):
        size = board.size
        lines = []
        
        header = "     "
        for col in range(size):
            header += str(col + 1).rjust(3)
        lines.append(header)
        lines.append("    " + "---" * size)

        for row in range(size):
            line = str(row + 1).rjust(2) + " | "

            for col in range(size):
                cell = board.grid[row][col]

                if hideShips == True and cell == Board.SHIP:
                    cell = Board.EMPTY

                line += cell.rjust(3)
            
            lines.append(line)

        return lines

    '''
    Prints the board of a designated player.
    @param board (Board) represents the players board
    @param hideShips (boolean) represents if the ships should be hidden
    '''
    def printBoard(view, board, hideShips):
        for line in view.buildBoardLines(board, hideShips):
            print(line)
        print()

    '''
    Builds the opponent's fleet status
    Returns a list (list[str]) representing each ship along with it's status
    Shows every ship with a checkmark if still alive or an X if sunk.
    @param fleet (list[Ship]) represents the opponent's fleet
    '''
    def buildFleetLines(view, fleet):
        lines = []

        for ship in fleet:
            status = "✓"
            if ship.isSunk():
                status = "X"

            lines.append(f"  [{status}] {ship.name} (size: {ship.size})")
        return lines


    '''
    Prints what the entire view looks like including the current players board, 
    the state of the opponent players fleet, as well as the opponent players board
    @param currPlayer (Player) represents the current player
    @param opponent (Player) represents the opponent
    '''
    def printView(view, currPlayer, opponent):
        currBoardLines = view.buildBoardLines(currPlayer.board, False)
        currFleetLines = view.buildFleetLines(currPlayer.fleet)
        oppFleetLines = view.buildFleetLines(opponent.fleet)
        oppBoardLines = view.buildBoardLines(opponent.board, True)

        currBoardWidth = max(len(line) for line in currBoardLines)
        fleetWidth = max(len(line) for line in currFleetLines)

        totalRows = max(len(currBoardLines), len(oppFleetLines), len(oppBoardLines))
        currBoardLines += [""] * (totalRows - len(currBoardLines))
        currFleetLines += [""] * (totalRows - len(currFleetLines))
        oppFleetLines += [""] * (totalRows - len(oppFleetLines))
        oppBoardLines += [""] * (totalRows - len(oppBoardLines))

        currHeader = f"{currPlayer.name}'s Board"
        currFleetHeader = f"{currPlayer.name}'s Ships Remaining"
        oppFleetHeader = f"{opponent.name}'s Ships Remaining"
        oppHeader = f"{opponent.name}'s Board"
        print(
            f"\n{currHeader.ljust(currBoardWidth)}" +
            "     " +
            f"{currFleetHeader.ljust(fleetWidth)}" +
            "     " +
            f"{oppFleetHeader.ljust(fleetWidth)}" +
            "     " +
            f"{oppHeader}"
        )

        for currLine, currFleetLine, oppFleetLine, opLine in zip(currBoardLines, 
                                                                 currFleetLines, 
                                                                 oppFleetLines, 
                                                                 oppBoardLines):
            print(
                f"{currLine.ljust(currBoardWidth)}" +
                "     " +
                f"{currFleetLine.ljust(fleetWidth)}" +
                "     " +
                f"{oppFleetLine.ljust(fleetWidth)}" +
                "     " +
                f"{opLine}"
                )
 
        print()
 

    '''
    Prints the winner of the game
    '''
    def showWinner(view, player):
        print(f"{player.name} has won the game!")

    '''
    Displays what happens after an attack on a ship.
    Rows and columns are converted to 1-based
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
        print("Please enter an integer for the row and col (row,col)")


    
    



            

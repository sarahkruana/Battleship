from model.Ship import Ship

class Board:
    EMPTY = "_"
    SHIP = "S"
    HIT = "X"
    MISS = "O"

    '''
    Constructor to create an empty board that the players can fill with ships
    @param size (int) represents the size of the board. 
    The size cannot be greater than ten nor less than 5. 
    '''
    def __init__(board, size):
        if size > 10:
            raise ValueError("board size is too large")
        if size < 5:
            raise ValueError("board size is too small")
        
        board.size = size
        board.grid = [[board.EMPTY for _ in range(size)] for _ in range(size)]
        board.ships: list[Ship] = []
        board.attacks: set[tuple[int,int]] = set()

    '''
    Returns (boolean) if a ship can be placed in a certain set of locations
    @param positions (list[tuple[int, int]]) represents the positions to place the ship onto
    '''
    def canPlace(board, positions) -> bool:
        for row, col in positions:
            if board.grid[row][col] != board.EMPTY:
                return False
            if not board.checkInput(row, col):
                return False
            
        rows = [r for r, _ in positions]
        cols = [c for _, c in positions]
        print(f"rows: {rows}, cols: {cols}")
        if len(set(rows)) != 1 and len(set(cols)) != 1:
            return False
        
        if len(set(rows)) == 1:
            return board.checkContiguous(cols)
        else:
            return board.checkContiguous(rows)
        
        return True

    '''
    Helper method that returns (boolean) if a given list of integers is contiguous. 
    Used in canPlace.
    @param line (list[int]) represents the list of integers (given rows/cols)
    '''
    def checkContiguous(board, line) -> bool:
        if len(set(line)) != len(line):
            return False
        if max(line) - min(line) != len(line) - 1:
            return False
        return True
        
    '''
    Returns (boolean) whether the placing a ship is successful or not. If it can,
    it will place a ship on the board at the designated positions
    @param ship (Ship) represents the designated ship
    @param positions (list[tuple[int, int]]) represents the list of positions to place the ship at
    '''
    def placeShip(board, ship, positions) -> bool:
        if not board.canPlace(positions):
            return False
        
        ship.placeShip(positions)
        board.ships.append(ship)
        for row, col in positions:
            board.grid[row][col] = board.SHIP

        return True
    
    '''
    Handles what happens when a certain location on the grid is attacked by the opposing player
    Returns (str) of the outcome of the attack (invalid, already_attacked, sunk, hit, miss)
    @param row (int) represents the row of the designated attack location
    @param col (int) represents the col of the designated attack location
    '''
    def attacked(board, row, col) -> str:
        if board.checkInput(row, col) == False:
            return "invalid"
        
        if (row,col) in board.attacks:
            return "already_attacked"
        
        board.attacks.add((row,col))

        for ship in board.ships:
            if ship.hit(row, col):
                board.grid[row][col] = board.HIT
                if ship.isSunk():
                    return "sunk"
                else:
                    return "hit"
                
        board.grid[row][col] = board.MISS
        return "miss"
    
    '''
    Returns (boolean) if the given row and col are valid inputs
    @param row (int) represents the row of the designated location
    @param col (int) represents the col of the designated location
    '''
    def checkInput(board, row, col) -> bool:
        if row < 0 or row >= board.size:
                return False
        if col < 0 or col >= board.size:
                return False
        return True
        
    '''
    Returns (boolean) if all the ships on the board are sunk
    '''
    def allSunk(board) -> bool:
        return all(ship.isSunk() for ship in board.ships)
 
    '''
    Returns (boolean) if all the possible ships are placed on the board
    @param ships (list[Ships]) represent the different ships that either are/aren't placed
    '''
    def allPlaced(board, ships) -> bool:
        return all(ship in board.ships for ship in ships)




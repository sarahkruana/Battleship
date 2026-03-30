from model.ship import Ship

class Board:
    EMPTY = "_"
    SHIP = "S"
    HIT = "X"
    MISS = "O"

    def __init__(board, size: int):
        if size > 10:
            raise ValueError("board size is too large")
        if size < 5:
            raise ValueError("board size is too small")
        
        board.size = size
        board.grid = [[board.EMPTY for _ in range(size)] for _ in range(size)]
        board.ships: list[Ship] = []
        board.attacks: set[tuple[int,int]] = set()

    def canPlace(board, positions: list[tuple[int, int]]) -> bool:
        for row, col in positions:
            if board.grid[row][col] != board.EMPTY:
                return False
            if not board.checkInput(row, col):
                return False
            
        rows = [row for row, _ in positions]
        cols = [col for col, _ in positions]
        if len(set(rows)) != 1 and len(set(cols)) != 1:
            return False
        
        if len(set(rows)) == 1:
            return board.checkContiguous(rows)
        else:
            return board.checkContiguous(cols)
        
        return True

    def checkContiguous(board, line: list[int]) -> bool:
        sorted = sorted(line)
        if sorted != list(range(sorted[0], sorted[0] + len(sorted))):
            return False
        return True
        
    def placeShip(board, ship: Ship, positions: list[tuple[int, int]]) -> bool:
        if not board.canPlace(positions):
            return False
        
        ship.place(positions)
        board.ships.append(ship)
        for row, col in positions:
            board.grid[row][col] = board.SHIP

        return True
    
    def attacked(board, row: int, col: int) -> str:
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
    
    def checkInput(board, row: int, col: int) -> bool:
        if row < 0 or row >= board.size:
                return False
        if col < 0 or col >= board.size:
                return False
        return True
        
    
    def allSunk(board) -> bool:
        return all(ship.isSunk() for ship in board.ships)
 
    def allPlaced(board, ships: list[Ship]) -> bool:
        return all(ship in board.ships for ship in ships)




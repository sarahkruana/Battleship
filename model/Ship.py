class Ship:
    '''
    Constuctor that creates a basic ship
    @param name (str) represents the name of the sip
    @param size (int) represents the size of the ship (how many spots it takes up)
    '''
    def __init__(ship, name: str, size: int):
        ship.name = name
        ship.size = size
        ship.positions = []
        ship.hits = set()

    '''
    Sets the ships location. If the amount of positions given is too small, it throws an error
    @param positions (list[tuple[int,int]]) represents the designated positions
    '''
    def placeShip(ship, positions):
        if len(positions) != ship.size:
            raise ValueError(f"{ship.name} needs {ship.size} positions")
            
        ship.positions = positions

    '''
    Returns (boolean) if a hit on the ship at a certain location is true
    @param row represents the row of the location
    @param col represents the col of the location
    '''
    def hit(ship, row, col) -> bool:
        if (row, col) in ship.positions:
            ship.hits.add((row, col))
            return True

        return False

    '''
    Returns (boolean) if the ship is sunk or not
    '''
    def isSunk(ship) -> bool:
        return len(ship.hits) == ship.size

    '''
    Returns (str) the name of the ship along with its size and whether or not it is sunk
    '''
    def __str__(ship):
        return f"Ship({ship.name}, size={ship.size}, sunk={ship.isSunk()})"
 
 
SHIPS_SET = [
    ("Carrier", 5),
    ("Battleship", 4),
    ("Cruiser", 3),
    ("Submarine", 3),
    ("Destroyer", 2)
]
 
'''
Returns (list[Ship]) a standard fleet of ships listed above
'''
def createShips() -> list[Ship]:
    return [Ship(name, size) for name, size in SHIPS_SET]
 
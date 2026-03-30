class Ship:
    def __init__(ship, name: str, size: int):
        ship.name = name
        ship.size = size
        ship.positions = []
        ship.hits = set()

    def placeShip(ship, positions: list[tuple[int,int]]):
        if len(positions) != ship.size:
            raise ValueError(f"{ship.name} needs {ship.size} positions")
            ship.positions = positions

    def hit(ship, row: int, col: int) -> bool:
        if (row, col) in ship.positions:
            ship.hits.add((row, col))
            return True

        return False

    def isSunk(ship) -> bool:
        return len(ship.hits) == ship.size

    def __str__(ship):
        return f"Ship({ship.name}, size={ship.size}, sunk={ship.isSunk()})"
 
 
SHIPS_SET = [
    ("Carrier", 5),
    ("Battleship", 4),
    ("Cruiser", 3),
    ("Submarine", 3),
    ("Destroyer", 2)
]
 
def createShips() -> list[Ship]:
    return [Ship(name, size) for name, size in SHIPS_SET]
 
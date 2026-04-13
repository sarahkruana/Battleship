import unittest
from model.Board import Board
from model.Ship import Ship, createShips


class TestBoard(unittest.TestCase):
   
    def setUp(self):
        self.board = Board(7)
        self.ship = Ship("Destroyer", 2)


    def test_validInit(self):
        self.assertEqual(self.board.size, 7)
        self.assertEqual(len(self.board.ships), 0)
        self.assertEqual(len(self.board.attacks), 0)
        for row in self.board.grid:
            for cell in row:
                self.assertEqual(cell, Board.EMPTY)

    def test_tooBigInit(self):
        with self.assertRaises(ValueError):
            Board(11)

    def test_tooSmallInit(self):
        with self.assertRaises(ValueError):
            Board(4)


    def test_validCanPlace(self):
        self.assertTrue(self.board.canPlace([(0,0),(0,1)]))
        self.assertTrue(self.board.canPlace([(0,0),(1,0)]))

    def test_invalidCanPlace(self):
        self.assertFalse(self.board.canPlace([(0,0),(1,1)]))
        self.assertFalse(self.board.canPlace([(0,0),(0,2)]))

        self.board.placeShip(self.ship, [(0,0),(0,1)])
        cruiser = Ship("Cruiser", 3)
        self.assertFalse(self.board.canPlace([(0,0),(0,1),(0,2)]))

        self.assertFalse(self.board.canPlace([(0,0),(0,8)]))


    def test_validPlaceShip(self):
        result = self.board.placeShip(self.ship, [(0,0),(0,1)])
       
        self.assertTrue(result)
        self.assertIn(self.ship, self.board.ships)
        self.assertEqual(self.board.grid[0][0], Board.SHIP)
        self.assertEqual(self.board.grid[0][1], Board.SHIP)

    def test_invalidPlaceShip(self):
        result = self.board.placeShip(self.ship, [(0,0),(1,1)])

        self.assertFalse(result)
        self.assertNotIn(self.ship, self.board.ships)

        self.board.placeShip(self.ship, [(0,0),(0,1)])
        cruiser = Ship("Cruiser", 3)
        result = self.board.placeShip(cruiser, [(0,0),(0,1),(0,2)])

        self.assertFalse(result)


    def test_missAttack(self):
        result = self.board.attacked(0, 0)

        self.assertEqual(result, "miss")
        self.assertEqual(self.board.grid[0][0], Board.MISS)

    def test_hitAttack(self):
        self.board.placeShip(self.ship, [(0,0),(0,1)])
        result = self.board.attacked(0, 0)

        self.assertEqual(result, "hit")
        self.assertEqual(self.board.grid[0][0], Board.HIT)

    def test_sunkAttack(self):
        self.board.placeShip(self.ship, [(0,0),(0,1)])
        self.board.attacked(0, 0)
        result = self.board.attacked(0, 1)

        self.assertEqual(result, "sunk")

    def test_alrAttacked(self):
        self.board.attacked(0, 0)
        result = self.board.attacked(0, 0)

        self.assertEqual(result, "already_attacked")

    def test_invalidAttack(self):
        result = self.board.attacked(9, 9)

        self.assertEqual(result, "invalid")


    def test_validCheckInput(self):
        self.assertTrue(self.board.checkInput(0, 0))
        self.assertTrue(self.board.checkInput(6, 6))

    def test_invalidCheckInput(self):
        self.assertFalse(self.board.checkInput(7, 0))
        self.assertFalse(self.board.checkInput(0, 7))
        self.assertFalse(self.board.checkInput(-1, 0))
        self.assertFalse(self.board.checkInput(0, -1))


    def test_notAllSunk(self):
        self.board.placeShip(self.ship, [(0,0),(0,1)])
        self.board.attacked(0, 0)
        self.assertFalse(self.board.allSunk())

    def test_allSunk(self):
        self.board.placeShip(self.ship, [(0,0),(0,1)])
        self.board.attacked(0, 0)
        self.board.attacked(0, 1)
        self.assertTrue(self.board.allSunk())


    def test_notAllPlaced(self):
        fleet = createShips()
        self.assertFalse(self.board.allPlaced(fleet))

    def test_allPlaced(self):
        fleet = createShips()
        positions = [
            [(0,0),(0,1),(0,2),(0,3),(0,4)],
            [(1,0),(1,1),(1,2),(1,3)],
            [(2,0),(2,1),(2,2)],
            [(3,0),(3,1),(3,2)],
            [(4,0),(4,1)]
        ]
        for ship, pos in zip(fleet, positions):
            self.board.placeShip(ship, pos)

        self.assertTrue(self.board.allPlaced(fleet))

if __name__ == "__main__":
    unittest.main()

import unittest
from model.Player import Player
from model.Ship import createShips
from model.Board import Board


class TestPlayer(unittest.TestCase):
   
    def setUp(self):
        self.player = Player("Red", 7)


    def test_init(self):
        self.assertEqual(self.player.name, "Red")
        self.assertIsInstance(self.player.board, Board)
        self.assertEqual(self.player.board.size, 7)
        self.assertEqual(len(self.player.fleet), 5)


    def test_fleet(self):
        names = [ship.name for ship in self.player.fleet]
        self.assertIn("Carrier", names)
        self.assertIn("Battleship", names)
        self.assertIn("Cruiser", names)
        self.assertIn("Submarine", names)
        self.assertIn("Destroyer", names)


    def test_uniqueFleet(self):
        blue = Player("Blue", 7)
        self.assertIsNot(self.player.fleet, blue.fleet)
        self.assertIsNot(self.player.board, blue.board)

if __name__ == "__main__":
    unittest.main()

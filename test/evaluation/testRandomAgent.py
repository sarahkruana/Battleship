import unittest

from evaluation.RandomAgent import RandomAgent
from model.Board import Board
from model.Ship import Ship


class TestRandomAgent(unittest.TestCase):
 
    def setUp(self):
        self.agent = RandomAgent()
        self.board = Board(7)
        destroyer = Ship("Destroyer", 2)
        self.board.placeShip(destroyer, [(0, 0), (0, 1)])
 

    def test_inBounds(self):
        row, col = self.agent.chooseAttack(self.board, [])
        
        self.assertGreaterEqual(row, 0)
        self.assertLess(row, 7)
        self.assertGreaterEqual(col, 0)
        self.assertLess(col, 7)
 
    def test_notAlrAttacked(self):
        for row in range(7):
            for col in range(7):
                if (row, col) != (6, 6):
                    self.board.attacked(row, col)
 
        row, col = self.agent.chooseAttack(self.board, [])
        
        self.assertNotIn((row, col), self.board.attacks)
 
    def test_oneLeft(self):
        for row in range(7):
            for col in range(7):
                if (row, col) != (6, 6):
                    self.board.attacked(row, col)
 
        row, col = self.agent.chooseAttack(self.board, [])
        self.assertEqual((row, col), (6, 6))
 
 
if __name__ == "__main__":
    unittest.main()
 
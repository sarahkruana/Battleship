import unittest
from model.AIPlayer import AIPlayer
from model.MonteCarloAgent import MonteCarloAgent
from model.Board import Board
from model.Ship import Ship


class TestAIPlayer(unittest.TestCase):

   def setUp(self):
       self.ai = AIPlayer("Monte", 7)


   def test_init(self):
       self.assertEqual(self.ai.name, "Monte")
       self.assertIsInstance(self.ai.board, Board)
       self.assertEqual(self.ai.board.size, 7)
       self.assertEqual(len(self.ai.fleet), 5)
       self.assertIsInstance(self.ai.agent, MonteCarloAgent)


   def test_placeShipsRand(self):
       self.ai.placeShipsRand()
       allPos = []
       for ship in self.ai.board.ships:
           for pos in ship.positions:
               self.assertNotIn(pos, allPos)
               allPos.append(pos)
       self.assertEqual(len(self.ai.board.ships), 5)


   def test_generatePos(self):
       results = [self.ai.generatePos(2) for _ in range(100)]
       hori = [h for h in results if h[0][0] == h[1][0]]
       vert = [v for v in results if v[0][1] == v[1][1]]
       self.assertGreater(len(hori), 0)
       self.assertGreater(len(vert), 0)


   def test_validChooseAttack(self):
       opponentBoard = Board(7)
       opponent = AIPlayer("opp", 7)
       opponent.placeShipsRand()

       for ship in opponent.board.ships:
           opponentBoard.placeShip(ship, ship.positions)

       row, col = self.ai.chooseAttack(opponentBoard)
       self.assertGreaterEqual(row, 0)
       self.assertLess(row, 7)
       self.assertGreaterEqual(col, 0)
       self.assertLess(col, 7)

   def test_chooseNotAlrAttack(self):
       opponentBoard = Board(7)
       opponent = AIPlayer("Opponent", 7)
       opponent.placeShipsRand()

       for ship in opponent.board.ships:
           opponentBoard.placeShip(ship, ship.positions)

       opponentBoard.attacked(0, 0)
       opponentBoard.attacked(0, 1)
       opponentBoard.attacked(0, 2)

       row, col = self.ai.chooseAttack(opponentBoard)
       self.assertNotIn((row, col), opponentBoard.attacks)

if __name__ == "__main__":
   unittest.main()


import unittest
from io import StringIO
import sys

from view.TextualView import TextualView
from model.Player import Player


class TestGameView(unittest.TestCase):

    def setUp(self):
        self.view = TextualView()
        self.player = Player("Red", 5)
        self.opponent = Player("Blue", 5)

    def capture_output(self, func, *args):
        captured = StringIO()
        sys.stdout = captured
        func(*args)
        sys.stdout = sys.__stdout__
        return captured.getvalue()

    def test_printBoard_shows_grid(self):
        output = self.capture_output(self.view.printBoard, self.player.board, False)
        self.assertIn("_", output)
        self.assertIn("1", output)

    def test_printBoard_hides_ships(self):
        ship = self.player.fleet[4]
        self.player.board.placeShip(ship, [(0,0),(0,1)])

        output = self.capture_output(self.view.printBoard, self.player.board, True)
        self.assertNotIn("S", output)

    def test_printView_outputs_both_boards(self):
        output = self.capture_output(self.view.printView, self.player, self.opponent)
        self.assertIn("Red's Board", output)
        self.assertIn("Blue's Board", output)

    def test_printView_shows_fleet(self):
        output = self.capture_output(self.view.printView, self.player, self.opponent)
        self.assertIn("Ships Remaining", output)
        for ship in self.opponent.fleet:
            self.assertIn(ship.name, output)

    def test_showWinner(self):
        output = self.capture_output(self.view.showWinner, self.player)
        self.assertIn("Red has won the game!", output)

    def test_showAttackResult_hit(self):
        output = self.capture_output(self.view.showAttackResult, "Red", 0, 0, "hit")
        self.assertIn("HIT", output)

    def test_showAttackResult_miss(self):
        output = self.capture_output(self.view.showAttackResult, "Red", 0, 0, "miss")
        self.assertIn("miss", output)

    def test_showAttackResult_sunk(self):
        output = self.capture_output(self.view.showAttackResult, "Red", 0, 0, "sunk")
        self.assertIn("sunk", output)

    def test_showAttackResult_already_attacked(self):
        output = self.capture_output(self.view.showAttackResult, "Red", 0, 0, "already_attacked")
        self.assertIn("already been attacked", output)

    def test_showAttackResult_invalid(self):
        output = self.capture_output(self.view.showAttackResult, "Red", 0, 0, "invalid")
        self.assertIn("off the board", output)

    def test_promptTurn(self):
        output = self.capture_output(self.view.promptTurn)
        self.assertIn("Please enter an integer", output)


if __name__ == "__main__":
    unittest.main()

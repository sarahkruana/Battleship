import unittest
from unittest.mock import patch, MagicMock
#i needed to create mocks of the mvc game enviroment so i used patch and magicmock

from model.BattleshipGame import BattleshipGame
from model.Player import Player
from model.AIPlayer import AIPlayer
from view.TextualView import TextualView
from controller.GameController import GameController


class TestGameController(unittest.TestCase):

    def setUp(self):
        self.redPlayer = Player("Red", 7)
        self.bluePlayer = AIPlayer("Monte", 7)
        self.game = BattleshipGame(self.redPlayer, self.bluePlayer, 7)
        self.view = TextualView()
        self.controller = GameController(self.game, self.view)

    '''
    helper to place both fleets so the game can be started
    '''
    def placeBothFleets(self):
        shipPos = [
            [(0,0),(0,1),(0,2),(0,3),(0,4)],
            [(1,0),(1,1),(1,2),(1,3)],
            [(2,0),(2,1),(2,2)],
            [(3,0),(3,1),(3,2)],
            [(4,0),(4,1)]
        ]
        for player in [self.redPlayer, self.bluePlayer]:
            for ship, pos in zip(player.fleet, shipPos):
                self.game.placeShip(player, ship, pos)

  
    def test_runAIShipPlacement(self):
        with patch.object(self.controller, "clearScreen"):
            with patch.object(self.game, "gameStart"):
                with patch.object(self.controller, "placeShip"):
                    self.controller.runShipPlacement()

        self.assertEqual(len(self.bluePlayer.board.ships), 5)

    def test_runHumanShipPlacement(self):
        inputs = [
            "1,1 1,2 1,3 1,4 1,5",
            "2,1 2,2 2,3 2,4",
            "3,1 3,2 3,3",
            "4,1 4,2 4,3",
            "5,1 5,2",
        ]
        with patch.object(self.controller, "clearScreen"):
            with patch.object(self.game, "gameStart"):
                with patch("builtins.input", side_effect=inputs):
                    self.controller.runShipPlacement()
        self.assertEqual(len(self.redPlayer.board.ships), 5)
        carrier = self.redPlayer.fleet[0]
        self.assertEqual(carrier.positions, [(0,0),(0,1),(0,2),(0,3),(0,4)])


    def test_placeShipValid(self):
        ship = self.redPlayer.fleet[4]
        with patch("builtins.input", return_value="1,1 1,2"):
            self.controller.placeShip(self.redPlayer, ship)
        self.assertIn(ship, self.redPlayer.board.ships)
        self.assertEqual(ship.positions, [(0,0),(0,1)])

    def test_placeShipBadInput(self):
        destroyer = self.redPlayer.fleet[4]

        with patch("builtins.input", side_effect=["bad input", "1,1 1,2"]):
            self.controller.placeShip(self.redPlayer, destroyer)
        self.assertIn(destroyer, self.redPlayer.board.ships)

        submarine = self.redPlayer.fleet[3]
        with patch("builtins.input", side_effect=["1,1 1,2 1,3", "2,1 2,2 2,3"]):
            self.controller.placeShip(self.redPlayer, submarine)
        self.assertIn(submarine, self.redPlayer.board.ships)


    def test_getValidLocInput(self):
        with patch("builtins.input", return_value="1,1 1,2 1,3 1,4 1,5"):
            result = self.controller.getLocationInput(5)
        self.assertEqual(result, [(1,1),(1,2),(1,3),(1,4),(1,5)])
   
    def test_getBadLocInput(self):
        with patch("builtins.input", return_value="1,1 1,2"):
            result = self.controller.getLocationInput(5)
        self.assertIsNone(result)

        with patch("builtins.input", return_value="11 12 13 14 15"):
            result = self.controller.getLocationInput(5)
        self.assertIsNone(result)
 
        with patch("builtins.input", return_value="a,b 1,2 1,3 1,4 1,5"):
            result = self.controller.getLocationInput(5)
        self.assertIsNone(result)
   
    def test_getQuitLocInput(self):
        with patch("builtins.input", return_value="quit"):
            with self.assertRaises(SystemExit):
                self.controller.getLocationInput(5)

        with patch("builtins.input", return_value="1,1 quit"):
            with self.assertRaises(SystemExit):
                self.controller.getLocationInput(5)


    def test_runAiTurn(self):
        self.placeBothFleets()
        self.game.gameStart()
        self.bluePlayer.chooseAttack = MagicMock(return_value=(6, 6))
        self.game.current = 1
        self.controller.runTurn(self.bluePlayer, self.redPlayer)
        self.bluePlayer.chooseAttack.assert_called_once_with(self.redPlayer.board)
        self.assertIn((6,6), self.redPlayer.board.attacks)
   
    def test_runHumanTurn(self):
        self.placeBothFleets()
        self.game.gameStart()
        with patch("builtins.input", return_value="6,6"):
            self.controller.runTurn(self.redPlayer, self.bluePlayer)
        self.assertIn((5, 5), self.bluePlayer.board.attacks)


    def test_getValidAttackInput(self):
        self.placeBothFleets()
        self.game.gameStart()
        with patch("builtins.input", return_value="6,6"):
            row, col = self.controller.getAttackInput()
        self.assertEqual((row, col), (6, 6))
   
    def test_getOutBoundsAttackInput(self):
        self.placeBothFleets()
        self.game.gameStart()
        with patch("builtins.input", side_effect=["9,9", "6,6"]):
            row, col = self.controller.getAttackInput()
        self.assertEqual((row, col), (6, 6))
   
    def test_getAlrAttackedInput(self):
        self.placeBothFleets()
        self.game.gameStart()
        self.bluePlayer.board.attacked(5, 5)
        with patch("builtins.input", side_effect=["6,6", "6,7"]):
            row, col = self.controller.getAttackInput()
        self.assertEqual((row, col), (6, 7))
   
    def test_getBadAttackInput(self):
        self.placeBothFleets()
        self.game.gameStart()
        with patch("builtins.input", side_effect=["66", "6,6"]):
            row, col = self.controller.getAttackInput()
        self.assertEqual((row, col), (6, 6))
   
    def test_getQuitAttackInput(self):
        self.placeBothFleets()
        self.game.gameStart()
        with patch("builtins.input", return_value="quit"):
            with self.assertRaises(SystemExit):
                self.controller.getAttackInput()

    def test_getLetterAttackInput(self):
        self.placeBothFleets()
        self.game.gameStart()

        with patch("builtins.input", side_effect=["a,b", "6,6"]):
            row, col = self.controller.getAttackInput()
        self.assertEqual((row, col), (6, 6))

if __name__ == "__main__":
    unittest.main()

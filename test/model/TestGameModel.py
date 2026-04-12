import unittest

from model.BattleshipGame import BattleshipGame
from model.Player import Player
from model.Ship import Ship, createShips

class TestGameModel(unittest.TestCase):

    def setUp(self):
        red = Player("Red", 7)
        blue = Player("Blue", 7)
        self.game = BattleshipGame(red, blue, 7)

    def test_initialization(self):
        self.assertEqual(self.game.size, 7)
        self.assertEqual(self.game.redPlayer.name, "Red")
        self.assertEqual(self.game.bluePlayer.name, "Blue")
        self.assertEqual(self.game.current, 0)
        self.assertIsNone(self.game.winner)
        self.assertFalse(self.game.started)

    def test_getCurrent_and_getOpponent(self):
        self.assertEqual(self.game.getCurrent(), self.game.redPlayer)
        self.assertEqual(self.game.getOpponent(), self.game.bluePlayer)

        self.game.current = 1
        self.assertEqual(self.game.getCurrent(), self.game.bluePlayer)
        self.assertEqual(self.game.getOpponent(), self.game.redPlayer)

    def test_placeShip_before_start(self):
        ships = createShips()
        carrier = ships[0]

        positions = [(0,0), (0,1), (0,2), (0,3), (0,4)]
        result = self.game.placeShip(self.game.redPlayer, carrier, positions)
        self.assertTrue(result)

    def test_placeShip_after_game_started_raises_error(self):
        self.placeBothFleets()
        self.game.gameStart()
 
        with self.assertRaises(RuntimeError):
            self.game.placeShip(
                self.game.redPlayer, 
                self.game.redPlayer.fleet[0], 
                [(0,0),(0,1),(0,2),(0,3),(0,4)]
            )

    def test_allPlaced(self):
        red = self.game.redPlayer

        positions = [
            [(0,0),(0,1),(0,2),(0,3),(0,4)],
            [(1,0),(1,1),(1,2),(1,3)],
            [(2,0),(2,1),(2,2)],
            [(3,0),(3,1),(3,2)],
            [(4,0),(4,1)]
        ]

        for ship, pos in zip(red.fleet, positions):
            self.game.placeShip(red, ship, pos)

        self.assertTrue(self.game.allPlaced(red))

    def test_gameStart_success(self):
        for player in [self.game.redPlayer, self.game.bluePlayer]:
            pos_list = [
                [(0,0),(0,1),(0,2),(0,3),(0,4)],
                [(1,0),(1,1),(1,2),(1,3)],
                [(2,0),(2,1),(2,2)],
                [(3,0),(3,1),(3,2)],
                [(4,0),(4,1)]
            ]
            for ship, pos in zip(player.fleet, pos_list):
                self.game.placeShip(player, ship, pos)

        self.game.gameStart()
        self.assertTrue(self.game.started)

    def test_gameStart_raises_if_not_all_ships_placed(self):
        with self.assertRaises(RuntimeError):
            self.game.gameStart()

    def test_attack_returns_correct_result(self):
        self.placeBothFleets()
        self.game.gameStart()
 
        self.game.current = 0
        result = self.game.attack(6, 6)
        self.assertEqual(result, "miss")
 
        self.game.current = 0
        result = self.game.attack(4, 0)
        self.assertEqual(result, "hit")
 
        self.game.current = 0
        result = self.game.attack(4, 1)
        self.assertEqual(result, "sunk")

        self.game.current = 0
        result = self.game.attack(6, 6)
        self.assertEqual(result, "already_attacked")

    def test_isOver_and_winner(self):
        self.placeBothFleets()
        self.game.gameStart()
 
        for ship in self.game.bluePlayer.board.ships:
            for row, col in ship.positions:
                self.game.current = 0
                self.game.attack(row, col)
 
        self.assertTrue(self.game.isOver())
        self.assertEqual(self.game.winner, self.game.redPlayer)

    def test_totalAttacks(self):
        self.placeBothFleets()
        self.game.gameStart()
 
        for col in range(5):
            self.game.current = 0
            self.game.attack(0, col)
        for col in range(4):
            self.game.current = 0
            self.game.attack(1, col)
 
        self.assertEqual(self.game.totalAttacks(self.game.bluePlayer), 5 + 4)

    def test_checkStarted(self):
        self.assertTrue(self.game.checkStarted("notStarted"))
        self.assertFalse(self.game.checkStarted("started"))

        self.game.started = True
        self.assertFalse(self.game.checkStarted("notStarted"))
        self.assertTrue(self.game.checkStarted("started"))

    '''
    helper needed to place both players ships (required to start the game, etc)
    '''
    def placeBothFleets(self):
        shipPos = [
            [(0,0),(0,1),(0,2),(0,3),(0,4)],
            [(1,0),(1,1),(1,2),(1,3)],
            [(2,0),(2,1),(2,2)],
            [(3,0),(3,1),(3,2)],
            [(4,0),(4,1)]
        ]
        for player in [self.game.redPlayer, self.game.bluePlayer]:
            for ship, pos in zip(player.fleet, shipPos):
                self.game.placeShip(player, ship, pos)
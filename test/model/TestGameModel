import unittest

from model.BattleshipGame import BattleshipGame
from model.Player import Player
from model.Ship import Ship, createShips

class TestGameModel(unittest.TestCase):

    def setUp(self):
        self.game = BattleshipGame("Red", "Blue", 5)

    def test_initialization(self):
        self.assertEqual(self.game.size, 5)
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
        ships = createShips()

        with self.assertRaises(RuntimeError):
            self.game.placeShip(self.game.redPlayer, ships[0], [(0,0)])

    def test_allPlaced(self):
        ships = createShips()
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
        ships = createShips()
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
        ship = self.game.bluePlayer.fleet[4]
        self.game.placeShip(self.game.bluePlayer, ship, [(2,2), (2,3)])

        self.game.gameStart()

        result = self.game.attack(0, 0)
        self.assertEqual(result, "miss")

        result = self.game.attack(2, 2)
        self.assertEqual(result, "hit")

        result = self.game.attack(2, 3)
        self.assertEqual(result, "sunk")

    def test_isOver_and_winner(self):
        self.game.gameStart()

        for ship in self.game.bluePlayer.board.ships:
            for r, c in ship.positions:
                self.game.attack(r, c)

        self.assertTrue(self.game.isOver())
        self.assertEqual(self.game.winner, self.game.redPlayer)

    def test_totalAttacks(self):
        ships = createShips()
        red = self.game.redPlayer
        for ship in ships[:2]:
            ship.placeShip([(0,0)] * ship.size)
            for i in range(ship.size):
                ship.hit(0, i)

        self.assertEqual(self.game.totalAttacks(red), 5 + 4)

    def test_checkStarted(self):
        self.assertTrue(self.game.checkStarted("notStarted"))
        self.assertFalse(self.game.checkStarted("started"))

        self.game.started = True
        self.assertFalse(self.game.checkStarted("notStarted"))
        self.assertTrue(self.game.checkStarted("started"))

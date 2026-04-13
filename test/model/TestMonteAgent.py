import unittest
from model.MonteCarloAgent import MonteCarloAgent
from model.AIPlayer import AIPlayer
from model.Board import Board
from model.Ship import Ship


class TestMonteCarloAgent(unittest.TestCase):

    def setUp(self):
        self.agent = MonteCarloAgent()
        self.board = Board(7)
        self.ai = AIPlayer("Monte", 7)
        self.ai.placeShipsRand()

    '''
    helper to place both fleets so the game can be started
    '''
    def placeFleet(self, board):
        shipPos = [
            [(0,0),(0,1),(0,2),(0,3),(0,4)],
            [(1,0),(1,1),(1,2),(1,3)],
            [(2,0),(2,1),(2,2)],
            [(3,0),(3,1),(3,2)],
            [(4,0),(4,1)]
        ]
        for ship, pos in zip(self.ai.fleet, shipPos):
            board.placeShip(ship, pos)


    def test_init(self):
        self.assertEqual(self.agent.minSims, 500)
        self.assertEqual(self.agent.maxSims, 3000)


    def test_chooseAttack(self):
        self.placeFleet(self.board)

        unsunk = [ship for ship in self.board.ships if not ship.isSunk()]
        agent = MonteCarloAgent(minSims=50, maxSims=50)
        row, col = agent.chooseAttack(self.board, unsunk)
       
        self.assertGreaterEqual(row, 0)
        self.assertLess(row, 7)
        self.assertGreaterEqual(col, 0)
        self.assertLess(col, 7)

    def test_chooseNotAlrAttack(self):
        self.placeFleet(self.board)
        self.board.attacked(0, 0)
        self.board.attacked(0, 1)
        self.board.attacked(0, 2)
      
        unsunk = [ship for ship in self.board.ships if not ship.isSunk()]
        agent = MonteCarloAgent(minSims=50, maxSims=50)
        row, col = agent.chooseAttack(self.board, unsunk)
      
        self.assertNotIn((row, col), self.board.attacks)


    def test_probabilityMapShape(self):
        self.placeFleet(self.board)

        unsunk = [ship for ship in self.board.ships if not ship.isSunk()]
        agent = MonteCarloAgent(minSims=50, maxSims=50)
        probMap = agent.probabilityMap(self.board, unsunk)
      
        self.assertEqual(len(probMap), 7)
        self.assertEqual(len(probMap[0]), 7)
   
    def test_probabilityMapRange(self):
        self.placeFleet(self.board)
      
        unsunk = [ship for ship in self.board.ships if not ship.isSunk()]
        agent = MonteCarloAgent(minSims=50, maxSims=50)
        probMap = agent.probabilityMap(self.board, unsunk)
      
        for row in probMap:
            for val in row:
                self.assertGreaterEqual(val, 0.0)
                self.assertLessEqual(val, 1.0)


    def test_runSim(self):
        self.placeFleet(self.board)

        unsunk = [ship for ship in self.board.ships if not ship.isSunk()]
        result = self.agent.runSim(self.board, unsunk)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 7)
        self.assertEqual(len(result[0]), 7)
    
    def test_runSimHits(self):
        self.placeFleet(self.board)
        self.board.attacked(0, 0)

        unsunk = [ship for ship in self.board.ships if not ship.isSunk()]
        for _ in range(20):
            result = self.agent.runSim(self.board, unsunk)
            if result is not None:
                self.assertTrue(result[0][0])
    
    def test_runSimBlockedCells(self):
        blocked = Board(5)
        for row in range(5):
            for col in range(5):
                blocked.attacked(row, col)
        unsunk = [Ship("Carrier", 5)]
        result = self.agent.runSim(blocked, unsunk)
        self.assertIsNone(result)


    def test_isValidEmpty(self):
        simGrid = [[False for _ in range(7)] for _ in range(7)]
        pos = [(0,0),(0,1),(0,2)]
    
        self.assertTrue(self.agent.isValid(pos, self.board, simGrid))
 
    def test_isValidMiss(self):
        self.board.attacked(0, 0)
        simGrid = [[False for _ in range(7)] for _ in range(7)]
        pos = [(0,0),(0,1),(0,2)]
    
        self.assertFalse(self.agent.isValid(pos, self.board, simGrid))

        simGrid[1][1] = True
        pos = [(1,1),(1,2),(1,3)]
        self.assertFalse(self.agent.isValid(pos, self.board, simGrid))
  
    def test_isValidHit(self):
        destroyer = Ship("Destroyer", 2)
        self.board.placeShip(destroyer, [(0,0),(0,1)])
        self.board.attacked(0, 0)

        simGrid = [[False for _ in range(7)] for _ in range(7)]
        pos = [(0,0),(0,1)]
        self.assertTrue(self.agent.isValid(pos, self.board, simGrid))


    def test_generatePosSize(self):
        for size in [2, 3, 4, 5]:
            pos = self.agent.generatePos(size, 7)
          
            self.assertEqual(len(pos), size)
  
    def test_generatePosBounds(self):
        for _ in range(100):
            pos = self.agent.generatePos(3, 7)
          
            for row, col in pos:
                self.assertGreaterEqual(row, 0)
                self.assertLess(row, 7)
                self.assertGreaterEqual(col, 0)
                self.assertLess(col, 7)

    def test_generatePosContiguous(self):
        for _ in range(100):
            pos = self.agent.generatePos(4, 7)
            rows = [r for r, _ in pos]
            cols = [c for _, c in pos]
        
            if len(set(rows)) == 1:
                self.assertEqual(max(cols) - min(cols), len(pos) - 1)
            else:
                self.assertEqual(max(rows) - min(rows), len(pos) - 1)


    def test_applyFilterImpossible(self):
        smallBoard = Board(5)
        destroyer = Ship("Destroyer", 2)
        smallBoard.placeShip(destroyer, [(0,0),(0,1)])
      
        for col in range(5):
            smallBoard.attacked(0, col)
        for col in range(5):
            smallBoard.attacked(1, col)
        for col in range(5):
            smallBoard.attacked(2, col)
        for col in range(4):
            smallBoard.attacked(3, col)
        for col in range(5):
            smallBoard.attacked(4, col)
      
        probMap = [[1.0 for _ in range(5)] for _ in range(5)]
        self.agent.applyFilter(probMap, smallBoard, 2)
      
        self.assertEqual(probMap[3][4], 0.0)
  
    def test_applyFilter_skipsAttacked(self):
        self.placeFleet(self.board)
        self.board.attacked(3, 3)

        probMap = [[1.0 for _ in range(7)] for _ in range(7)]
        self.agent.applyFilter(probMap, self.board, 2)
     
        self.assertEqual(probMap[3][3], 1.0)

if __name__ == "__main__":
    unittest.main()


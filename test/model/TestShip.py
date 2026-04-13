import unittest
from model.Ship import Ship, createShips


class TestShip(unittest.TestCase):


   def setUp(self):
       self.ship = Ship("Destroyer", 2)


   def test_init(self):
       self.assertEqual(self.ship.name, "Destroyer")
       self.assertEqual(self.ship.size, 2)
       self.assertEqual(self.ship.positions, [])
       self.assertEqual(self.ship.hits, set())




   def test_validPlaceShip(self):
       self.ship.placeShip([(3,3),(3,4)])
       self.assertEqual(self.ship.positions, [(3,3),(3,4)])


   def test_badSizePlaceShip(self):
       with self.assertRaises(ValueError):
           self.ship.placeShip([(0,0)])




   def test_validHit(self):
       self.ship.placeShip([(0,0),(0,1)])
       result = self.ship.hit(0, 0)
       self.assertTrue(result)
       self.assertIn((0,0), self.ship.hits)


       self.ship.hit(0, 0)
       self.assertEqual(len(self.ship.hits), 1)


   def test_badHit(self):
       self.ship.placeShip([(0,0),(0,1)])
       result = self.ship.hit(1, 1)
       self.assertFalse(result)
       self.assertNotIn((1,1), self.ship.hits)




   def test_notIsSunk(self):
       self.ship.placeShip([(0,0),(0,1)])
       self.ship.hit(0, 0)
       self.assertFalse(self.ship.isSunk())


   def test_sunkIsSunk(self):
       self.ship.placeShip([(0,0),(0,1)])
       self.ship.hit(0, 0)
       self.ship.hit(0, 1)
       self.assertTrue(self.ship.isSunk())


  
   def test_str(self):
       self.assertEqual(str(self.ship), "Ship(Destroyer, size=2, sunk=False)")
       self.ship.placeShip([(0,0),(0,1)])
       self.ship.hit(0, 0)
       self.ship.hit(0, 1)
       self.assertEqual(str(self.ship), "Ship(Destroyer, size=2, sunk=True)")


   def test_createShips(self):
       fleet = createShips()
       self.assertEqual(len(fleet), 5)
       self.assertEqual(fleet[0].name, "Carrier")
       self.assertEqual(fleet[0].size, 5)
       self.assertEqual(fleet[1].name, "Battleship")
       self.assertEqual(fleet[1].size, 4)
       self.assertEqual(fleet[2].name, "Cruiser")
       self.assertEqual(fleet[2].size, 3)
       self.assertEqual(fleet[3].name, "Submarine")
       self.assertEqual(fleet[3].size, 3)
       self.assertEqual(fleet[4].name, "Destroyer")
       self.assertEqual(fleet[4].size, 2)


if __name__ == "__main__":
   unittest.main()

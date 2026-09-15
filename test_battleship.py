import unittest
from Battleship import Board, SmallShip, MediumShip, LargeShip, Orientation, TurnResult, Square


#testing str to make sure it shows -, o, x  
squareUNTOUCHED = Square(4,5)
assert str(squareUNTOUCHED), "   -"

squareMISS = Square(5,5)
squareUNTOUCHED.shot_fired == True
assert str(squareMISS), "   o"

squareBATTLESHIP = Square(2,1)
squareBATTLESHIP.battleship == True
squareBATTLESHIP.shot_fired == True
assert str(squareBATTLESHIP), "   x"


b = Board(rows=10, cols=10)
ship = SmallShip() #should NOT fit off the right edge
assert b.can_place(ship, 0, 10, Orientation.H) == False #should NOT fit off the board. 
#Has to return false if 10 because the board only has 0-9. if it returns true, 
#that means it was able to place a ship outside of of the board
assert b.can_place(ship, 10, 0, Orientation.V) == False 
assert b.can_place(ship, 5, 5, Orientation.H) == True #place ship + check overlap fails on same spot
b.place_ship(ship, 5, 5, Orientation.H)
ship2 = SmallShip() #another smallship
assert b.can_place(ship2, 5, 5, Orientation.H) == False # same location as the first one. testing overlap

#random test
bsb2 = Board(rows=10, cols=10)
small = bsb2.place_ship_random(SmallShip())
med = bsb2.place_ship_random(MediumShip())
large = bsb2.place_ship_random(LargeShip())
assert small == True
assert med == True
assert large == True

#large ship is sunk
ship = LargeShip()
assert ship.is_sunk == False
ship.hits = 1
assert ship.is_sunk == False
ship.hits = 2
assert ship.is_sunk == False
ship.hits = 3
assert ship.is_sunk == True

class TestBoardFireMediumShip(unittest.TestCase):
    """
    Testing that 1 hit to medium size ship returns True for hit
    and returns False for sunk
    """
    def test_fire_hits_medium_ship(self):
        board = Board(rows=5, cols=5)
        ship = MediumShip()
        placed = board.place_ship(ship,0,0,Orientation.H)
        self.assertTrue(placed)
        result = board.fire(0,0)
        self.assertEqual(result,TurnResult.HIT)
        self.assertEqual(ship.hits,1)
        self.assertFalse(ship.is_sunk)

class TestBoardFireSmallShip(unittest.TestCase):
    """
    Testing that 1 hit to small size ship returns sunk
    """
    def test_fire_hits_small_ship(self):
        board = Board(rows=5, cols=5)
        ship = SmallShip()
        placed = board.place_ship(ship,0,0,Orientation.H)
        self.assertTrue(placed)
        result = board.fire(0,0)
        self.assertEqual(result,TurnResult.SUNK)
        self.assertEqual(ship.hits,1)

class TestHittingRepeat(unittest.TestCase):
    """
    Testing that hitting the same spot will return TurnResult.REPEAT 
    """
    def test_repeat_hit_sqaure(self):
        board = Board(rows=5, cols=5)
        result = board.fire(1,1)
        result2 = board.fire(1,1)
        self.assertEqual(result,TurnResult.MISS)
        self.assertEqual(result2,TurnResult.REPEAT)


if __name__ == "__main__":
    unittest.main()

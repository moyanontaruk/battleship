import random
from enum import Enum 

class Square:
    """
    single square that will later be used for 10x10grid 
    2 methods:
    1) __init__
    2) __str__
    """
    def __init__(self, row:int, col:int):
        """ 
        init the Square class.  
        parameters:
            row:int,
            col:int,
        attributes:
            battleship on square starts at None,
            shot_fired = False then changes to True if shot at
        """
        self.row = row 
        self.col = col
        self.battleship = None
        self.shot_fired = False

    def __str__ (self) -> str:
        """
        returns a string:
        (-) untouched, (x)hit, or (O)missed thats 3 spaces wide
        """
        if not self.shot_fired: 
            symbol = "-" #untouched
        elif self.battleship: 
            symbol = "x" #hit
        else:
            symbol = "o" #miss
        return f"{symbol:>3}" 

class Orientation(Enum): # this is for placing the ship in the orientation, preset options, can only be those options 
    """
    Orientation of the ship either H or V
    """
    H = "H"
    V = "V" 

class TurnResult(Enum):
    """
    outcome of when a shot is fired
    """
    HIT = "Hit"
    MISS = "Miss"
    REPEAT = "Repeat"
    SUNK = "Sunk"

class Battleship:
    """
    Battleship class has 2 methods: 
    1) __init__
    2) is_sunk 

    represents ships placed on the board

    """
    def __init__(self, size: int):
        """
        init Battleship class.
        parameters:
            size of battleship, # of squares it'll be (getting from outside the method).
        attributes: 
            size - length of ship
            hits - how many hits
            Square - how many squares it takes up depends on the ships
        """
        self.size:int = size
        self.hits:int = 0  #same concept as score. starting at 0 because it depends where player select 
        self.square: list = []
        #self.sqr = this is where the location of the ships WOULD be but at this point it has not been created     
    @property 
    def is_sunk(self) -> bool: 
        """ 
        return true if hits is greater size size of ship = sunk
        """
        return self.hits >= self.size

# super refers to the parent class (battleship), pulls the attributes, ".__init__" assigns the attribute a value
class SmallShip(Battleship):
    """
    Subclass of Battleship class. 
    3 ships of this size that takes up 1 squares
    """
    MAX_COUNT = 3 #how many ships of this size 
    def __init__(self):
        super().__init__(1) #what the size of this ship is
class MediumShip(Battleship):
    """
    Subclass of Battleship class. 
    There is 2 ships of this size that takes up 2 squares
    """
    MAX_COUNT = 2
    def __init__(self):
        super().__init__(2)
class LargeShip(Battleship):
    """
    Subclass of Battleship class. 
    There is 1 ships of this size that takes up 3 squares
    """
    MAX_COUNT = 1
    def __init__(self):
        super().__init__(3)
 
class Board: #we defining grid now, earlier we only defined each single sqr
    """ 
    Board class has 6 methods:
    1) __init__
    2) __str__
    3) can_place
    4) place_ship
    5) place_ship_random
    6) fire

    the game board. has a grid of Square objects and tracks ships placed
    """
    def __init__ (self, rows:int =  10, cols:int = 10): #=10 because it's a 10x10 board not (1,10) b/c thats a list
        """
        init the board
        Method in Board class -
        parameters:
            rows: int - number of rows,
            cols: int - number of cols,
        attributes:
            ship: list - all ships on board,
            grid: list - list representing squares on the board
        """
        self.rows = rows
        self.cols = cols
        self.ship:list = [] #putting it here so we can call all ships(win check, counting sunk ships, save/load ) without scanning whole grid each time
        self.grid:list= []  #empty, will need to append going down the row 0, row 1, row 2 which will create a loop
                            #that goes into cols left to right. 
        for r in range (rows):
            r_list:list = []
            for c in range (cols): #nested loop, "for c" is inside the one above because once the r_list is met then continue on
                r_list.append(Square(r,c)) #b/c we're calling the square class and it doesn't matter what we call
                                           #(r,c) after because it's the order that matters which is row + col
            self.grid.append (r_list) # we've left the inner loop, went outside to call self.grid 
                                      #to add what the new stuff we added in the r_list

    def __str__(self) -> str:
        """
        return a str representation of the board
        """
        firstblock = "  " #starting block of the board
        for r in range (self.rows):
            a = str(r)
            firstblock += f"{a:>3}" 
        out = firstblock + "\n"

        for c in range (self.rows):
            colfirstblock = f"{c:>2}" 
            for i in range(self.cols):
                colfirstblock += str(self.grid[c][i])
            out += colfirstblock + "\n"
        return out

    def can_place (self,ship,row:int, col:int, orientation:Orientation):
        """
        Checking ship stays within boundaries and not overlapping.
        parameters:
            ship from battleship to place
            row:int,
            col:int,
            orientation:Orientation(class) either H or V
        return true if all passes, place ship
        """
        if row < 0 or col < 0 or row >= self.rows or col >= self.cols:
            return False #safety net, making sure input is within board
        if orientation == Orientation.H:
            end_col = col+ship.size -1
            if end_col >= self.cols:
                return False
            for c in range(col, col + ship.size):  #check overlap H.
                if self.grid[row][c].battleship is not None:
                    return False
        else: #orientation V
            end_row = row + ship.size -1
            if end_row >= self.rows:
                return False
            for r in range(row, row + ship.size): #checking overlap V
                if self.grid[r][col].battleship is not None:
                    return False
        return True #if all passes, move on to next

    def place_ship(self,ship, row:int, col:int, orientation: Orientation):
        """
        places ship on the board, checks with can_place first. 
        Once passes, return True to place ship and tracks ship in the board's ship list
        parameters:
            ship from battleship to place
            row:int
            col:int
            orientation:Orientation(class) H or V
        """
        if not self.can_place(ship,row,col,orientation): # calling the function from above
            return False # putting as a safety net to make sure AGAIN that the ship can actually be placed
        if orientation == Orientation.H:
            for c in range(col, col + ship.size):
                sq = self.grid[row][c]
                sq.battleship = ship
                ship.square.append(sq)
        else: #this is V since above is H
            for r in range(row, row + ship.size):
                sq = self.grid[r][col]
                sq.battleship = ship
                ship.square.append(sq)
        self.ship.append(ship)
        return True

    def place_ship_random(self, ship, max_attempt:int = 222): 
        """
        placing ship at random on the board ensuring it is valid (from can_place) or max attempt is hit.
        parameters:
            ship from battleship to place
            max_attempt:int.
        return True if ship was placed, false if not.
        """
        for i in range(max_attempt):
            row: int = random.randint(0, self.rows - 1)
            col: int = random.randint(0, self.cols - 1)
            orientation = random.choice([Orientation.H, Orientation.V])
            if self.can_place(ship, row, col, orientation): #this has to come back true or else it fails the assert test
                self.place_ship(ship, row, col, orientation)
                return True
        return False

    def fire(self, row:int, col:int):
        """
        fire at a sqaure on the board. ensuring the fire is within boundaries.
        if out of boundaries or already hit, return TurnResult.REPEAT
        TurnResult.HIT if fire hits ship
        TurnResult.SUNK if fire sinks ship
        TurnResult.MISS if no ship in square
        parameters:
            row:int,
            col:int,
        """
        if row < 0 or col < 0 or row >= self.rows or col >= self.cols: #if out of range, repeat
            return TurnResult.REPEAT #if any of above is true, returm repeat
        sq = self.grid[row][col]
        if sq.shot_fired:
            return TurnResult.REPEAT #if already shot at the spot, repeat
        sq.shot_fired = True
        if sq.battleship:
            sq.battleship.hits += 1
            if sq.battleship.is_sunk: #putting after the True part because if the shot is missed, 
                                      #it wont record MEANING the same spot can be fired again. 
                return TurnResult.SUNK
            return TurnResult.HIT
        else:
            return TurnResult.MISS

class Player():
    """
    player in the game
    """
    def __init__(self, name: str, board: Board):
        """
        init a Player 
        parameters:
            Name: str--of player,
            board: Board(class) both player shares.
        attributes:
            score:int -- player's name and current score
        """
        self.name:str = name
        self.board:Board = board #self.board because both plays shares and uses the same board 
        self.score:int = 0 #because that is what the value starts at before starting the game

    def __str__(self) -> str:
        """
        str - return player name and score
        """
        return f"{self.name}: {self.score} points"

#keeping taking turns outside any class because it'll be easier to test if it's an I/O issue
#take_turns = takes player input, calls board.fire(),prints result, adds 1 point for SUNK
def take_turns(player, board:Board):
    """
    gets player to input row/col, checks for invalid unput, update score for sunk.

    return = result = board.fire

    parameters:
    player,
    board:Board(class).
    """
    while True:
        try:
            row, col = map(int, input(f"{player.name}, Enter your guess (row col): ").split())
            break
        except ValueError:
            print("Invalid input. Enter two numbers like 5 8")
    result = board.fire(row,col)
    print(f"{player.name} fired at {row, col} -> {result.value}")
    if result in (TurnResult.HIT, TurnResult.MISS, TurnResult.REPEAT):
        player.score += 0
    else:
        player.score += 1 #only point for SUNK
    print(f"Current Score - {player.name}: {player.score}")
    return result

def getting_player_name(PlayerName) -> str:
    """Function.
    if player name entered is empty, 
    return to top of function to ask again untill a non-empty input is recevied.
    """
    try:
        name = input(PlayerName).strip()
        if not name:
            raise ValueError("Name cannot be blank.")
        return name
    except ValueError as errorerror:
        print(errorerror)
        return getting_player_name(PlayerName)

def play_game():
    """
    both player inputs name, creates board and randomly places ship, 
    player takes turn and goes till all ship are sunk. 
    prints winner and scores
    """
    print("LET THE GAMES BEGIN")
    player_1_name: str = getting_player_name("Player 1, Enter your name: ")
    print(f"Ready, Player 1: {player_1_name}")
    player_2_name: str = getting_player_name("Player 2, Enter your name: ")
    print(f"Ready, Player 2: {player_2_name}")
    board = Board()
    for small in range(SmallShip.MAX_COUNT): # loop runs, creates a small ship -> calls Board -> random method in there -> 3 times
        board.place_ship_random(SmallShip()) 
    for medium in range(MediumShip.MAX_COUNT):
        board.place_ship_random(MediumShip())
    for large in range(LargeShip.MAX_COUNT):
        board.place_ship_random(LargeShip())

    p1 = Player(player_1_name, board)
    p2 = Player(player_2_name, board)

    current, other = p1, p2

    while True:
        print(board)
        print(f"Current Score - \n{player_1_name}: {p1.score}\n{player_2_name}: {p2.score}")
        result = take_turns(current, board)
        if result ==  TurnResult.REPEAT:
            print(f"{current.name}, that shot was invalid or already selected.\nTRY AGAIN!")
            continue #keep asking, dont switch to other player
        all_sunk = True
        for ship in board.ship:
            if not ship.is_sunk:
                all_sunk = False
                break
        if all_sunk:#game end if so
            break
        current, other = other, current #switching players, corrected the repeating player name here
                                        #issue - player.name kept looping to only the first player and not second 
    print("~~~~Game Oveeerrrrr~~~~")
    if p1.score > p2.score:
        print(f"{p1.name} is the winner!\nFinal score:\n{p1.name} {p1.score}\n{p2.name}: {p2.score}")
    elif p2.score > p1.score:
        print(f"{p2.name} is the winner!\nFinal score:\n{p2.name} {p2.score}\n{p1.name}: {p1.score}")
    else:
        print(f"IT'S A TIE!\n{p1.name}: {p1.score}\n{p2.name}: {p2.score}")

if __name__ == "__main__":
    play_game()
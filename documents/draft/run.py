
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from nnf import Var
import random

from sqlalchemy import true

# Encoding that will store all of your constraints
E = Encoding()

# GLOBAL VARIABLES
# Board size (we can change this; doesn't have to be a square either)
BOARD_SIZE = 6

# we might use this for walls and for possible moves for Theseus or Minotaur
DIRECTIONS = ['top', 'bottom', 'left', 'right']

# Minotaur gets 2 turns for each one Theseus gets
MINOTAUR_TURNS = 2
THESEUS_TURNS = 1

# Number of turns and hedges
NUM_ROUNDS = random.randint(0, 30)
NUM_HEDGES = random.randint(0, 20)

# Initialize arrays for players/things as well as game grid
def init_grid():
    grid = []
    for i in range(BOARD_SIZE):
        row = []
        for j in range(BOARD_SIZE):  #Assigns a name to each grid space for visual purposes
            row.append(False) #initialize each space to False
        grid.append(row)
    print(grid)
    return grid

# Assign initialized arrays to each player/thing
def place_variable(var):
    var_pos = init_grid()
    p = random.randint(0, BOARD_SIZE)
    q = random.randint(0, BOARD_SIZE)
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if i == p and j == q:
                var_pos[i][j] = True
            else:
                var_pos[i][j] = False
    return var_pos
    
# Create the initial positions of the variables  
thes = place_variable('thes') # Theseus
mino = place_variable('min') # Minotaur
goal = place_variable('goal') # Where Theseus is trying to go


# Initialize a list for the turn number. The current turn number will be set to True, and 
# everything else to False. When all elements are set to False, the game ends.
def init_turn(turn_num):
    turns = []
    # turn 0 is when we create the board for the first time, so no one moves - hence we 
    # add an extra at the end to actually have NUM_TURNS turns
    for i in range(NUM_ROUNDS+1):
        if i == turn_num:
            turns.append(True)
        else:
            turns.append(False)

# Get position of player/thing
def pos(var):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if (place_variable(var)[i][j] == str(var)):
                pos = place_variable(var)[i][j]
                return pos
    
# Set the row, col indices on the board
def set_board():
    # If one variable is true for this square, the other variables must be false
    # Iterate through the board square by square
    t = True
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if (pos(thes) == grid[x][y]):
                t &= thes[x][y] # "The board is true AND Theseus' position is True", it then follows that the rest of the variables are false for this position
                t &= ~mino[x][y]
                t &= ~goal[x][y]
            elif (pos(mino) == grid[x][y]):
                t &= mino[x][y]
                t &= ~thes[x][y]
                t &= ~goal[x][y]
            elif (pos(goal) == grid[x][y]):
                t &= goal[x][y]
                t &= ~thes[x][y]
                t &= ~mino[x][y]
            else:
                t &= ~thes[x][y]
    return t

# Set the hedges (mini-walls) inside the maze. Generate some random number of hedges at some random
# squares, then choose some random direction for each hedge.
def set_hedges():
    # 2D arrays for hedge locations and directions
    vert_hedges_bool = init_grid() # T if hedge at right side of square, F if not
    hor_hedges_bool = init_grid() # T is hedge at top of square, F if not
    
    # Generate coordinates and directions for hedges.
    # For each hedge, generate 2 coordinates and one direction.
    for i in range(NUM_HEDGES):
        row = random.randint(0, BOARD_SIZE-1)
        col = random.randint(0, BOARD_SIZE-1)
        dir = DIRECTIONS[random.randint(0,3)]

        if dir == 'left':
            vert_hedges_bool[row][col-1] = True
        elif dir == 'right':
            vert_hedges_bool[row][col] = True
        elif dir == 'top':
            hor_hedges_bool[row][col] = True
        elif dir == 'bottom':
            hor_hedges_bool[row+1][col] = True
    return vert_hedges_bool, hor_hedges_bool

# GLOBAL VARIABLE - HEDGE POSITIONS WILL NEVER CHANGE THROUGHOUT GAME
VERT_HEDGES, HOR_HEDGES = set_hedges()
    
                
def within_borders(target_row, target_col):
    """
    @param: target_row (int), row index of square being queried
    @param: target_col (int), col index of square being queried
    @return: True if square in board, False otherwise
    NOT COMPLETED.
    """
    #border = index is out of range of BORDER SIZE
    #if move = same index as border square return false
    
    border_square = grid[BOARD_SIZE][BOARD_SIZE]
    
    
def minotaur_constraints(mino_row, mino_col, thes_row, thes_col, target_row, target_col):
    """"
    Defines constraints on Minotaur's moves.
    Minotaur cannot move out of the board or cross a wall.
    Minotaur will always try to move closer to Theseus. If he can do so by moving horizontally,
    he will move horizontally. He will move vertically iff he cannot get closer to Theseus by moving
    horizontally.
    @param: mino_row (int), Minotaur's current row position
    @param: mino_col (int), Minotaur's col position
    @param: thes_row (int), Theseus' row position
    @param: thes_col (int), Theseus' col position
    @param: target_row (int), row index of square being queried for Minotaur's move
    @param: target_col (int), col index of square being queried for Minotaur's move
    @return: True if Minotaur can move to [row,col] according to rules, False otherwise
    """
    # do stuff

def theseus_constraints(thes_row, thes_col, mino_row, mino_col, target_row, target_col):
    '''
    Defines constraints on Theseus' moves.
    Theseus cannot move out of the board or cross a wall.
    Theseus cannot move to a square that is within the Minotaur's reach.
    @param: thes_row (int), Theseus' row position
    @param: thes_col (int), Theseus' col position
    @param: mino_row (int), Minotaur's row position
    @param: mino_col (int), Minotaur's col position
    @param: target_row (int), row index of square being queried for Theseus' move
    @param: target_col(int), column index of square being queried for Theseus' move
    @return: True if Theseus can move to [row, col], False otherwise
    '''
    # Check if the target square is out of bounds
    if not within_borders(target_row, target_col):
        return False
        
    # Check if target square is within range for Theseus
    if not ( (target_row == thes_row + 1 and target_col == thes_col) or 
             (target_row == thes_row - 1 and target_col == thes_col) or
             (target_row == thes_row and target_col == thes_col + 1) or
             (target_row == thes_row and target_col == thes_col -1) ):
        return False
    
    # Check if there are walls preventing Theseus from moving to the target square.
    # Target square 1 to right of Theseus' current position.
    if target_row == thes_row and target_col == thes_col + 1 and VERT_HEDGES[thes_row][thes_col]:
        return False
    # Target square 1 to left
    elif target_row == thes_row and target_col == thes_col - 1 and VERT_HEDGES[thes_row][thes_col-1]:
        return False
    # Target square 1 up
    elif target_row == thes_row - 1 and target_col == thes_col and HOR_HEDGES[thes_row][thes_col]:
        return False
    # Target square 1 down
    elif target_row == thes_row + 1 and target_col == thes_col and HOR_HEDGES[thes_row+1][thes_col]:
        return False

    # DON'T-GET-EATEN CONSTRAINTS HERE #

    # Check if Theseus is moving onto the Minotaur's square... obviously bad idea
    if target_row == mino_row and target_col == mino_col:
        return False

    # Theseus can move within 2 squares horizontally or vertically or 1 square diagonally of
    # Minotaur and be safe if there are hedges between him and the Minotaur. Recall that
    # hedges are represented by 2D Boolean array - for vertical hedges, True if there is
    # a hedge to the right of the square, False otherwise; for horizontal hedges, True if
    # there is a hedge at the top of the square; False otherwise.

    # Check scenarios for if Theseus is already in same col as Minotaur and only moving rows.
    if thes_col == mino_col:
        safe = False # tracker - true if square determined to be safe because of hedges, false otherwise
        # Target square 2 directly above Minotaur
        if target_row == mino_row - 2:
            if HOR_HEDGES[mino_row][mino_col] or HOR_HEDGES[target_row+1][target_col]:
                safe = True
        # Target square 1 above Minotaur
        elif target_row == mino_row - 1:
            if HOR_HEDGES[mino_row][mino_col]:
                safe = True
        # Target square 1 below Minotaur
        elif target_row == mino_row + 1:
            if HOR_HEDGES[target_row][target_col]:
                safe = True
        # Target square 2 below Minotaur
        elif target_row == mino_row + 2:
            if HOR_HEDGES[target_row][target_col] or HOR_HEDGES[target_row-1][target_col]:
                safe = True
        if safe == False:
            return False
    
    # Theseus already in same row as Minotaur and only moving cols.
    if thes_row == mino_row:
        safe = False
        # Target square 2 left of Minotaur
        if target_col == mino_col - 2:
            if VERT_HEDGES[target_row][target_col] or VERT_HEDGES[target_row][target_col+1]:
                safe = True
        # Target square 1 left of Minotaur
        elif target_col == mino_col - 1:
            if VERT_HEDGES[target_row][target_col]:
                safe = True
        # Target square 1 right of Minotaur
        elif target_col == mino_col + 1:
            if VERT_HEDGES[mino_row][mino_col]:
                safe = True
        # Target square 2 right of Minotaur:
        elif target_col == mino_col + 2:
            if VERT_HEDGES[mino_row][mino_col] or VERT_HEDGES[mino_row][mino_col+1]:
                safe = True
        if safe == False:
            return False

    # Theseus moved to square diagonal from Minotaur. For safety, he needs a minimum of two hedges.
    # Possible scenarios: 1) 2 hedges set perpendicular to each other block off Minotaur from Theseus
    # 2) 2 hedges set perpendicular to each otehr block off Theseus from Minotaur
    # 3) 2 hedges vertically separating them
    # 4) 2 hedges horizontally separating them
    # Target square is one down, one to left of Minotaur
    if target_row == mino_row + 1 and target_col == mino_col - 1:
        safe = False
        if VERT_HEDGES[target_row][target_col] and (VERT_HEDGES[target_row-1][target_col] or
                                                    HOR_HEDGES[target_row][target_col]):
            safe = True
        elif HOR_HEDGES[target_row][target_col+1] and (VERT_HEDGES[target_row-1][target_col]
                                                        or HOR_HEDGES[target_row][target_col]):
            safe = True
        if safe == False:
            return False
    # Target square is one down, one to right of Minotaur
    elif target_row == mino_row + 1 and target_col == mino_col + 1:
        safe = False
        if HOR_HEDGES[target_row][target_col-1] and (VERT_HEDGES[target_row-1][target_col-1]
                                                    or HOR_HEDGES[target_row][target_col]):
            safe = True
        elif VERT_HEDGES[target_row][target_col-1] and (VERT_HEDGES[target_row-1][target_col-1]
                                                        or HOR_HEDGES[target_row][target_col]):
            safe = True
        if safe == False:
            return False
    # Target square is one up, one to left of Minotaur
    elif target_row == mino_row - 1 and target_col == mino_col - 1:
        safe = False
        if VERT_HEDGES[target_row][target_col] and (HOR_HEDGES[target_row+1][target_col]
                                                    or VERT_HEDGES[target_row+1][target_col]):
            safe = True
        elif HOR_HEDGES[target_row+1][target_col+1] and (VERT_HEDGES[target_row+1][target_col]
                                                        or HOR_HEDGES[target_row+1][target_col]):
            safe = True
        if safe == False:
            return False
    # Target is one up, one to right of Minotaur
    elif target_row == mino_row - 1 and target_col == mino_col + 1:
        safe = False
        if VERT_HEDGES[target_row+1][target_col-1] and (HOR_HEDGES[target_row+1][target_col-1]
                                                        or VERT_HEDGES[target_row][target_col-1]):
            safe = True
        elif HOR_HEDGES[target_row+1][target_col] and (VERT_HEDGES[target_row][target_col-1]
                                                        or HOR_HEDGES[target_row-1][target_col-1]):
            safe = True
        if safe == False:
            return False

    # If we get this far, the target square is OK.
    return True
            

def player_moves(player, player_pos):
    '''
    Determine the valid moves for a given player, using constraints determined
    by theseus_constraints or minotaur_constraints as applicable
    @param: player (string), Theseus or Minotaur
    @param: row (int), horizontal index of player position
    @param: col (int), vertical index of player position
    @return: a list of valid moves
    '''
    moves = init_grid()
    if player == 'Theseus':
        # access his position, then query moves one up, down, left, and right with theseus_constraints()



'''
CONSTRAINTS:

- Theseus cannot cross a wall - i.e. Theseus cannot move if it would put him outside of the length/width of the maze

- Minotaur cannot cross a wall - i.e. Minotaur cannot move if it would put him outside of the length/width of the maze

- Minotaur will only make moves that bring him closer to Theseus

- Minotaur will move horizontally before vertically 
  (only moves vertical if he can't get closer horizonally)

- Theseus and Minotaur cannot move up if "bottom" wall above, cannot move down if "top" wall below, 
  cannot move right if "left" wall to the right and cannot move left if "right" wall to the left

- Theseus and Minotaur cannot move up if space they are currently on has "top" wall condition, cannot move down if space they are currently on has "bottom" wall condition,
  cannot move right if space they are currently on has "right" wall condition, cannot move left if space they are currently on has "left" wall condition

- Theseus can't move into a square that is one away from the Minotaur

- Minotaur will only make a move if it makes him closer to Theseus, otherwise won't move

- Theseus will only move if he gets closer to the escape spot

- Theseus will pick the best move possible that will get him clsoest to the escape spot
  (need to look at 2-3 steps ahead to determine what the best move is)
'''





# Different classes for propositions are useful because this allows for more dynamic constraint creation
# for propositions within that class. For example, you can enforce that "at least one" of the propositions
# that are instances of this class must be true by using a @constraint decorator.
# other options include: at most one, exactly one, at most k, and implies all.
# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    # Add custom constraints by creating formulas with the variables you created. 
    E.add_constraint((a | b) & ~x)
    # Implication
    E.add_constraint(y >> z)
    # Negate a formula
    E.add_constraint(~(x & y))
    # You can also add more customized "fancy" constraints. Use case: you don't want to enforce "exactly one"
    # for every instance of BasicPropositions, but you want to enforce it for a, b, and c.:
    constraint.add_exactly_one(E, a, b, c)

    return E


if __name__ == "__main__":

    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()

"""
References: 
    https://github.com/mkevinq/checkmate-finder/blob/main/run.py
    https://github.com/CzJLee/Minotaur-Project/blob/master/board_class.py
    https://github.com/boosungkim/python-chess/blob/master/Piece.py
    https://github.com/CzJLee/Minotaur-Project

"""

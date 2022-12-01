from bauhaus import Encoding, proposition, constraint
from nnf import config
import random

# SUMMARY OF FUNCTIONS/BRIEF CODE DOCUMENTATION HERE:
# https://docs.google.com/document/d/1cW7keLwbJXumtzpbQCZ_Dcds2fXrwDSy-KxJAeD6IaA/edit

config.sat_backend = "kissat"

E = Encoding()

# Constants
BOARD_SIZE = 6
DIRECTIONS = ['top', 'bottom', 'left', 'right']
# Due to the recursive nature of the code, round numbers over 15
# tend to start taking a REALLY long time, so we have limited it here
# Even with 13-15 moves, sometimes it can take a really long time - 
# if that happens, try killing the process and running the program again.
# This is one of the biggest limitations of our current implementation.
NUM_ROUNDS = random.randint(0, 15)
NUM_HEDGES = random.randint(5, 40)

# For example_theory_1, uncomment the line below
#NUM_ROUNDS = 3

# For example_theory_2, uncomment the line below
#NUM_ROUNDS = 8

# For example_theory_3, uncomment the line below
#NUM_ROUNDS = 14

# Proposition to describe Theseus' current position
@proposition(E)
class ThesPos:
    def __init__(self, x, y):
        '''
        Constructor to initialize Theseus' x and y position.
        @params: x, y (ints) 0-based row, col indices
        '''
        self.x = x
        self.y = y

    def set(self, x, y):
        '''
        Sets Theseus' x, y position.
        @params: x, y (ints) row, col indices
        '''
        self.x = x
        self.y = y

    def get(self):
        '''
        No args.
        @return: row, col index of Theseus' position
        '''
        return self.x, self.y


# Proposition to describe Minotaur's current position
@proposition(E)
class MinoPos:
    def __init__(self, x, y):
        '''
        Constructor to initialize Minotaur's x, y position.
        @params: x, y (ints) row, col indices
        '''
        self.x = x
        self.y = y
    
    def set(self, x, y):
        '''
        Sets Minotaur's x, y position.
        @params: x, y (ints), row, col indices
        '''
        self.x = x
        self.y = y

    def get(self):
        '''
        No args.
        @return: row, col index of Minotaur position
        '''
        return self.x, self.y


# Constraint to describe the exit square
@constraint.exactly_one(E)
@proposition(E)
class ExitSquare:
    def __init__(self, x, y):
        '''
        Constructor to set the exit square (should never be changed)
        @params: x, y (ints) row, col indices
        '''
        self.x = x
        self.y = y

    def get(self):
        '''
        No args.
        @return: row, col index of exit square (ints)
        '''
        return self.x, self.y


# Proposition for the maze to have hedges
@constraint.at_least_one(E)
@proposition(E)
class Hedges:
    def __init__(self):
        '''
        Constructor for hedge objects. Hedges should never be modified.
        No args.
        '''
        self.vert, self.hor = Hedges.set_hedges()

    def hedge_grid():
        '''
        Initialize 2D arrays to hold hedge data.
        No args.
        '''
        grid = []
        for i in range(BOARD_SIZE):
            row = []
            for j in range(BOARD_SIZE):
                row.append(False)
            grid.append(row)
        return grid

    def set_hedges():
        '''
        Initialize hedges. True in horizontal hedges means a hedge exists 
        at the right side, and True in vertical hedges means a hedge 
        exists at the top wall. Random number of hedges in random  
        positions generated.
        No args.
        '''
        # 2D arrays for hedge locations and directions
        vert_hedges = Hedges.hedge_grid()
        hor_hedges = Hedges.hedge_grid()

        # Generate coordinates and directions for hedges.
        # For each hedge, generate 2 coordinates and one direction.
        for i in range(NUM_HEDGES):
            row = random.randint(0, BOARD_SIZE - 1)
            col = random.randint(0, BOARD_SIZE - 1)
            dir = DIRECTIONS[random.randint(0, 3)]
            # Set True and False at appropriate indices
            if dir == 'left' and col - 1 >= 0:
                vert_hedges[row][col - 1] = True
            elif dir == 'right':
                vert_hedges[row][col] = True
            elif dir == 'top':
                hor_hedges[row][col] = True
            elif dir == 'bottom' and row + 1 < 6:
                hor_hedges[row + 1][col] = True
        return vert_hedges, hor_hedges


class BoardSquare:
    def __init__(self, x, y):
        '''
        Constructor to initialize the given board square
        (everything set to False).
        No args.
        Fields: Theseus' position, Minotaur's position, hedges, and exit
        square.
        '''
        self.x = x
        self.y = y
        self.t_x = False
        self.t_y = False
        self.m_x = False
        self.m_y = False
        self.EXIT_x = False
        self.EXIT_y = False
        self.top = False
        self.bottom = False
        self.right = False
        self.left = False


def start_board(t_start_x, t_start_y, m_start_x, m_start_y,
                EXIT_x, EXIT_y, VERT_H, HOR_H):
    '''
    Initialize the board with starting positions of Theseus and 
    Minotaur, as well as permanent hedges and a permanent exit square.
    @params: t_start_x, t_start_y (ints)             Theseus' start position
    @params: m_start_x, m_start_y (ints)             Minotaur's start position
    @params: EXIT_x, EXIT_y (ints)                   exit square
    @params: VERT_H, HOR_H  (2D arrays of booleans)  hedges
    @return: the starting board (2D array of BoardSquare objects)
    '''
    # Initialize a 2D array for the board. Fields x,y will be set to
    # the current row, col indices; everything else will be initialized
    # to False.
    board = []
    for x in range(BOARD_SIZE):
        row = []
        for y in range(BOARD_SIZE):
            square = BoardSquare(x, y)
            # Set the fields to true as necessary
            if x == t_start_x and y == t_start_y:
                square.t_x = True
                square.t_y = True
            if x == m_start_x and y == m_start_y:
                square.m_x = True
                square.m_y = True
            if x == EXIT_x and y == EXIT_y:
                square.EXIT_x = True
                square.EXIT_y = True
            if VERT_H[x][y]:  # hedge to the right
                square.right = True
            if HOR_H[x][y]:  #hedge to top
                square.top = True
            row.append(square)
        board.append(row)
    # set left and bottom hedges - if (x,y) has hedge to right, (x,y+1) has hedge to left
    # and if (x,y) has hedge on top, (x-1, y) has hedge on bottom
    # x-1 and y+1 checking to make sure we remain within bounds
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y].right and y + 1 < BOARD_SIZE:
                board[x][y + 1].left = True
            if board[x][y].top and x - 1 >= 0:
                board[x - 1][y].bottom = True
    return board

def set_board(board, t_pos, m_pos):
    '''
    Set the board to the current game state.
    @param: board (2D array of BoardSquare objects)  describes current board config
    @param: t_pos (ThesPos object)      describes Theseus' current position
    @param: m_pos (MinoPos object)      describes Minotaur's current position
    @return: updated configuration of board (2D array of BoardSquare objects)
    '''
    t_x, t_y = t_pos.get()
    m_x, m_y = m_pos.get()
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            # first set the old Theseus and Minotaur squares to False
            if board[x][y].t_x and board[x][y].t_y:
                board[x][y].t_x = False
                board[x][y].t_y = False
            elif board[x][y].m_x and board[x][y].m_y:
                board[x][y].m_x = False
                board[x][y].m_y = False
            # now check if this square is the new Theseus/Minotaur square
            # if so, set the appropriate fields to True
            if x == t_x and y == t_y:
                board[x][y].t_x = True
                board[x][y].t_y = True
            elif x == m_x and y == m_y:
                board[x][y].m_x = True
                board[x][y].m_y = True
    return board

def thes_win(board, t_pos):
    '''
    Determines if Theseus has won the game by checking whether his square is
    the same as the exit square. The function that calls this function first checks if
    Theseus has been eaten by the Minotaur, so we don't need to check that here.
    @param: board (2D array of Board_Square objects)  describes the current game state
    @param: t_pos (ThesPos object)                    Theseus's current x,y position
    @return: boolean (True if Theseus wins, False otherwise)
    '''
    t_row, t_col = t_pos.get()
    if board[t_row][t_col].EXIT_x and board[t_row][t_col].EXIT_y:
        # We're only checking if a solution exists, not how many there possibly could be,
        # so if we pass the condition then we can just clear constraints and force
        # Theseus to be on the exit square
        E.clear_constraints()
        E.add_constraint((t_pos >> ThesPos(board[t_row][t_col].EXIT_x, board[t_row][t_col].EXIT_y)))
        return True
    return False

def thes_eaten(t_pos, m_pos):
    '''
    Determines if Theseus has been eaten by the Minotaur by checking
    whether his square is the same as the Minotaur's.
    @param: t_pos (ThesPos object)  Theseus' current position
    @param: m_pos (MinoPos object)  Minotaur's current position
    @return: boolean (True if Theseus eaten, False otherwise)
    '''
    t_row, t_col = t_pos.get()
    m_row, m_col = m_pos.get()
    if t_row == m_row and t_col == m_col:
        # Theseus being on this square causes him to lose
        E.add_constraint((t_pos & m_pos) >> ~t_pos)
        return True
    return False


# Proposition for Minotaur to make a move
@proposition(E)
class MinoMoves:
    def mino_hedges_in_way(board, targ_row, targ_col, m_row, m_col):
        '''
        Determines if there are hedges between the Minotaur's current position
        and his target square.
        @param: targ_row, targ_col (ints)  x,y position of target square
        @param: m_row, m_col (ints)        x,y of Minotaur's current position
        @return: True if there are hedges in the way, False otherwise
        '''
        # Target square above Minotaur
        # 2 squares above
        if targ_row == m_row - 2 and targ_col == m_col:
            if board[m_row][m_col].top or board[m_row - 1][m_col].top:
                return True
            # if the first conditional evaluates to True and the nested if to False,
            # we can return False and prevent unnecessary evaluation of other conditionals
            return False
        # 1 square above
        elif targ_row == m_row - 1 and targ_col == m_col:
            if board[m_row][m_col].top:
                return True
            return False
        # Target square below
        # 1 square below
        elif targ_row == m_row + 1 and targ_col == m_col:
            if board[m_row][m_col].bottom:
                return True
            return False
        # 2 squares below
        elif targ_row == m_row + 2 and targ_col == m_col:
            if board[m_row][m_col].bottom or board[m_row + 1][m_col].bottom:
                return True
            return False

        # Target square left
        # 2 squares left
        elif targ_row == m_row and targ_col == m_col - 2:
            if board[m_row][m_col].left or board[m_row][m_col - 1].left:
                return True
            return False
        # 1 square left
        elif targ_row == m_row and targ_col == m_col - 1:
            if board[m_row][m_col].left:
                return True
            return False
        # Target square right
        # 1 square right
        elif targ_row == m_row and targ_col == m_col + 1:
            if board[m_row][m_col].right:
                return True
            return False
        # 2 squares right
        elif targ_row == m_row and targ_col == m_col + 2:
            if board[m_row][m_col].right or board[m_row][m_col + 1].right:
                return True
            return False

        # Note that for diagonal moves, there are four possible configs of hedges
        # that can prevent the Minotaur moving to that square. All configs require
        # at least 2 hedges.

        # Target up and to the left
        elif targ_row == m_row - 1 and targ_col == m_row - 1:
            if board[targ_row][targ_col].bottom and (board[targ_row][targ_col].right
                                                    or board[m_row][m_col].top):
                return True
            elif board[m_row][m_col].left and (board[m_row][m_col].top
                                            or board[targ_row][targ_col].right):
                return True
            return False
        # Target up and to right
        elif targ_row == m_row - 1 and targ_col == m_col + 1:
            if board[targ_row][targ_col].bottom and (board[targ_row][targ_col].left
                                                    or board[m_row][m_col].top):
                return True
            elif board[m_row][m_col].right and (board[m_row][m_col].top
                                                or board[targ_row][targ_col].left):
                return True
            return False
        # Target down and to left
        elif targ_row == m_row + 1 and targ_col == m_col - 1:
            if board[targ_row][targ_col].top and (board[targ_row][targ_col].right
                                                or board[m_row][m_col].bottom):
                return True
            elif board[m_row][m_col].left and (board[m_row][m_col].bottom
                                            or board[targ_row][targ_col].right):
                return True
            return False
        # Target down and to right
        elif targ_row == m_row + 1 and targ_col == m_col + 1:
            if board[targ_row][targ_col].top and (board[targ_row][targ_col].left
                                                or board[m_row][m_col].bottom):
                return True
            elif board[m_row][m_col].right and (board[m_row][m_col].bottom
                                                or board[targ_row][targ_col].left):
                return True
            return False

        # I don't know if we need to even set a default case because this function should
        # cover all cases of Minotaur moving squares, but we can always remove it
        return False

    def mino_move(board, m_pos, t_pos, hedges):
        """
        Defines the Minotaur's move according to the algorithm below.
        1) Minotaur cannot move out of the board or cross a wall.
        2) Minotaur will always try to move closer to Theseus. If he can do so by moving horizontally,
           he will move horizontally. He will move vertically iff he cannot get closer to Theseus by moving
           horizontally.
        Note that we don't need to check if the Minotaur's possible move is within the board because
        there is no situation where he would need to move outside of the board to get closer to Theseus.
        @param: board (2D array of Board_Square objects)  current game state
        @param: m_pos (MinoPos object)                    Minotaur's current position
        @param: t_pos (ThesPos object)                    Theseus' current position
        @param: hedges (Hedges object)                    hedges of board
        @return: a (row, col) tuple of the Minotaur's valid move
        """
        mino_row, mino_col = m_pos.get()
        thes_row, thes_col = t_pos.get()
        # Calculate the distances w.r.t. rows and columns between Theseus and Minotaur
        row_diff = mino_row - thes_row
        col_diff = mino_col - thes_col

        # First check horizontal moves
        # Theseus to right of Minotaur
        if col_diff < 0 and not MinoMoves.mino_hedges_in_way(board, mino_row, mino_col + 1,
                                                    mino_row, mino_col):
            # The Minotaur should move one square to the right
            E.add_constraint((m_pos & t_pos & hedges) >> MinoPos(mino_row, mino_col+1))
            return tuple([mino_row, mino_col + 1])
        # Theseus to left of Minotaur
        elif col_diff > 0 and not MinoMoves.mino_hedges_in_way(board, mino_row, mino_col - 1,
                                                    mino_row, mino_col):
            # The Minotaur should move one square to the left
            E.add_constraint((m_pos & t_pos & hedges) >> MinoPos(mino_row, mino_col-1))
            return tuple([mino_row, mino_col - 1])

        # Otherwise, the Minotaur can't get closer to Theseus by moving horizontally, so he tries
        # to move vertically. If he moves vertically and gets closer to Theseus, row_diff should decrease.
        else:  # includes col_diff == 0
            # Theseus below the Minotaur
            if row_diff < 0 and not MinoMoves.mino_hedges_in_way(board, mino_row + 1, mino_col,
                                                    mino_row, mino_col):
                # Minotaur should move one down
                E.add_constraint((m_pos & t_pos & hedges) >> MinoPos(mino_row+1, mino_col))
                return tuple([mino_row + 1, mino_col])
            # Theseus above the Minotaur
            elif row_diff > 0 and not MinoMoves.mino_hedges_in_way(board, mino_row - 1, mino_col,
                                                        mino_row, mino_col):
                # Minotaur should move one up
                E.add_constraint((m_pos & t_pos & hedges) >> MinoPos(mino_row-1, mino_col))
                return tuple([mino_row - 1, mino_col])
        # If none of the above work, the Minotaur skips his turn.
        E.add_constraint((m_pos & t_pos & hedges) >> MinoPos(mino_row, mino_col))
        return tuple([mino_row, mino_col])


# Group of functions to generate possible moves for Theseus
class ThesMoves:
    def within_borders(target_row, target_col):
        """
        Checks if Theseus' target square is in the board.
        @param: target_row (int)  row index of square being queried
        @param: target_col (int)  col index of square being queried
        @return: boolean (True if square in board, False otherwise)
        """
        #if the target row index is 6 or more
        if target_row >= BOARD_SIZE:
            return False
        #if the target row index is less than 0 (wants to move up out of the maze)
        elif target_row < 0:
            return False
        #if the target column index is 6 or more
        elif target_col >= BOARD_SIZE:
            return False
        #if the target column index is less than 0
        elif target_col < 0:
            return False
        else:
            return True

    def mino_within_range(targ_row, targ_col, m_row, m_col):
        '''
        Determines whether Theseus' target square is within range of the Minotaur.
        @param: targ_row, targ_col (ints)  Theseus' target x,y position
        @param: m_row, m_col (ints)        current x,y position of Minotaur
        @return: boolean (False if target square is more than 2 squares away from
        Minotaur horizontally or vertically, or target square is more than 1 square
        away diagonally; True otherwise)
        '''
        # Target square within 2 up, 2 down, 2 left, or 2 right of Minotaur
        if ((abs(targ_row - m_row) <= 2 and targ_col == m_col)
            or (abs(targ_col - m_col) <= 2 and targ_row == m_row)):
            return True
        # Target square is one diagonal from Minotaur
        if (abs(targ_row - m_row) == 1 and abs(targ_col - m_col) == 1):
            return True
        return False
    
    def theseus_constraints(board, t_pos, m_pos, targ_pos, hedges):
        '''
        Defines constraints on Theseus' moves.
        1) Theseus cannot move out of the board or cross a wall.
        2) Theseus cannot move to a square that is within the Minotaur's reach.
        @param: board (2D array of Board_Square objects)  current game state
        @param: t_pos (ThesPos object)                    Theseus' current position
        @param: m_pos (MinoPos object)                    Minotaur's current position
        @param: targ_pos (ThesPos object)                 Theseus' target square
        @param: hedges (Hedges object)                    hedge config of maze
        @return: boolean (True if targ_pos is safe, False otherwise)
        '''
        thes_row, thes_col = t_pos.get()
        mino_row, mino_col = m_pos.get()
        target_row, target_col = targ_pos.get()

        # Check if the target square is out of bounds
        if not ThesMoves.within_borders(target_row, target_col):
            E.add_constraint((t_pos & m_pos & hedges) >> ~targ_pos)
            return False

        # Check if there are hedges preventing Theseus from moving to the target square.
        # Target square 1 to right of Theseus' current position.
        if target_row == thes_row and target_col == thes_col + 1 and board[
            thes_row][thes_col].right:
            E.add_constraint((t_pos & m_pos & hedges) >> ~targ_pos)
            return False
        # Target square 1 to left
        elif target_row == thes_row and target_col == thes_col - 1 and board[
            thes_row][thes_col].left:
            E.add_constraint((t_pos & m_pos & hedges) >> ~targ_pos)
            return False
        # Target square 1 up
        elif target_row == thes_row - 1 and target_col == thes_col and board[
            thes_row][thes_col].top:
            E.add_constraint((t_pos & m_pos & hedges) >> ~targ_pos)
            return False
        # Target square 1 down
        elif target_row == thes_row + 1 and target_col == thes_col and board[
            thes_row][thes_col].bottom:
            E.add_constraint((t_pos & m_pos & hedges) >> ~targ_pos)
            return False

        # DON'T-GET-EATEN CONSTRAINTS HERE #

        # Check if Theseus is moving onto the Minotaur's square... obviously bad idea
        if target_row == mino_row and target_col == mino_col:
            E.add_constraint((t_pos & m_pos & hedges) >> ~targ_pos)
            return False

        # Check if Theseus is moving onto the exit - then we don't need to check
        # if the Minotaur is in range 
        if thes_win(board, targ_pos):
            E.add_constraint((t_pos & m_pos & hedges) >> targ_pos)
            return True

        # Theseus can move within 2 squares horizontally or vertically or 1 square diagonally of
        # Minotaur and be safe if there are hedges between him and the Minotaur.
        if ThesMoves.mino_within_range(target_row, target_col, mino_row, mino_col):
            if not MinoMoves.mino_hedges_in_way(board, target_row, target_col, mino_row,
                                    mino_col):
                E.add_constraint((t_pos & m_pos & hedges) >> ~targ_pos)
                return False

        # If we reach this point, the square is OK.
        return True

    def theseus_moves(board, t_pos, m_pos, hedges):
        '''
        Determine the valid moves for Theseus, using constraints determined
        by theseus_constraints().
        @param: board (2D array of Board_Square objects)  current game state
        @param: t_pos (ThesPos object)                    Theseus' current position
        @param: m_pos (MinoPos object)                    Minotaur's current position
        @param: hedges (Hedges object)                    Hedge config of maze
        @return: list of row,col tuples of Theseus' valid moves. Note that if the list
        is empty, Theseus loses.
        '''
        thes_row, thes_col = t_pos.get()
        # Theseus can move to 4 different squares, or remain in his spot (skip his turn).
        moves = []
        # Move up or down
        if ThesMoves.theseus_constraints(board, t_pos, m_pos, ThesPos(thes_row - 1, thes_col), hedges):
            moves.append(tuple([thes_row - 1, thes_col]))
        if ThesMoves.theseus_constraints(board, t_pos, m_pos, ThesPos(thes_row + 1, thes_col), hedges):
            moves.append(tuple([thes_row + 1, thes_col]))
        # Move left or right
        if ThesMoves.theseus_constraints(board, t_pos, m_pos, ThesPos(thes_row, thes_col + 1), hedges):
            moves.append(tuple([thes_row, thes_col + 1]))
        if ThesMoves.theseus_constraints(board, t_pos, m_pos, ThesPos(thes_row, thes_col - 1), hedges):
            moves.append(tuple([thes_row, thes_col - 1]))
        # Skip turn
        if ThesMoves.theseus_constraints(board, t_pos, m_pos, t_pos, hedges):
            moves.append(tuple([thes_row, thes_col]))
        return moves


def is_winnable(board, t_pos, m_pos, exit, hedges, round_num=0):
    '''
    Determines recursively whether Theseus can win, given a certain board configuration.
    Base Cases:
    1) Theseus has won (his position is the exit square) and Minotaur's position is not exit square. Return True.
    2) Theseus has been eaten (his position is the Minotaur's). Return False.
    3) Theseus has run out of moves and loses (round_num = NUM_ROUNDS). Return False.
    If we get this far, generate a list of his viable moves.
    4) Theseus has no viable moves (his move list is empty). Return False.
    Recursive Case:
    5. Theseus has viable moves. Loop over the moves in the list.
       General structure: Have Theseus make a move. Then have the Minotaur make two based on his algorithm. Then
       return a recursive call to this function to determine whether Theseus can win.
    @param: board (2D array of Board_Square objects)  current board configuration
    @param: t_pos (ThesPos object)                    Theseus' current position
    @param: m_pos (MinoPos object)                    Minotaur's current position
    @param: hedges (Hedges object)                    config of hedges in maze
    @param: round_num (int)                           round the game is on; increments with each turn
    @return: boolean (True if Theseus can win, False otherwise)
    '''
    t_row, t_col = t_pos.get()
    m_row, m_col = m_pos.get()
    exit_x, exit_y = exit.get()
    # If Theseus has been eaten by the Minotaur
    if thes_eaten(t_pos, m_pos):
        E.add_constraint((t_pos & m_pos & hedges) >> ~t_pos)
        return False
    # If Theseus' position is the exit and the Minotaur is not there
    if thes_win(board, t_pos):
        E.add_constraint((t_pos & m_pos & hedges) >> t_pos)
        return True
    # Theseus has run out of turns
    if round_num >= NUM_ROUNDS:
        E.add_constraint((t_pos & m_pos & hedges) >> ~t_pos)
        return False
    else:
        # Get a list of Theseus' moves
        moves = ThesMoves.theseus_moves(board, t_pos, m_pos, hedges)
        # If the moves list is empty
        if not moves:
            E.add_constraint((t_pos & m_pos & hedges) >> ~t_pos)
            return False
        else:
            # We already validated the moves list so that no moves that get Theseus
            # eaten immediately are included, so if the exit square is in the moves list,
            # he wins
            if tuple([exit_x, exit_y]) in moves:
                E.add_constraint((t_pos & m_pos & hedges) >> t_pos)
                return True
            # Check each move in the moves list
            move = moves[0]
            while moves:
                # Have Theseus move once and the Minotaur move twice
                t_new_pos = ThesPos(move[0], move[1])
                t_pos.set(move[0], move[1])
                # Now have the Minotaur move
                m_turn1 = MinoMoves.mino_move(board, m_pos, t_pos, hedges)
                m_pos.set(m_turn1[0], m_turn1[1])
                m_turn2 = MinoMoves.mino_move(board, m_pos, t_pos, hedges)
                m_pos.set(m_turn2[0], m_turn2[1])
                # Set the board according to new positions and increment the round number by 1
                board = set_board(board, t_pos, m_pos)
                round_num += 1
                # If Theseus can eventually win, return True - no need to check anything else
                if is_winnable(board, t_pos, m_pos, exit, hedges, round_num):
                    E.add_constraint((t_pos & m_pos & hedges) >> t_pos)
                    return True
                # If Theseus can't win with this move, go on to the next move
                else:
                    round_num -= 1
                    # Reset Minotaur's and Theseus' position to where they were before
                    m_pos.set(m_row, m_col)
                    t_pos.set(t_row, t_col)
                    E.add_constraint((t_pos & m_pos & hedges) >> ~t_new_pos)
                    moves.remove(move)
                    if moves:
                        move = moves[0]


def example_theory_1():
    '''
    A full example theory for our model. Hedges and number of rounds are randomized,
    but starting Theseus and Minotaur and immutable Exit positions are not. As such,
    Theseus is expected to win most rounds, but the placement of hedges may prevent
    him from winning. To run this theory, uncomment NUM_ROUNDS = 3 on line 24.
    See game() for a truly randomized run.
    No args.
    '''
    # Some starting positions for everyone
    exit_x, exit_y = 3, 3
    t_x, t_y = 3, 2
    m_x, m_y = 0, 5
    exit = ExitSquare(exit_x, exit_y)
    t_start = ThesPos(t_x, t_y)
    constraint.add_exactly_one(E, t_start) # only one starting position for Theseus
    m_start = MinoPos(m_x, m_y)
    constraint.add_exactly_one(E, m_start) # only one starting position for Minotaur

    # Randomized hedges. NUM_ROUNDS is global and initialized elsewhere.
    hedges = Hedges()

    # Start the game
    board = start_board(t_x, t_y, m_x, m_y, exit_x, exit_y, hedges.vert, hedges.hor)

    # Print some visual representations of the board
    # Theseus and Minotaur positions
    t_and_m = []
    for i in range(BOARD_SIZE):
        row = ['*', '*', '*','*', '*', '*']
        t_and_m.append(row)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col].t_x and board[row][col].t_y:
                t_and_m[row][col] = "T"
            elif board[row][col].m_x and board[row][col].m_y:
                t_and_m[row][col] = "M"
            elif board[row][col].EXIT_x and board[row][col].EXIT_y:
                t_and_m[row][col] = "E"
    print("Starting board for example theory 1:")
    for row in t_and_m:
        print(row)
    print()

    # Vertical hedges
    v_h = []
    for i in range(BOARD_SIZE):
        row = ['*', '*', '*','*', '*', '*']
        v_h.append(row)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if hedges.vert[row][col]:
                v_h[row][col] = "T"
            else:
                v_h[row][col] = "F"
    print("Vertical hedges:")
    for row in v_h:
        print(row)
    print()

    # Horizontal hedges
    h_h = []
    for i in range(BOARD_SIZE):
        row = ['*', '*', '*','*', '*', '*']
        h_h.append(row)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if hedges.hor[row][col]:
                h_h[row][col] = "T"
            else:
                h_h[row][col] = "F"
    print("Horizontal hedges:")
    for row in h_h:
        print(row)
    print()

    # Number of rounds
    print("Number of rounds: ", NUM_ROUNDS)

    # Play the game
    turn_num = 0
    if is_winnable(board, t_start, m_start, exit, hedges, turn_num):
        print("Theseus escapes!")
    else:
        print("Theseus got eaten by the Minotaur :(")
    T = E.compile()
    print("Satisfiable: %s" % T.satisfiable())
    print()


def example_theory_2():
    '''
    A second full example theory for our model. Similar to first one, but here
    Theseus is expect to lose most runs except if he has fortunately-placed hedges.
    This will likely take longer to run than example_theory_1. To run this theory,
    uncomment NUM_ROUNDS = 8 on line 27.
    See game() for a truly randomized run.
    No args.
    '''
    # Some starting positions for everyone
    exit_x, exit_y = 3, 5
    t_x, t_y = 0, 2
    m_x, m_y = 5, 2
    exit = ExitSquare(exit_x, exit_y)
    t_start = ThesPos(t_x, t_y)
    constraint.add_exactly_one(E, t_start) # only one starting position for Theseus
    m_start = MinoPos(m_x, m_y)
    constraint.add_exactly_one(E, m_start) # only one starting position for Minotaur

    # Randomized hedges. NUM_ROUNDS is global and initialized elsewhere.
    hedges = Hedges()

    # Start the game
    board = start_board(t_x, t_y, m_x, m_y, exit_x, exit_y, hedges.vert, hedges.hor)

    # Print some visual representations of the board
    # Theseus and Minotaur positions
    t_and_m = []
    for i in range(BOARD_SIZE):
        row = ['*', '*', '*','*', '*', '*']
        t_and_m.append(row)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col].t_x and board[row][col].t_y:
                t_and_m[row][col] = "T"
            elif board[row][col].m_x and board[row][col].m_y:
                t_and_m[row][col] = "M"
            elif board[row][col].EXIT_x and board[row][col].EXIT_y:
                t_and_m[row][col] = "E"
    print("Starting board for example theory 2:")
    for row in t_and_m:
        print(row)
    print()

    # Vertical hedges
    v_h = []
    for i in range(BOARD_SIZE):
        row = ['*', '*', '*','*', '*', '*']
        v_h.append(row)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if hedges.vert[row][col]:
                v_h[row][col] = "T"
            else:
                v_h[row][col] = "F"
    print("Vertical hedges:")
    for row in v_h:
        print(row)
    print()

    # Horizontal hedges
    h_h = []
    for i in range(BOARD_SIZE):
        row = ['*', '*', '*','*', '*', '*']
        h_h.append(row)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if hedges.hor[row][col]:
                h_h[row][col] = "T"
            else:
                h_h[row][col] = "F"
    print("Horizontal hedges:")
    for row in h_h:
        print(row)
    print()

    # Number of rounds
    print("Number of rounds: ", NUM_ROUNDS)

    # Play the game
    turn_num = 0
    if is_winnable(board, t_start, m_start, exit, hedges, turn_num):
        print("Theseus escapes!")
    else:
        print("Theseus got eaten by the Minotaur :(")
    T = E.compile()
    print("Satisfiable: %s" % T.satisfiable())
    print()


def example_theory_3():
    '''
    Showcases an interesting configuration of the maze, with Theseus being farther
    from the exit than the Minotaur, but hedges preventing the Minotaur from making
    any effective moves. Originally derived from a run of example_theory_2.
    This requires at least eight moves to work - to ensure this runs properly,
    uncomment NUM_ROUNDS = 14 on line 30.
    No args.
    '''
    # Set starting positions, exit, and hedges
    e_x, e_y = 3, 5
    t_x, t_y = 0, 2
    m_x, m_y = 5, 2

    exit = ExitSquare(e_x, e_y)
    t_start = ThesPos(t_x, t_y)
    constraint.add_exactly_one(E, t_start)
    m_start = MinoPos(m_x, m_y)
    constraint.add_exactly_one(E, m_start)

    vert_h = [
             [False, False, True, False, False, False],
             [True, True, True, False, False, False],
             [True, False, False, False, True, True],
             [True, True, False, True, True, True],
             [True, False, False, False, False, True],
             [False, True, True, True, False, False]
             ]
    hor_h = [
            [True, False, False, False, False, False],
            [False, False, False, False, False, True],
            [False, False, False, False, False, False],
            [True, True, False, True, True, True],
            [True, True, False, True, False, False],
            [False, False, True, False, True, False]
            ]
    hedges = Hedges()
    hedges.vert = vert_h
    hedges.hor = hor_h
    
    # Start the board
    board = start_board(t_x, t_y, m_x, m_y, e_x, e_y, vert_h, hor_h)

    # Print some representations
    # Theseus and Minotaur positions
    t_and_m = []
    for i in range(BOARD_SIZE):
        row = ['*', '*', '*','*', '*', '*']
        t_and_m.append(row)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col].t_x and board[row][col].t_y:
                t_and_m[row][col] = "T"
            elif board[row][col].m_x and board[row][col].m_y:
                t_and_m[row][col] = "M"
            elif board[row][col].EXIT_x and board[row][col].EXIT_y:
                t_and_m[row][col] = "E"
    print("Starting board:")
    for row in t_and_m:
        print(row)
    print()

    # Vertical hedges
    vert_h_print = [
             ['F', 'F', 'T', 'F', 'F', 'F'],
             ['T', 'T', 'T', 'F', 'F', 'F'],
             ['T', 'F', 'F', 'F', 'T', 'T'],
             ['T', 'T', 'F', 'T', 'T', 'T'],
             ['T', 'F', 'F', 'F', 'F', 'T'],
             ['F', 'T', 'T', 'T', 'F', 'F']
             ]
    print("Vertical hedges:")
    for row in vert_h_print:
        print(row)
    print()

    # Horizontal hedges
    hor_h_print = [
            ['T', 'F', 'F', 'F', 'F', 'F'],
            ['F', 'F', 'F', 'F', 'F', 'T'],
            ['F', 'F', 'F', 'F', 'F', 'F'],
            ['T', 'T', 'F', 'T', 'T', 'T'],
            ['T', 'T', 'F', 'T', 'F', 'F'],
            ['F', 'F', 'T', 'F', 'T', 'F']
            ]
    print("Horizontal hedges:")
    for row in hor_h_print:
        print(row)
    print()

    # Number of rounds
    print("Number of rounds: ", NUM_ROUNDS)

    # Play the game
    turn_num = 0
    if is_winnable(board, t_start, m_start, exit, hedges, turn_num):
        print("Theseus escapes!")
    else:
        print("Theseus got eaten by the Minotaur :(")
    T = E.compile()
    print("Satisfiable: %s" % T.satisfiable())
    print()


def game():
    '''
    A truly randomized version of the game. All positions, hedges, and 
    number of rounds are randomized.
    No args.
    '''
    # Set starting positions and exit
    e_x, e_y = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)
    t_x, t_y = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)
    m_x, m_y = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)

    exit = ExitSquare(e_x, e_y)
    t_start = ThesPos(t_x, t_y)
    constraint.add_exactly_one(E, t_start)
    m_start = MinoPos(m_x, m_y)
    constraint.add_exactly_one(E, m_start)
    hedges = Hedges()

    # Initialize the board
    board = start_board(t_x, t_y, m_x, m_y, e_x, e_y, hedges.vert, hedges.hor)

    # Print some representations
    # Theseus and Minotaur positions
    t_and_m = []
    for i in range(BOARD_SIZE):
        row = ['*', '*', '*','*', '*', '*']
        t_and_m.append(row)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col].t_x and board[row][col].t_y:
                t_and_m[row][col] = "T"
            elif board[row][col].m_x and board[row][col].m_y:
                t_and_m[row][col] = "M"
            elif board[row][col].EXIT_x and board[row][col].EXIT_y:
                t_and_m[row][col] = "E"
    print("Starting board:")
    for row in t_and_m:
        print(row)
    print()

    # Vertical hedges
    v_h = []
    for i in range(BOARD_SIZE):
        row = ['*', '*', '*','*', '*', '*']
        v_h.append(row)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if hedges.vert[row][col]:
                v_h[row][col] = "T"
            else:
                v_h[row][col] = "F"
    print("Vertical hedges:")
    for row in v_h:
        print(row)
    print()

    # Horizontal hedges
    h_h = []
    for i in range(BOARD_SIZE):
        row = ['*', '*', '*','*', '*', '*']
        h_h.append(row)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if hedges.hor[row][col]:
                h_h[row][col] = "T"
            else:
                h_h[row][col] = "F"
    print("Horizontal hedges:")
    for row in h_h:
        print(row)
    print()

    # Number of rounds
    print("Number of rounds: ", NUM_ROUNDS)

    # Play the game
    turn_num = 0
    if is_winnable(board, t_start, m_start, exit, hedges, turn_num):
        print("Theseus escapes!")
    else:
        print("Theseus got eaten by the Minotaur :(")
    T = E.compile()
    print("Satisfiable: %s" % T.satisfiable())
    print()

# Only leave one of these uncommented at a time! Otherwise, you're adding
# the propositions and constraints for the next run of the program on top of
# the previous run. Do not leave more than one of the following uncommented
# at a time!
#example_theory_1()
#example_theory_2()
#example_theory_3()
game()

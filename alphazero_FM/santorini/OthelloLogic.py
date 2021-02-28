'''
Author: Eric P. Nichols
Date: Feb 8, 2008.
Board class.
Board data:
  1=white, -1=black, 0=empty
  first dim is column , 2nd is row:
     pieces[1][7] is the square in column 2,
     at the opposite end of the board in row 8.
Squares are stored and manipulated as (x,y) tuples.
x is the column, y is the row.
'''
class Board():

    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

    # SANTORINI: Done
    def __init__(self, n):
        "Set up initial board configuration."

        self.n = n
        # Create the empty board array.
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [0]*self.n

        # Set up the initial 2 pieces.
        #TODO: ADD TWO PLAYERS
        self.pieces[self.n-1][self.n-1] = 1
        self.pieces[0][0] = -1

    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

    def countDiff(self, color):
        """Counts the # pieces of the given color
        (1 for white, -1 for black, 0 for empty spaces)"""
        count = 0
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y]==color:
                    count += 1
                if self[x][y]==-color:
                    count -= 1
        return count

    # SANTORINI: In Progress
    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black)
        """
        moves = set()  # stores the legal moves.

        # Get all the squares with pieces of the given color.
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y]==color:
                    newmoves = self.get_moves_for_square((x,y))
                    moves.update(newmoves)
                    break
        return list(moves)

    def has_legal_moves(self, color):
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y]==color:
                    newmoves = self.get_moves_for_square((x,y))
                    if len(newmoves)>0:
                        return True
        return False

    def is_legal_move(self, x_sum, y_sum, color):
        # boundaries
        if not (x_sum >= self.n or y_sum >= self.n or x_sum < 0 or y_sum < 0) and \
                (self[x_sum][y_sum] != -color):
            return True
        return False

    def remove_color(self, color):
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y]==color:
                    self[x][y] = 0

    # SANTORINI: In Progress
    def get_moves_for_square(self, square):
        """
        """
        # search all possible directions.
        moves = []
        for direction in self.__directions:
            move = self._discover_move(square, direction)
            if move:
                moves.append(move)

        # return the generated move list
        return moves

    def execute_move(self, move, color):
        x_orig, y_orig = move

        self.remove_color(color)
        self[x_orig][y_orig] = color

    # SANTORINI: In Progress
    def _discover_move(self, origin, direction):
        """ Returns the endpoint for a legal move, starting at the given origin,
        moving by the given increment."""

        x_orig, y_orig = origin
        x_dir, y_dir = direction

        x_sum = x_orig + x_dir
        y_sum = y_orig + y_dir

        color = self[x_orig][y_orig]

        if self.is_legal_move(x_sum, y_sum, color):
            return (x_sum, y_sum)

        return None



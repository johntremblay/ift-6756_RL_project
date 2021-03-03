'''
Author: Francois Milot
Date: March 1, 2021.
Board class.
Board data:
  1=white, -1=black, 0=empty
  first dim is column , 2nd is row:
     pieces[1][7] is the square in column 2,
     at the opposite end of the board in row 8.
Squares are stored and manipulated as (x,y) tuples.
x is the column, y is the row.
'''

from math import copysign

class Board():

    # list of all 8 directions on the board, as (x,y) offsets
    __directions_move = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]
    __directions_build = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

    # SANTORINI: Done
    def __init__(self, n):
        "Set up initial board configuration."

        self.n = n
        # Create the empty board array.
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [0]*self.n

        # Set up the initial 2 pieces.
        #TODO: ADD TWO OTHER PLAYERS
        self.pieces[self.n-1][self.n-1] = 1
        self.pieces[0][0] = -1

    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

    # SANTORINI: Done
    def get_legal_moves_builds(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black)
        """
        new_moves_builds = set()

        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] in [i * color for i in [1, 11, 21]]:
                    new_moves_builds.update(self.get_moves_for_square((x,y)))
        return list(new_moves_builds)

    # SANTORINI: Done
    def has_legal_moves_builds(self, color):
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] in [i * color for i in [1, 11, 21]]:
                    newmoves = self.get_moves_for_square((x,y))
                    if len(newmoves)>0:
                        return True
        return False

    # SANTORINI: Done
    def get_moves_for_square(self, square):
        """
        """
        # search all possible directions.
        moves_builds = []
        for direction_move in self.__directions_move:
            move = self._discover_move(square, direction_move)

            if move is not None:
                for direction_build in self.__directions_build:
                    build = self._discover_build(move, direction_build)
                    if build is not None:
                        move_build = (move, build)
                        moves_builds.append(move_build)

        return moves_builds

    # SANTORINI: Done
    def execute_move_build(self, move, build, color):
        # Move
        x_move, y_move = move
        self._remove_color(color)
        self[x_move][y_move] = color*(self[x_move][y_move]+1)

        # Build
        x_build, y_build = build
        self[x_build][y_build] += 10

    # SANTORINI: Done
    def _remove_color(self, color):
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] in [i * color for i in [1, 11, 21]]:
                    self[x][y] = (self[x][y] - color) * color

    # SANTORINI: Done
    def _discover_move(self, origin, direction):
        """ Returns the endpoint for a legal move, starting at the given origin,
        moving by the given increment."""

        x_orig, y_orig = origin
        x_dir, y_dir = direction

        color = int(copysign(1, self[x_orig][y_orig]))

        if self._is_legal_move(origin, direction, color):
            return (x_orig + x_dir, y_orig + y_dir)

        return None

    # SANTORINI: Done
    def _is_legal_move(self, origin, direction, color):
        x_orig, y_orig = origin
        x_dir, y_dir = direction

        x_sum = x_orig + x_dir
        y_sum = y_orig + y_dir

        if not (x_sum >= self.n or y_sum >= self.n or x_sum < 0 or y_sum < 0): # boundaries of board
            if (self[x_sum][y_sum] not in [i * (-color) for i in [1, 11, 21]]) and (self[x_sum][y_sum] not in [40, -40]): # players present or capped building
                if self[x_sum][y_sum] * color - (self[x_orig][y_orig] - color) <= 10: # players can drop building but not increase by more than one
                    return True
        return False

    # SANTORINI: Done
    def _discover_build(self, origin, direction):
        """ Returns the endpoint for a legal move, starting at the given origin,
        moving by the given increment."""

        x_orig, y_orig = origin
        x_dir, y_dir = direction

        x_sum = x_orig + x_dir
        y_sum = y_orig + y_dir

        if self._is_legal_build(x_sum, y_sum):
            return (x_sum, y_sum)

        return None

    # SANTORINI: Done
    def _is_legal_build(self, x_sum, y_sum):
        if (not (x_sum >= self.n or y_sum >= self.n or x_sum < 0 or y_sum < 0)):
            if (self[x_sum][y_sum] not in [1, -1, 11, -11, 21, -21, 40, -40]):
                # print(self[x_sum][y_sum])
                return True
        return False


    #TO DELETE
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
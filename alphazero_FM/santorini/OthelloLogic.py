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

        # Get all the squares with pieces of the given color.
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] in [i * color for i in [1, 11, 21, 31]]:
                    new_moves_builds = self.get_moves_for_square((x,y))
                    break
        return new_moves_builds

    # SANTORINI: Done
    def has_legal_moves_builds(self, color):
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] in [i * color for i in [1, 11, 21, 31]]:
                    new_moves_builds = self.get_moves_for_square((x,y))
                    if len(new_moves_builds)>0:
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

            if move:
                for direction_build in self.__directions_build:
                    build = self._discover_build(move, direction_build)
                    if build:
                        move_build = (move, build)
                        moves_builds.append(move_build)
        # return the generated move list
        return moves_builds

    # SANTORINI: Done
    def is_legal_move(self, x_sum, y_sum, color):
        if not (x_sum >= self.n or y_sum >= self.n or x_sum < 0 or y_sum < 0) and \
                (self[x_sum][y_sum] not in [i * (-color) for i in [1, 11, 21, 31]]):
            return True
        return False

    # SANTORINI: Done
    def is_legal_build(self, x_sum, y_sum, color):
        if not (x_sum >= self.n or y_sum >= self.n or x_sum < 0 or y_sum < 0) and \
                (self[x_sum][y_sum] not in [1, -1, 11, -11, 21, -21, 31, -31, 30, -30]):
            return True
        return False

    # SANTORINI: Done
    def execute_move(self, move, color):
        # Move
        x_orig, y_orig = move
        self.remove_color(color)
        self[x_orig][y_orig] = color*(self[x_orig][y_orig]+1)

    # SANTORINI: Done
    def execute_build(self, build):
        x_orig, y_orig = build
        self[x_orig][y_orig] += 10

    # SANTORINI: Done
    def remove_color(self, color):
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] in [i * color for i in [1, 11, 21, 31]]:
                    self[x][y] = (self[x][y] - color) * color

    # SANTORINI: Done
    def _discover_move(self, origin, direction):
        """ Returns the endpoint for a legal move, starting at the given origin,
        moving by the given increment."""

        x_orig, y_orig = origin
        x_dir, y_dir = direction

        x_sum = x_orig + x_dir
        y_sum = y_orig + y_dir

        color = int(copysign(1, self[x_orig][y_orig]))

        if self.is_legal_move(x_sum, y_sum, color):
            return (x_sum, y_sum)

        return None

    # SANTORINI: Done
    def _discover_build(self, origin, direction):
        """ Returns the endpoint for a legal move, starting at the given origin,
        moving by the given increment."""

        x_orig, y_orig = origin
        x_dir, y_dir = direction

        x_sum = x_orig + x_dir
        y_sum = y_orig + y_dir

        color = int(copysign(1, self[x_orig][y_orig]))

        if self.is_legal_build(x_sum, y_sum, color):
            return (x_sum, y_sum)

        return None

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
from __future__ import print_function
import sys

sys.path.append('..')
from Game import Game
from .SantoriniLogic import Board
import numpy as np


class SantoriniGame(Game):
    # SANTORINI: Done
    square_content = {
        -31: "3-X",
        -21: "2-X",
        -11: "1-X",
        -1: "0-X",
        +40: "CAP",
        +30: "3--",
        +20: "2--",
        +10: "1--",
        +0: "0--",
        +31: "3-O",
        +21: "2-O",
        +11: "1-O",
        +1: "0-O"
    }

    # SANTORINI: Done
    @staticmethod
    def getSquarePiece(piece):
        return SantoriniGame.square_content[piece]

    # SANTORINI: Done
    def __init__(self, n):
        super().__init__()
        self.n = n

    # SANTORINI: Done
    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces)

    # SANTORINI: Done
    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    # SANTORINI: Done
    def getActionSize(self):
        # return number of actions
        return self.n ** 4

    # SANTORINI: Done
    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        b = Board(self.n)
        b.pieces = np.copy(board)

        move = (int(action / self.n ** 3), int((action / self.n ** 2) % self.n))
        build = (int((action / self.n) % self.n), int(action % self.n))
        b.execute_move_build(move, build, player)

        return (b.pieces, -player)

    # SANTORINI: Done
    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0] * self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves = b.get_legal_moves_builds(player)

        if len(legalMoves) == 0:
            return np.array(valids)

        for move, build in legalMoves:
            x_move, y_move = move
            x_build, y_build = build
            valids[(self.n ** 3) * x_move + (self.n ** 2) * y_move + (self.n) * x_build + y_build] = 1

        return np.array(valids)

    # SANTORINI: Done
    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.pieces = np.copy(board)
        if not (b.has_legal_moves_builds(player)):
            return -1
        if not (b.has_legal_moves_builds(-player)):
            return 1
        for i in range(self.n):
            for j in range(self.n):
                if b.pieces[i][j] == 31:
                    return 1
                elif b.pieces[i][j] == -31:
                    return -1
        return 0

    # SANTORINI: Done
    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player * board

    # TODO: Major work here
    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert (len(pi) == self.n ** 4)  # 1 for pass
        return [(board, pi)]
        # pi_board = np.reshape(pi[:-1], (self.n, self.n))
        # l = []
        #
        # for i in range(1, 5):
        #     for j in [True, False]:
        #         newB = np.rot90(board, i)
        #         newPi = np.rot90(pi_board, i)
        #         if j:
        #             newB = np.fliplr(newB)
        #             newPi = np.fliplr(newPi)
        #         l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        # return l

    # SANTORINI: Done
    def stringRepresentation(self, board):
        return board.tostring()

    # SANTORINI: Done
    def stringRepresentationReadable(self, board):
        board_s = "".join(self.square_content[square] for row in board for square in row)
        return board_s

    # SANTORINI: Done
    @staticmethod
    def display(board):
        n = board.shape[0]
        print("    ", end="")
        for y in range(n):
            print(y, end="   ")
        print("")
        print("------------------------")
        for y in range(n):
            print(y, "|", end="")  # print the row #
            for x in range(n):
                piece = board[y][x]  # get the piece to print
                print(SantoriniGame.square_content[piece], end=" ")
            print("|")

        print("------------------------")


# TODO: Move the below, since cannot be called and only a workaround of
# TODO: not a good canonicalboard representation
def getNNForm(board):
    assert isinstance(board, np.ndarray), 'Only accepts numpy array representation'
    board_level_map = {key: idx for idx, key in enumerate(SantoriniGame.square_content.keys())}
    nn_board = np.zeros((len(SantoriniGame.square_content), board.shape[0], board.shape[1]))
    for row in range(board.shape[0]):
        for col in range(board.shape[1]):
            square = board[row][col]
            board_i = board_level_map[square]
            nn_board[board_i, row, col] = 1.0
    return nn_board
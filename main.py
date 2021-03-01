import sys
import threading

from Coach import Coach
from chessaz.ChessGame import ChessGame as Game
from chessaz.pytorch.NNet import NNetWrapper as nn
from utils import *


args = dotdict({
    'numIters': 5,
    'numEps': 2,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        #
    'updateThreshold': 0.5,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 2,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 2,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,

    'checkpoint': '/home/john/PycharmProjects/ift-6756_RL_project/training/',
    'load_model': True,
    'load_folder_file': ('/home/john/PycharmProjects/ift-6756_RL_project/checkpoint/', 'checkpoint.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})

if __name__ == "__main__":
    my_game = Game()
    nnet = nn(my_game)

    if args.load_model:
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

    c = Coach(my_game, nnet, args)
    if args.load_model:
        print("Load trainExamples from file")
        c.loadTrainExamples()
    sys.setrecursionlimit(100000)
    # threading.stack_size(200000000)
    # thread = threading.Thread(target=c.learn())
    # thread.start()
    c.learn()

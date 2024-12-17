# play_game.py
#
# For testing the game. Run this module as main if you want to pit two algorithms 
# against one another.
from game import Match
from stratagem import *

NAME_TO_ALG = {
    "g": Greedy,
    "greed": Greedy,
    "greedy": Greedy,
    "safe": Safe,
    "b": Balanced,
    "balanced": Balanced,
    "rand": Random,
    "random": Random,
    "risky": Risky,
    "scared": Scared
}

if __name__ == '__main__':
    alg1: Stratagem = None
    alg2: Stratagem = None

    print('Input algorithms to use for each player:')
    while alg1 == None or alg2 == None:
        print('Player 1: ', end='')
        input1: str = input('').strip().lower()
        print('Player 2: ', end='')
        input2: str = input('').strip().lower()

        alg1 = NAME_TO_ALG.get(input1)
        alg2 = NAME_TO_ALG.get(input2)

    new_match: Match = Match(4, 4, 3, alg1(), alg2())

    new_match.play(True, True)
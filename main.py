'''Main application'''
import argparse
from animals import Sheep, Wolf
from argument_parser import IntRange
from info_functions import display_info, save_to_json, save_to_csv


parser = argparse.ArgumentParser()

parser.add_argument('-r', '--rounds', help='numer of rounds', metavar='NUM',
                    type=IntRange(1), default=20)
parser.add_argument('-s', '--sheep', help='numer of sheep in flock', metavar='NUM',
                    type=IntRange(1), default=15)
parser.add_argument('-w', '--wait', help='wait for input after every round', action='store_true')

args = parser.parse_args()

WAIT = args.wait
MAX_ROUND_NUMBER = args.rounds
SHEEP_FLOCK_SIZE = args.sheep
INIT_POS_LIMIT = 10.0
SHEEP_MOVE_DIST = 0.5
WOLF_MOVE_DIST = 1.0


def start_simulation():
    '''Main function'''
    flock = [Sheep(INIT_POS_LIMIT, SHEEP_MOVE_DIST) for i in range(SHEEP_FLOCK_SIZE)]
    wolf = Wolf(WOLF_MOVE_DIST)
    for round_number in range(MAX_ROUND_NUMBER):
        alive_sheep = [sheep for sheep in flock if sheep.alive]
        if len(alive_sheep) > 0:
            for sheep in alive_sheep:
                sheep.run()
            wolf.chase(alive_sheep)

            display_info(flock, wolf, round_number)
            save_to_json(flock, wolf, round_number)
            save_to_csv(flock, round_number)

            if WAIT:
                input()
        else:
            print("All the sheep were eaten")
            return


if __name__ == '__main__':
    start_simulation()
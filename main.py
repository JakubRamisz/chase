'''Main application'''
import argparse
import configparser
from animals import Sheep, Wolf
from argument_parser import IntRange
from info_functions import display_info, save_to_json, save_to_csv


parser = argparse.ArgumentParser()

parser.add_argument('-c', '--config', help='auxiliary configuration file', metavar='FILE',
                    default='config.cnf')
parser.add_argument('-d', '--dir', help='subdirectory where report files will be placed',
                    default='.')
parser.add_argument('-r', '--rounds', help='numer of rounds', metavar='NUM',
                    type=IntRange(1), default=20)
parser.add_argument('-s', '--sheep', help='numer of sheep in flock', metavar='NUM',
                    type=IntRange(1), default=15)
parser.add_argument('-w', '--wait', help='wait for input after every round', action='store_true')

args = parser.parse_args()

config = configparser.ConfigParser()
if config.read(args.config) is None:
    raise argparse.ArgumentTypeError(f'{args.config} is not a config file')

config.read(args.config)
WAIT = args.wait
MAX_ROUND_NUMBER = args.rounds
SHEEP_FLOCK_SIZE = args.sheep
INIT_POS_LIMIT = config.getfloat('Terrain', 'InitPosLimit', fallback=10)
SHEEP_MOVE_DIST = config.getfloat('Movement', 'SheepMoveDist', fallback=0.5)
WOLF_MOVE_DIST = config.getfloat('Movement', 'WolfMoveDist', fallback=1)


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
            save_to_json(flock, wolf, round_number, args.dir)
            save_to_csv(flock, round_number, args.dir)

            if WAIT:
                input()
        else:
            print("All the sheep were eaten")
            return


if __name__ == '__main__':
    start_simulation()

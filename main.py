'''Main application'''
import argparse
import configparser
import logging
from os import path
from animals import Sheep, Wolf
from argument_parser import IntRange
from info_functions import display_info, save_to_json, save_to_csv


parser = argparse.ArgumentParser()

parser.add_argument('-c', '--config', help='auxiliary configuration file', metavar='FILE',
                    default='config.cnf')
parser.add_argument('-d', '--dir', help='subdirectory where report files will be placed',
                    default='.')
parser.add_argument('-l', '--log', help='logging level', metavar='LEVEL',
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
parser.add_argument('-r', '--rounds', help='numer of rounds', metavar='NUM',
                    type=IntRange(1), default=20)
parser.add_argument('-s', '--sheep', help='numer of sheep in flock', metavar='NUM',
                    type=IntRange(1), default=15)
parser.add_argument('-w', '--wait', help='wait for input after every round', action='store_true')

args = parser.parse_args()

logging.basicConfig(filename='chase.log', level=args.log,
                    format='[%(levelname)s] %(asctime)s - %(message)s')

config = configparser.ConfigParser()
if not path.exists(args.config):
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
    logging.debug('start_simulation() call')
    logging.info('start of simulation')

    logging.info('setting initial positions of sheep')
    flock = [Sheep(INIT_POS_LIMIT, SHEEP_MOVE_DIST) for i in range(SHEEP_FLOCK_SIZE)]
    logging.info('setting initial positions of the wolf')
    wolf = Wolf(WOLF_MOVE_DIST)
    for round_number in range(MAX_ROUND_NUMBER):
        alive_sheep = [sheep for sheep in flock if sheep.alive]
        if len(alive_sheep) > 0:
            for sheep in alive_sheep:
                logging.info('a sheep moves')
                sheep.run()
            logging.info('the wolf moves')
            wolf.chase(alive_sheep)

            logging.info('displaying round information')
            display_info(flock, wolf, round_number)
            logging.info('saving round information')
            save_to_json(flock, wolf, round_number, args.dir)
            save_to_csv(flock, round_number, args.dir)

            if WAIT:
                logging.info('waiting for input')
                input()
        else:
            print("All the sheep were eaten")
            logging.info('end of simulation')
            return

    logging.info('end of simulation')


if __name__ == '__main__':
    start_simulation()

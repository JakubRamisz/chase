import csv
import json
import logging
from os import remove, mkdir, path


def display_info(flock, wolf, round_number):
    '''Prints information about current state of simulation'''
    logging.debug('display_info() call ')
    formatted_wolf_pos = [ round(coordinate, 3) for coordinate in wolf.pos ]
    if wolf.prey:
        chased_sheep_info = f'The wolf is currently chasing sheep {flock.index(wolf.prey) + 1}\n'
    else:
        chased_sheep_info = 'The wolf is not chasing any sheep\n'

    if wolf.killed_this_round:
        killed_sheep_info = f'Sheep {flock.index(wolf.killed_this_round) + 1} was eaten\n'
    else:
        killed_sheep_info = ''


    print(f'Round: {round_number + 1}\nWolf position: {formatted_wolf_pos}\n'
            + chased_sheep_info + killed_sheep_info
            + f'{len([sheep for sheep in flock if sheep.alive])} sheep left alive\n')


def save_to_json(array, directory):
    '''Saves information about animal positions to pos.json file'''
    logging.debug('save_to_json() call')
    if not path.exists(directory):
        mkdir(directory)

    file_path = f'{directory}/pos.json'
    if path.exists(file_path):
        remove(file_path)

    with open(file_path, 'a', encoding='UTF-8') as json_file:
        json_file.write(json.dumps(array, indent=4))


def save_to_csv(flock, round_number, directory):
    '''Saves information about alive sheep to alive.csv file'''
    logging.debug('save_to_csv() call')
    if not path.exists(directory):
        mkdir(directory)

    file_path = f'{directory}/alive.csv'
    if (round_number == 0) and (path.exists(file_path)):
        remove(file_path)

    with open (file_path, 'a' , encoding='UTF-8') as csv_file:
        writer = csv.writer(csv_file)
        if round_number == 0:
            writer.writerow(('round number', 'sheep alive'))

        writer.writerow((round_number + 1, len([sheep for sheep in flock if sheep.alive])))

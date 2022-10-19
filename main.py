'''Main application'''
from animals import Sheep, Wolf
from info_functions import display_info, save_to_json, save_to_csv


MAX_ROUND_NUMBER = 20
SHEEP_FLOCK_SIZE = 15
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
        else:
            print("All the sheep were eaten")


if __name__ == '__main__':
    start_simulation()

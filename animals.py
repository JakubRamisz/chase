'''Model classes'''
from abc import ABC, abstractmethod
import random


class Animal(ABC):
    '''
    Abstract class representing simulated animals

    Args:
        move_dist (float): distance by which the animal can move

    Attributes:
        move_dist (float): used to store move_dist arg
        pos (list): represents position of the Animal on cartesian plane
    '''
    @abstractmethod
    def __init__(self, move_dist: float):
        self.move_dist = move_dist
        self.pos = None


    def move(self, vector: list):
        '''Move pos by a vector '''
        self.pos[0] += vector[0]
        self.pos[1] += vector[1]


class Sheep(Animal):
    '''
    Class representing simulated sheep

    Args:
        init_pos_limit (float): bounds for initial position
        move_dist (float): distance by which the sheep moves

    Attributes:
        move_dist (float): used to store move_dist arg
        pos (list): represents position of the Sheep on cartesian plane
        alive (boolean): used to determinate wether or not the sheep has been eaten
    '''
    def __init__(self, init_pos_limit: float, move_dist: float):
        super().__init__(move_dist)
        self.pos = [random.randrange(-init_pos_limit, init_pos_limit),
                    random.randrange(-init_pos_limit, init_pos_limit)]
        self.alive = True

    def run(self):
        '''
        Randomly chooses a cardinal direction and moves the Sheep by its
        move_dist in that direction
        '''
        direction_selector = [lambda pos: self.move((self.move_dist, 0)),
                            lambda pos: self.move((-self.move_dist, 0)),
                            lambda pos: self.move((0, self.move_dist)),
                            lambda pos: self.move((0, -self.move_dist))]

        random.choice(direction_selector)(self.pos)

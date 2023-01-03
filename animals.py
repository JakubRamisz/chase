'''Model classes'''
from abc import ABC, abstractmethod
from math import sqrt
import random
import logging


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
        logging.debug('Animal constructor call')
        self.move_dist = move_dist
        self.pos = None


    def move(self, vector: list):
        '''Move pos by a vector '''
        logging.debug('Animal.move() call')
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
        logging.debug('Sheep constructor call')
        super().__init__(move_dist)
        self.pos = [random.randrange(-init_pos_limit, init_pos_limit),
                    random.randrange(-init_pos_limit, init_pos_limit)]
        self.alive = True

    def run(self):
        '''
        Randomly chooses a cardinal direction and moves the Sheep by its
        move_dist in that direction
        '''
        logging.debug('Sheep.run() call')
        direction_selector = [lambda pos: self.move((self.move_dist, 0)),
                            lambda pos: self.move((-self.move_dist, 0)),
                            lambda pos: self.move((0, self.move_dist)),
                            lambda pos: self.move((0, -self.move_dist))]

        random.choice(direction_selector)(self.pos)


class Wolf(Animal):
    '''
    Class representing simulated wolf

    Args:
        move_dist (float): maximum distance by which the wolf can move

    Attributes:
        move_dist (float): used to store move_dist arg
        pos (list): represents position of the Wolf on cartesian plane
        prey (Sheep): Sheep the wolf is currently chasing
        killed_this_round (Sheep): The Sheep which was killed by the Wolf in last iteration
    '''
    def __init__(self, move_dist):
        logging.debug('Wolf constructor call')
        super().__init__(move_dist)
        self.pos = [0, 0]
        self.prey = None
        self.killed_this_round = None

    def chase(self, flock: list):
        '''
        Finds the closes Sheep in given flock of Sheep,
        moves the Wolf towards it by up to its move_dist,
        if a Sheep is within its move_dist, sets the Sheeps alive variable to False.
        '''
        logging.debug('Wolf.chase() call')
        self.prey = flock[0]
        for sheep in flock:
            if calculate_distance(self, sheep) < calculate_distance(self, self.prey):
                self.prey = sheep

        distance = calculate_distance(self, self.prey)
        vector = calculate_vector(self, self.prey)
        if distance <= self.move_dist:
            self.move(vector)
            self.prey.alive = False
            self.prey.pos = None
            self.killed_this_round = self.prey
            self.prey = None
        else:
            self.killed_this_round = None
            vector[0] = vector[0]/distance
            vector[1] = vector[1]/distance

            vector[0] = vector[0] * self.move_dist
            vector[1] = vector[1] * self.move_dist
            self.move(vector)


def calculate_distance(animal_a: Animal , animal_b: Animal):
    '''Returns distance between animal_a and animal_b'''
    logging.debug('calculate_distance() call')
    vector = calculate_vector(animal_a, animal_b)
    logging.debug('calculate_distance() return %r', vector)
    return sqrt(vector[0]**2 + vector[1]**2)


def calculate_vector(animal_a: Animal , animal_b: Animal):
    '''Returns a list representing a vector from animal_a to animal_b'''
    logging.debug('calculate_vector() call')
    vector = [animal_b.pos[0] - animal_a.pos[0], animal_b.pos[1] - animal_a.pos[1]]
    logging.debug('calculate_vector() return %r', vector)
    return vector

'''Model classes'''
from abc import ABC, abstractmethod


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

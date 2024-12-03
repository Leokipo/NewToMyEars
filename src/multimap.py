"""
Implementation of a multimap utilizing an array of sets.
Each index of the array equates to a popularity index (0-100) and the set contains songs with that popularity index
"""

import random

class multimap:
    def __init__(self):
        self.map = [set() for _ in range(101)] # populate the map array with a set for each index

    def insert(self, index, songName):
        # insert a new song to the set at the corresponding popularity index
        self.map[index].add(songName)

    def getSong(self, index):
        # get a random song from the given popularity index
        # O(n) time complexity because of conversion to list (random access)
        targetSet = self.map[index]
        return random.choice(list(targetSet))
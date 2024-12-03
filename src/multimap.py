"""
Implementation of a multimap utilizing an array of sets.
Each index of the array equates to a popularity index (0-100) and the set contains songs with that popularity index
"""
class multimap:
    def __init__(self):
        self.map = [{} for _ in range(100)] #populate the map array with a set for each index
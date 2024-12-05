"""
Implementation of a multimap utilizing an array of sets.
Each index of the array equates to a popularity index (0-100) and the set contains songs with that popularity index
"""

import random

class multimap:
    def __init__(self):
        self.map = [set() for _ in range(101)] # populate the map array with a set for each index

    def insert(self, index, songID):
        # insert a new song to the set at the corresponding popularity index
        self.map[index].add(songID)

    def getSong(self, index):
        # get a random song from the given popularity index
        # O(n) time complexity because of conversion to list (random access)
        target_set = self.map[index]
        if not bool(target_set):    # set is empty, return false and get a new popularity index
            return False
        song_id = random.choice(list(target_set))
        target_set.remove(song_id)
        return song_id

    def createPlaylist(self):
        """
        Generate random integers within ranges of 10: 0-10, 10-20, 20-30, 30-40, and 40-50
        Use those scores to get songs from the multimap
        If the score is not found, loop again
        Get two songs from each range of scores (10 total songs)
        """
        song_ids = []
        for j in range(4):
            for i in range(5):
                song_id = False
                while not song_id:
                    random_score = (i * 10) + random.randint(0, 10)
                    song_id = self.getSong(random_score)
                song_ids.append(song_id)
        return song_ids
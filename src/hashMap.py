# implementation of map data structure utilizing a hash map
class hashMap:
    def __init__(self, bucketCount, loadFactor):
        self.bucketCount = bucketCount
        self.loadFactor = loadFactor
        '''
        create an array of bucketCount buckets to store values
        each bucket is its own array for collision resolution (separate chaining)
        '''
        self.hashTable = [[] for _ in range(bucketCount)]

    def hash(self, key, value):
        # calculate hash key
        hashKey = key % self.bucketCount
        # append new value to the corresponding bucket
        self.hashTable[hashKey].append(value)
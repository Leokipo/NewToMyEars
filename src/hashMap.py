#implementation of map data structure utilizing a hash map
class hashMap:
    def __init__(self, bucketCount, loadFactor):
        self.bucketCount = bucketCount
        self.loadFactor = loadFactor

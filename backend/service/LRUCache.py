from collections import deque


class LRUCache:
    """
    Cache to store records.
    """

    def __init__(self, capacity):
        self.cache = dict()
        self.capacity = capacity
        self.access = deque()

    def get(self, key):
        if key not in self.cache:
            return -1
        else:
            self.access.remove(key)
            self.access.append(key)
            return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.access.remove(key)
        elif len(self.cache) == self.capacity:
            oldest = self.access.popleft()
            del self.cache[oldest]
        self.cache[key] = value
        self.access.append(key)

    def get_size(self):
        return len(self.access)

    def is_empty(self):
        return len(self.access) == 0

    def print(self):
        for key in self.access:
            print(f"{key}: {self.cache[key]}")

    def peek_all(self):
        return list(self.cache.values())
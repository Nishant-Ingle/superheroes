class Cache:
    """
    Cache to store records in-memory.
    """
    def __init__(self):
        self.cache = dict()

    def get(self, key):
        if key not in self.cache:
            return -1
        else:
            return self.cache[key]

    def put(self, key, value):
        self.cache[key] = value

    def get_size(self):
        return len(self.cache)

    def is_empty(self):
        return len(self.cache) == 0

    def print(self):
        for key, value in self.cache.items():
            print(f"{key}: {value}")

    def peek_all(self):
        return list(self.cache.values())

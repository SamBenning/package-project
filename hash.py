class HashMap:
    def __init__(self, size):
        self.size = size
        self.map = [None] * size

    def _get_hash(self, key):
        key_sum = 0
        for i in str(key):
            key_sum += ord(i)
        return key_sum % self.size

    def add(self, key, value):
        hash_val = self._get_hash(key)

        if not self.map[hash_val]:
            self.map[hash_val] = [[key, value]]
            return True
        else:
            # This for loop handles updating the value if the key is already in the hashmap.
            for i in self.map[hash_val]:
                if i[0] == key:
                    i[1] = value
                    return True
            self.map[hash_val].append([key, value])
            return True

    def get(self, key):
        hash_val = self._get_hash(key)

        if self.map[hash_val] is not None:
            for i in self.map[hash_val]:
                if i[0] == key:
                    return i[1]
        return None

    def get_map(self):
        elements = []
        for i in self.map:
            if i:
                elements.append(i)
        return elements

    def get_size(self):
        return len(self.map)


    def delete(self, key):
        hash_val = self._get_hash(key)
        if self.map[hash_val] is None:
            return False
        for i, j in enumerate(self.map[hash_val]):
            if j[0] == key:
                self.map[hash_val].pop(i)
                return True

    def print(self):
        print('-------ITEMS--------')
        for i in self.map:
            if i:
                print(str(i))
class HashTable:
    def __init__(self, size):
        self.size = size
        self.map = [None] * size

    # Simple hash function. Generates a hash value that will be used to map elements to a cell in the table.
    def _get_hash(self, key):
        key_sum = 0
        for i in str(key):
            key_sum += ord(i)
        return key_sum % self.size

    # Adds the passed in key, value pair to the hash table. If the key is already in the table, the value is updated
    # with the new value passed in.
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

    # If a key is in the table, this will return the value associated with that key. Otherwise, returns None.
    def get(self, key):
        hash_val = self._get_hash(key)

        if self.map[hash_val] is not None:
            for i in self.map[hash_val]:
                if i[0] == key:
                    return i[1]
        return None

    # Returns a list of all the elements contained in the hash table.
    def get_map(self):
        elements = []
        for i in self.map:
            if i:
                elements.append(i)
        return elements

    # Returns and integer of the size of the hash table.
    def get_size(self):
        return len(self.map)

    # Removes an element from the hash table based on passed in key. Returns true if element was deleted, false if not.
    def delete(self, key):
        hash_val = self._get_hash(key)
        if self.map[hash_val] is None:
            return False
        for i, j in enumerate(self.map[hash_val]):
            if j[0] == key:
                self.map[hash_val].pop(i)
                return True

    # Prints all non-None cells in the hash table.
    def print(self):
        print('-------ITEMS--------')
        for i in self.map:
            if i:
                print(str(i))
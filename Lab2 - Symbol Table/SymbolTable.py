class SymbolTable:
    def __init__(self, capacity=13):
        self._capacity = capacity
        self._elems = [[] for _ in range(self._capacity)]
        self._currentLength = 0

    def hash(self, key):
        """
        Hash function: sum(ascii values of key characters)%capacity
        :param key:
        :return:
        """

        if not isinstance(key, str):
            key = str(key)
        ascii_sum = 0
        for char in key:
            ascii_sum += hash(char)
        return ascii_sum % self._capacity

    def add(self, key):
        if self.exists(key):
            return self.getPos(key)
        else:
            self._elems[self.hash(key)].append(key)
            self._currentLength += 1
            return self.getPos(key)

    def exists(self, key):
        """
        Checks if a key already exists in a hash table
        :param key:
        :return:
        """
        bucket_index = self.hash(key)
        for i in range(len(self._elems)):
            if bucket_index == i:
                for j in range(len(self._elems[bucket_index])):
                    if self._elems[bucket_index][j] == key:
                        return True
        return False

    def getPos(self, key):
        bucket_index = self.hash(key)
        for i in range(len(self._elems)):
            if bucket_index == i:
                for j in range(len(self._elems[bucket_index])):
                    if self._elems[bucket_index][j] == key:
                        return bucket_index, j
        return -1, -1

    def __str__(self):
        string = ""
        for i in range(self._capacity):
            if self._elems[i]:
                string += '{} -> {}\n'.format(i, str(self._elems[i]))
        return string

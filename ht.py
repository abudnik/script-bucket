# Another yet MyHashTable
# Budnik Andrew, 2013.  Public domain.

from bisect import bisect_right

class HT():
    def __init__(self, initial_capacity=251, hash_fun=None):
        self.capacity = initial_capacity
        self.array = [[] for i in range(initial_capacity)]
        self.size = 0
        if hash_fun is None:
            self._hf = self._hash
        else:
            self._hf = hash_fun
        # init various statistics
        self._resize_cnt = 0

    def append(self, key, value):
        if self._need_resize():
            self._resize()
        self._set(key, value)
    
    def find(self, key):
        i = self._hf(key, self.capacity)
        for e in self.array[i]:
            if e[0] == key:
                return e[1]
        return None

    def remove(self, key):
        i = self._hf(key, self.capacity)
        for j in range(len(self.array[i])):
            if self.array[i][j][0] == key:
                del self.array[i][j]
                self.size -= 1
                if self._need_resize():
                    self._resize()
                return True
        return False

    def _need_resize(self):
        return self._get_optimal_capacity(self.size, self.capacity) != self.capacity

    def _set(self, key, value):
        i = self._hf(key, self.capacity)
        for e in self.array[i]:
            if e[0] == key:
                e[1] = value
                return
        self.array[i].append( [key, value] )
        self.size += 1

    def _resize(self):
        new = HT(self._get_optimal_capacity(self.size, self.capacity))
        for e in self:
            new._set(e[0], e[1])
        self.array = new.array
        self.capacity = new.capacity
        self._resize_cnt += 1
        print self.capacity

    @staticmethod
    def _get_optimal_capacity(size, capacity):
        optimal_capacity = (251,509,1021,2039,4093,8191,16381,32749,
                            65521,131071,262139,524287,1048573,2097143,
                            4194301,8388593,16777213,33554393,67108859,
                            134217689,268435399,536870909,1073741789)
        if size > optimal_capacity[-1]:
            return capacity << 1
        i = bisect_right(optimal_capacity, size)
        return optimal_capacity[i]

    @staticmethod
    def _hash(key, capacity):
        h = 0
        a = 127
        str_key = str(key)
        for i in range(len(str_key)):
            h = (h * a + ord(str_key[i])) % capacity
        return h

    def __iter__(self):
        for l in self.array:
            if not l: continue
            for e in l:
                yield e

    def print_stats(self):
        print 'size:', self.size
        print 'resize count:', self._resize_cnt

        hist_size = 100
        step = self.capacity / hist_size
        cnt = 0
        for i in range(self.capacity):
            if i % step == 0:
                #print '*' * (cnt / 10)
                cnt = 0
            cnt += len(self.array[i])

def Main():
    ht = HT()

    f = open('big.txt')
    for line in f:
        words = line.split()
        for w in words:
            ht.append( w, 'data_'+w )
            v = ht.find(w)
            if v is None:
                print 'Error: item wasn\'t found', w
                return

    words = [w[0] for w in ht]
    for w in words:
        if ht.remove(w) == False:
            print 'Error: item wasn\'t removed', w
            return

    ht.print_stats()

Main()

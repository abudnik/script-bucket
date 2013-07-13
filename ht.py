# Another yet MyHashTable

from bisect import bisect_right, bisect


# Simple (separate chaining with linked lists)
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


# Open adressing with linear probing
class HT_linear():
    def __init__(self, initial_capacity=251, hash_fun=None):
        self.capacity = initial_capacity
        self.array = initial_capacity*[None]
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
        while self.array[i] is not None:
            if self.array[i][0] == key:
                return self.array[i][1]
            i = (i + 1) % self.capacity
        return None

    def remove(self, key):
        i = self._hf(key, self.capacity)
        while self.array[i] is not None:
            if self.array[i][0] == key:
                break
            i = (i + 1) % self.capacity

        if self.array[i] is None:
            return False

        self.array[i] = None
        self.size -= 1
        j = (i + 1) % self.capacity
        while self.array[j] is not None:
            item = self.array[j]
            self.array[j] = None
            self.size -= 1
            self._set(item[0], item[1])
            j = (j + 1) % self.capacity
        if self._need_resize():
            self._resize()
        return True

    def _need_resize(self):
        if self.size > (self.capacity >> 1):
            return True
        if self.size > 251 and self.size < (self.capacity >> 3):
            return True
        return False

    def _set(self, key, value):
        i = self._hf(key, self.capacity)
        while self.array[i] is not None:
            if self.array[i][0] == key:
                self.array[i][1] = value
                return
            i = (i + 1) % self.capacity
        self.array[i] = [key, value]
        self.size += 1

    def _resize(self):
        new = HT_linear(self._get_optimal_capacity(self.size, self.capacity))
        for e in self:
            new._set(e[0], e[1])
        self.array = new.array
        self.capacity = new.capacity
        self._resize_cnt += 1
        print self.capacity

    @staticmethod
    def _get_next_capacity(capacity, increase=True):
        optimal_capacity = (251,509,1021,2039,4093,8191,16381,32749,
                            65521,131071,262139,524287,1048573,2097143,
                            4194301,8388593,16777213,33554393,67108859,
                            134217689,268435399,536870909,1073741789)
        if increase == True and capacity == optimal_capacity[-1]:
            return optimal_capacity << 1
        #if increase == False and capacity > optimal_capacity[-1]:
        i = bisect(optimal_capacity, capacity)
        if increase == True:
            return optimal_capacity[i]
        else:
            if i > 1:
                return optimal_capacity[i-2]
            else:
                return optimal_capacity[0]

    @staticmethod
    def _get_optimal_capacity(size, capacity):
        if size > (capacity >> 1):
            return HT_linear._get_next_capacity(capacity)
        else:
            return HT_linear._get_next_capacity(capacity, False)

    @staticmethod
    def _hash(key, capacity):
        h = 0
        a = 127
        str_key = str(key)
        for i in range(len(str_key)):
            h = (h * a + ord(str_key[i])) % capacity
        return h

    def __iter__(self):
        for e in self.array:
            if e is not None:
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
            if self.array[i] is not None:
                cnt += 1


# Open adressing with quadratic probing
class HT_quadratic():
    def __init__(self, initial_capacity=251, hash_fun=None):
        self.capacity = initial_capacity
        self.array = initial_capacity*[None]
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
        i = h = self._hf(key, self.capacity)
        k = 1
        while self.array[i] is not None:
            if self.array[i] is not 0 and self.array[i][0] == key:
                return self.array[i][1]
            i = (h + k * k) % self.capacity
            k += 1
        return None

    def remove(self, key):
        i = h = self._hf(key, self.capacity)
        k = 1
        while self.array[i] is not None:
            if self.array[i] is not 0 and self.array[i][0] == key:
                break
            i = (h + k * k) % self.capacity
            k += 1

        if self.array[i] is None:
            return False

        self.array[i] = 0
        self.size -= 1
        if self._need_resize():
            self._resize()
        return True

    def _need_resize(self):
        if self.size > (self.capacity >> 1):
            return True
        if self.size > 251 and self.size < (self.capacity >> 3):
            return True
        return False

    def _set(self, key, value):
        i = h = self._hf(key, self.capacity)
        k = 1
        while self.array[i] is not None:
            if self.array[i] is not 0 and self.array[i][0] == key:
                self.array[i][1] = value
                return
            i = (h + k * k) % self.capacity
            k += 1
        self.array[i] = [key, value]
        self.size += 1

    def _resize(self):
        new = HT_quadratic(self._get_optimal_capacity(self.size, self.capacity))
        for e in self:
            new._set(e[0], e[1])
        self.array = new.array
        self.capacity = new.capacity
        self._resize_cnt += 1
        print self.capacity

    @staticmethod
    def _get_next_capacity(capacity, increase=True):
        optimal_capacity = (251,509,1021,2039,4093,8191,16381,32749,
                            65521,131071,262139,524287,1048573,2097143,
                            4194301,8388593,16777213,33554393,67108859,
                            134217689,268435399,536870909,1073741789)
        if increase == True and capacity == optimal_capacity[-1]:
            return optimal_capacity << 1
        #if increase == False and capacity > optimal_capacity[-1]:
        i = bisect(optimal_capacity, capacity)
        if increase == True:
            return optimal_capacity[i]
        else:
            if i > 1:
                return optimal_capacity[i-2]
            else:
                return optimal_capacity[0]

    @staticmethod
    def _get_optimal_capacity(size, capacity):
        if size > (capacity >> 1):
            return HT_linear._get_next_capacity(capacity)
        else:
            return HT_linear._get_next_capacity(capacity, False)

    @staticmethod
    def _hash(key, capacity):
        h = 0
        a = 127
        str_key = str(key)
        for i in range(len(str_key)):
            h = (h * a + ord(str_key[i])) % capacity
        return h

    def __iter__(self):
        for e in self.array:
            if e is not None and e is not 0:
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
            if self.array[i] is not None:
                cnt += 1

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

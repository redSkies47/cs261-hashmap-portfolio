# Name:         Jonathan Chan
# OSU Email:    chanjon@oregonstate.edu
# Course:       CS261 - Data Structures
# Assignment:   HashMap Implementation
# Due Date:     06/03/2022
# Description:  An implementation of the HashMap with open addressing and its methods.


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Places or updates an existing key/value pair in the hash map.

        :param key: A string to serve as the key in the key-value pair.
        :param value: The desired value to store in the hash map.
        """

        # check the load factor & resize if >= 0.5
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity*2)

        # generate a 'hash' index
        hash_index = self._hash_function(key) % self._capacity

        # tracker for 'putting' the provided key-value pair
        placed = False
        quad = 1  # helps with quadratic probing

        # attempt to place into a bucket
        while not placed:
            current_bucket = self._buckets.get_at_index(hash_index)

            # verify current bucket can save a key-value pair
            if current_bucket is None or current_bucket.is_tombstone:
                self._buckets[hash_index] = HashEntry(key, value)
                self._size += 1
                placed = True

            # update existing key-value pair
            elif current_bucket.key == key:
                current_bucket.value = value
                placed = True

            # must do collision resolution with OA when different key
            else:
                # use quadratic probing to find next available spot
                hash_index = (self._hash_function(key) + quad**2) % \
                             self._capacity
                quad += 1

    def table_load(self) -> float:
        """
        Provides the average amount of objects stored in each bucket of
        the hash map.

        :return: A float to represent the average amount of objects per
        bucket.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Provides the amount of empty buckets in the hash table.

        :return: A positive integer that represents empty buckets.
        """
        # counter of empty buckets
        amount = 0

        # go through each bucket to count any 'empty' ones
        for index in range(self._capacity):
            bucket = self._buckets.get_at_index(index)

            # count every time there's no bucket or tombstone
            if not bucket or bucket.is_tombstone:
                amount += 1

        return amount

    def resize_table(self, new_capacity: int) -> None:
        """
        Allows the hash map to be resized to provided capacity. Key-value
        pairs are re-hashed.

        :param new_capacity: A positive integer that must be at least 1.
        """
        # case where new capacity is an invalid integer
        if new_capacity < 1 or new_capacity < self._size:
            return

        # 'save' some old hash map parts
        old_buckets = self._buckets
        old_capacity = self._capacity

        # initialize new hash table
        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(None)
        self._size = 0

        # update pointers
        self._capacity = new_capacity
        self._buckets = new_buckets

        # place key-value pairs from old table into new one
        for index in range(old_capacity):
            current_bucket = old_buckets.get_at_index(index)

            if current_bucket is None:
                pass

            elif current_bucket.is_tombstone:
                pass

            else:
                # only buckets with 'valid' keys get replaced
                current_key = current_bucket.key
                current_value = current_bucket.value

                self.put(current_key, current_value)

    def get(self, key: str) -> object:
        """
        Provides the associated value of the provided key. If key doesn't
        exist in the hash map, then it returns None.

        :param key: A string as the key in the desired key-value pair.
        :return: value: An object of the key-value pair.
        :return: None: The key was not found in the hash map.
        """
        # initialize value to return
        value = None

        # generate the hash index
        hash_index = self._hash_function(key) % self._capacity

        # initialize trackers for ending while loop
        end_search = False
        found = False
        quad = 1  # helps with quadratic probing

        # find the desired key
        while not end_search and not found:

            # see the bucket contents
            hash_entry = self._buckets.get_at_index(hash_index)

            if hash_entry is None:
                end_search = True

            # finding the bucket with desired key
            elif not hash_entry.is_tombstone and hash_entry.key == key:
                value = hash_entry.value
                found = True
            else:
                # calculate a new hash using quadratic probing
                hash_index = (self._hash_function(key) + quad**2)\
                             % self._capacity
                quad += 1

        return value

    def contains_key(self, key: str) -> bool:
        """
        Verifies if the provided key is in the hash map as a key-value
        pair.

        :param key: A string as the key in a key-value pair.
        :return: True: The provided key matched a key-value pair.
        :return: False: The provided key was not found.
        """
        # case where empty hash map doesn't contain any key-value pairs
        if self._size == 0:
            return False

        # get the hash entry at the intended hash index
        hash_index = self._hash_function(key) % self._capacity

        # initialize when while loop may end
        end_search = False
        quad = 1

        while not end_search:
            hash_entry = self._buckets.get_at_index(hash_index)

            if hash_entry is None:
                end_search = True

            # matching the key
            elif not hash_entry.is_tombstone and hash_entry.key == key:
                return True

            # calculate a new hash using quadratic probing
            else:
                hash_index = (self._hash_function(key) + quad**2)\
                             % self._capacity
                quad += 1

        # case where no matching key-value pair was found
        return False

    def remove(self, key: str) -> None:
        """
        Removes the associated key-value pair of the provided key. If key
        is not in the hash map, then there are no changes to the hash map.

        :param key: A string as the key in the key-value pair.
        """
        # case where empty hash map doesn't contain any key-value pairs
        if self._size == 0:
            return

        # get the hash entry at the intended hash index
        hash_index = self._hash_function(key) % self._capacity

        # initialize when while loop may end
        end_search = False
        found = False
        quad = 1

        while not end_search and not found:
            hash_entry = self._buckets.get_at_index(hash_index)

            if hash_entry is None:
                end_search = True

            # transform hash entry to tombstone
            elif not hash_entry.is_tombstone and hash_entry.key == key:
                hash_entry.is_tombstone = True
                self._size -= 1
                found = True

            else:
                # calculate a new hash using quadratic probing
                hash_index = (self._hash_function(key) + quad**2)\
                             % self._capacity
                quad += 1

    def clear(self) -> None:
        """
        Allows the clearing of all stored data in the hash map. It
        maintains the same hash map capacity and its hash function.
        """
        # initialize the new hash table
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._size = 0

    def get_keys(self) -> DynamicArray:
        """
        Provides all the keys in the hash map.

        :return: A dynamic array with all the keys in the hash map.
        """
        # initialize da to return
        da_of_keys = DynamicArray()

        # go through each bucket and get the HashEntry
        for bucket_index in range(self._capacity):
            hash_entry = self._buckets.get_at_index(bucket_index)

            if hash_entry is None:
                pass
            elif hash_entry.is_tombstone:
                pass

            # record key of valid hash entry
            else:
                da_of_keys.append(hash_entry.key)

        return da_of_keys


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())

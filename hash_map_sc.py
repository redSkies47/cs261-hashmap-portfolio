# Name:         Jonathan Chan
# OSU Email:    chanjon@oregonstate.edu
# Course:       CS261 - Data Structures
# Assignment:   HashMap Implementation
# Due Date:     06/03/2022
# Description:  An implementation of the HashMap withs chaining and its methods.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

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
        # generate a 'hash' index
        hash_index = self._hash_function(key) % self._capacity

        # case of empty bucket, new linked list & add key-value pair
        if self._buckets.get_at_index(hash_index) is None:
            ll = LinkedList()
            ll.insert(key, value)
            self._buckets.set_at_index(hash_index, ll)
            self._size += 1
        else:
            # case of prior entry in target bucket, seek provided key
            ll = self._buckets.get_at_index(hash_index)

            if ll.contains(key) is not None:
                # update associated value in key-value pair
                node_to_update = ll.contains(key)
                node_to_update.value = value
            else:
                # create a new key-value pair node
                ll.insert(key, value)
                self._size += 1

    def empty_buckets(self) -> int:
        """
        Provides the amount of empty buckets in the hash table.

        :return: A positive integer that represents empty buckets.
        """
        # counter of empty linked lists
        amount = 0

        # go through each bucket and find size 0 ll
        for index in range(self._capacity):
            ll = self._buckets.get_at_index(index)
            if ll.length() == 0:
                amount += 1

        return amount

    def table_load(self) -> float:
        """
        Provides the average amount of objects stored in each bucket of
        the hash map.

        :return: A float to represent the average amount of objects per
        bucket.
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Allows the clearing of all stored data in the hash map. It
        maintains the same hash map capacity and its hash function.
        """
        # create a new da and initiate each bucket
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Allows the hash map to be resized to provided capacity. Key-value
        pairs are re-hashed.

        :param new_capacity: A positive integer that must at least 1.
        """
        # case where new capacity is an invalid integer
        if new_capacity < 1:
            return

        # initialize the new hash table
        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(LinkedList())

        # place key-value pairs from old table into the new one
        for index in range(self._capacity):
            current_bucket = self._buckets.get_at_index(index)
            if current_bucket.length() != 0:
                # transfer each key-value
                for node in current_bucket:
                    # generate hash index and insert it to its linked list
                    new_index = self._hash_function(node.key) % new_capacity
                    ll = new_buckets.get_at_index(new_index)
                    ll.insert(node.key, node.value)

        # update pointer to new hash table & new capacity
        self._buckets = new_buckets
        self._capacity = new_capacity

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

        # get the linked list at the intended hash index
        hash_index = self._hash_function(key) % self._capacity
        ll = self._buckets.get_at_index(hash_index)

        # find case where linked list contains the key
        node = ll.contains(key)
        if node:
            value = node.value

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

        # get the linked list at the intended hash index
        hash_index = self._hash_function(key) % self._capacity
        ll = self._buckets.get_at_index(hash_index)

        # find the key-value pair in the linked list
        node = ll.contains(key)
        if node:
            return True

        # case where node was None so no key-value pair found
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

        # get the linked list at the intended hash index
        hash_index = self._hash_function(key) % self._capacity
        ll = self._buckets.get_at_index(hash_index)

        # find the key-value pair in the linked list
        node = ll.contains(key)
        if node:
            ll.remove(key)
            self._size -= 1

    def get_keys(self) -> DynamicArray:
        """
        Provides all the keys in the hash map.

        :return: A dynamic array with all the keys in the hash map.
        """
        # initialize da to return
        da_of_keys = DynamicArray()

        # go through each bucket and get the linked list
        for bucket_index in range(self._capacity):
            ll = self._buckets.get_at_index(bucket_index)
            # when ll contains some key-value pairs
            if ll.length != 0:
                # go through each node and place key in da
                for node in ll:
                    da_of_keys.append(node.key)

        return da_of_keys


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Provides the mode of the elements in the provided da. The mode is returned
    as a collection in a different da and a positive integer to represent its
    freq.

    :param da: The collection of elements to evaluate and find its mode.
    :return: da: A new collection of the mode(s) found.
    :return: int: A positive integer to represent the freq of the mode.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap(da.length() // 3, hash_function_1)

    # go through each bucket, O(n)
    for index in range(da.length()):
        current_element = da.get_at_index(index)

        # increase frequency when it's a repeat value
        if map.contains_key(current_element):
            freq = map.get(current_element)
            freq += 1
            map.put(current_element, freq)
        else:
            # start tracking a new value
            map.put(current_element, 1)

    # initiate da to return
    da_of_mode = DynamicArray()
    highest_frequency = 0

    # identify the element(s) with the highest frequency, O(n)
    unique_elements = map.get_keys()
    for unique_index in range(unique_elements.length()):

        # access key and frequency
        current_key = unique_elements.get_at_index(unique_index)
        current_freq = map.get(current_key)

        # when higher frequency is found, reset da_of_mode w/ only this element
        if current_freq > highest_frequency:
            da_of_mode = DynamicArray()
            da_of_mode.append(current_key)
            highest_frequency = current_freq

        # when its the same frequency, append this element
        elif current_freq == highest_frequency:
            da_of_mode.append(current_key)

        # disregard element with less frequency and move onto next one!

    return da_of_mode, highest_frequency


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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")

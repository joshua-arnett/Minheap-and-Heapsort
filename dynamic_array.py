# Name: Joshua Arnett
# OSU Email: arnettj@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 2
# Due Date: 07/16/2024
# Description: Created a DynamicArray class with several methods defined as required by the assignment instructions.

from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Creates a new array with the specified new capacity.
        Updates the current DynamicArray object's with the new data and capacity.
        """
        # New capacity has to be large enough to hold existing elements and cannot be less than 1
        if new_capacity < self._size or new_capacity < 1:
            return

        new_array = StaticArray(new_capacity)

        # Copy all the existing elements to the new array
        for num in range(self._size):
            element = self._data.get(num)
            new_array.set(num, element)

        # Update current object's data and capacity attributes
        self._data = new_array
        self._capacity = new_capacity

    def append(self, value: object) -> None:
        """
        Adds new item to the end of an array.
        """
        # Before we add anything, check to see if the array is already full. If so, we double its capacity
        if self._capacity == self._size:
            self.resize(self._capacity * 2)

        # Add element to the end of the array and increment the array's size attribute
        self._data.set(self._size, value)
        self._size += 1

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Inserts element in a specified index, shifting all other values to the right.
        """
        # Valid indices are [0, N] inclusive.
        if self._size < index or index < 0:
            raise DynamicArrayException

        # If array is already full, double its capacity
        if self._size == self._capacity:
            self.resize(self._capacity * 2)

        # We count backwards to reach the last elements first, moving them an index forward
        for num in range(self._size - 1, index - 1, -1):
            element = self._data.get(num)
            self._data.set(num + 1, element)

        # Finally we add the element and increment the array's size attribute
        self._size += 1
        self._data.set(index, value)

    def remove_at_index(self, index: int) -> None:
        """
        Removes element from a specified index, shifting all other values to the left.
        """
        # Valid indices are [0, N - 1] inclusive.
        if index < 0 or index > self._size - 1:
            raise DynamicArrayException

        # Before we remove anything, if number of elements is < 1/4 of its current capacity AND capacity > 10,
        # we lessen the capacity to twice the number of existing elements
        if self._capacity / 4 > self._size and self._capacity > 10:
            # The reduced capacity cannot become less than 10 elements.
            if self._size * 2 < 10:
                new_array = StaticArray(10)
                self._capacity = 10
            else:
                new_array = StaticArray(self._size * 2)
                self._capacity = self._size * 2

            # Copy existing elements in new array and set it equal to the current object's data attribute
            for num in range(self._size):
                element = self._data.get(num)
                new_array.set(num, element)
            self._data = new_array

        # Set the removed element's index value equal to None
        self._data.set(index, None)

        # Shift values at the right of the removed value to the left
        for num in range(index + 1, self._size):
            element = self._data.get(num)
            self._data.set(num, None)
            self._data.set(num - 1, element)

        # Decrement the current object's size attribute
        self._size -= 1

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Returns a sliced array.

        start_index: Where to start the slice
        size: The size of the sliced array
        """
        # Start index and array size must be positive and within the bounds of the array
        if start_index < 0 or size < 0 or start_index > self._size - 1:
            raise DynamicArrayException
        # Size of the sliced array cannot be larger than the size of the unsliced array
        if size + start_index > self._size:
            raise DynamicArrayException

        # Append sliced elements in our new array
        new_dyn_array = DynamicArray()
        for num in range(start_index, start_index + size):
            element = self._data.get(num)
            new_dyn_array.append(element)

        return new_dyn_array

    def merge(self, second_da: "DynamicArray") -> None:
        """
        Merge two DynamicArray objects.
        """
        for element in second_da:
            self.append(element)

    def map(self, map_func) -> "DynamicArray":
        """
        Computes the map function using elements from the array as arguments.
        Returns new array with the output values.
        """
        new_array = DynamicArray()

        for num in range(self._size):
            element = self._data.get(num)
            new_array.append(map_func(element))

        return new_array

    def filter(self, filter_func) -> "DynamicArray":
        """
        Computes the filter function using elements from the array as arguments.
        Returns new array with the filtered values.
        """
        new_array = DynamicArray()

        for num in range(self._size):
            element = self._data.get(num)
            if filter_func(element) is True:
                new_array.append(element)

        return new_array

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Sequentially applies the reduce_func to all elements of the dynamic array and
        returns the resulting value.
        """
        # If array's size is 0, return the initializer
        if self._size == 0:
            return initializer

        # If initializer is None, we set it equal to the first element of the array
        if initializer is None:
            initializer = self._data.get(0)
        # Else, we use the reduce function on the initializer and the first element and use the result going forward
        else:
            initializer = reduce_func(initializer, self._data.get(0))

        # We loop through and use the reduce function on all the elements of the array,
        # storing our result in the initializer variable
        for num in range(1, self._size):
            element = self._data.get(num)
            initializer = reduce_func(initializer, element)

        return initializer


def find_mode(arr: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Returns a tuple containing the mode and its frequency within the sorted data set.
    arr: a StaticArray object
    """
    # STEP 1: FIND THE MODE FREQUENCY
    mode_frequency = 0

    current_value = None
    current_frequency = 0

    for array_index in range(arr.length()):
        element = arr.get_at_index(array_index)

        # If our current value is equal to the element, increment the current value's frequency by 1
        if element == current_value:
            current_frequency += 1
        # If our current value != the element, we set the current value equal to the new element
        else:
            current_value = element
            current_frequency = 1

        # Check if current value's frequency exceeds our current mode's.
        # If so, set our current mode equal to the current value.
        if current_frequency > mode_frequency:
            mode_frequency = current_frequency

    # STEP 2: ADD THE ELEMENTS THAT HAVE THE SAME FREQUENCY AS THE MODE TO A NEW ARRAY
    current_frequency = 1
    array_index = 0
    new_array = DynamicArray()

    while array_index <= arr.length() - 1:
        element = arr.get_at_index(array_index)

        # If there is still a next element, do this:
        if array_index < arr.length() - 1:
            next_element = arr.get_at_index(array_index + 1)

            # If our current element is equal to the next, increment the current value's frequency by 1
            if element == next_element:
                current_frequency += 1
            # Else, we compare its frequency to the mode's. If they are equal, add it to the new array
            else:
                if current_frequency == mode_frequency:
                    new_array.append(element)
                # Reset current value's frequency
                current_frequency = 1
        # If we are at the last element and its frequency is equal to the mode frequency, add it to the new array
        elif array_index == arr.length() - 1 and current_frequency == mode_frequency:
            new_array.append(element)

        array_index += 1

    return (new_array, mode_frequency)


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":
    # print("\n# resize - example 1")
    # da = DynamicArray()
    #
    # # print dynamic array's size, capacity and the contents
    # # of the underlying static array (data)
    # da.print_da_variables()
    # da.resize(8)
    # da.print_da_variables()
    # da.resize(2)
    # da.print_da_variables()
    # da.resize(0)
    # da.print_da_variables()
    #
    # print("\n# resize - example 2")
    # da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    # print(da)
    # da.resize(20)
    # print(da)
    # da.resize(4)
    # print(da)
    #
    # print("\n# append - example 1")
    # da = DynamicArray()
    # da.print_da_variables()
    # da.append(1)
    # da.print_da_variables()
    # print(da)
    #
    # print("\n# append - example 2")
    # da = DynamicArray()
    # for i in range(9):
    #     da.append(i + 101)
    #     print(da)
    #
    # print("\n# append - example 3")
    # da = DynamicArray()
    # for i in range(600):
    #     da.append(i)
    # print(da.length())
    # print(da.get_capacity())
    #
    # print("\n# insert_at_index - example 1")
    # da = DynamicArray([100])
    # print(da)
    # da.insert_at_index(0, 200)
    # da.insert_at_index(0, 300)
    # da.insert_at_index(0, 400)
    # print(da)
    # da.insert_at_index(3, 500)
    # print(da)
    # da.insert_at_index(1, 600)
    # print(da)
    #
    # print("\n# insert_at_index example 2")
    # da = DynamicArray()
    # try:
    #     da.insert_at_index(-1, 100)
    # except Exception as e:
    #     print("Exception raised:", type(e))
    # da.insert_at_index(0, 200)
    # try:
    #     da.insert_at_index(2, 300)
    # except Exception as e:
    #     print("Exception raised:", type(e))
    # print(da)
    #
    # print("\n# insert at index example 3")
    # da = DynamicArray()
    # for i in range(1, 10):
    #     index, value = i - 4, i * 10
    #     try:
    #         da.insert_at_index(index, value)
    #     except Exception as e:
    #         print("Cannot insert value", value, "at index", index)
    # print(da)
    #
    # print("\n# remove_at_index - example 1")
    # da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    # print(da)
    # da.remove_at_index(0)
    # print(da)
    # da.remove_at_index(6)
    # print(da)
    # da.remove_at_index(2)
    # print(da)
    #
    # print("\n# remove_at_index - example 2")
    # da = DynamicArray([1024])
    # print(da)
    # for i in range(17):
    #     da.insert_at_index(i, i)
    # print(da.length(), da.get_capacity())
    # for i in range(16, -1, -1):
    #     da.remove_at_index(0)
    # print(da)
    #
    # print("\n# remove_at_index - example 3")
    # da = DynamicArray()
    # print(da.length(), da.get_capacity())
    # [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    # print(da.length(), da.get_capacity())
    # [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    # print(da.length(), da.get_capacity())
    # da.remove_at_index(0)  # step 3 - remove 1 element
    # print(da.length(), da.get_capacity())
    # da.remove_at_index(0)  # step 4 - remove 1 element
    # print(da.length(), da.get_capacity())
    # [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    # print(da.length(), da.get_capacity())
    # da.remove_at_index(0)  # step 6 - remove 1 element
    # print(da.length(), da.get_capacity())
    # da.remove_at_index(0)  # step 7 - remove 1 element
    # print(da.length(), da.get_capacity())
    #
    # for i in range(14):
    #     print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
    #     da.remove_at_index(0)
    #     print(" After remove_at_index(): ", da.length(), da.get_capacity())
    #
    # print("\n# remove at index - example 4")
    # da = DynamicArray([1, 2, 3, 4, 5])
    # print(da)
    # for _ in range(5):
    #     da.remove_at_index(0)
    #     print(da)
    #
    # print("\n# slice example 1")
    # da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    # da_slice = da.slice(1, 3)
    # print(da, da_slice, sep="\n")
    # da_slice.remove_at_index(0)
    # print(da, da_slice, sep="\n")
    #
    # print("\n# slice example 2")
    # da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    # print("SOURCE:", da)
    # slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    # for i, cnt in slices:
    #     print("Slice", i, "/", cnt, end="")
    #     try:
    #         print(" --- OK: ", da.slice(i, cnt))
    #     except:
    #         print(" --- exception occurred.")

    # print("\n# merge example 1")
    # da = DynamicArray([1, 2, 3, 4, 5])
    # da2 = DynamicArray([10, 11, 12, 13])
    # print(da)
    # da.merge(da2)
    # print(da)
    #
    # print("\n# merge example 2")
    # da = DynamicArray([1, 2, 3])
    # da2 = DynamicArray()
    # da3 = DynamicArray()
    # da.merge(da2)
    # print(da)
    # da2.merge(da3)
    # print(da2)
    # da3.merge(da)
    # print(da3)
    #
    # print("\n# map example 1")
    # da = DynamicArray([1, 5, 10, 15, 20, 25])
    # print(da)
    # print(da.map(lambda x: x ** 2))
    #
    # print("\n# map example 2")
    #
    #
    # def double(value):
    #     return value * 2
    #
    #
    # def square(value):
    #     return value ** 2
    #
    #
    # def cube(value):
    #     return value ** 3
    #
    #
    # def plus_one(value):
    #     return value + 1
    #
    #
    # da = DynamicArray([plus_one, double, square, cube])
    # for value in [1, 10, 20]:
    #     print(da.map(lambda x: x(value)))
    #
    # print("\n# filter example 1")
    #
    #
    # def filter_a(e):
    #     return e > 10
    #
    #
    # da = DynamicArray([1, 5, 10, 15, 20, 25])
    # print(da)
    # result = da.filter(filter_a)
    # print(result)
    # print(da.filter(lambda x: (10 <= x <= 20)))
    #
    # print("\n# filter example 2")
    #
    #
    # def is_long_word(word, length):
    #     return len(word) > length
    #
    #
    # da = DynamicArray("This is a sentence with some long words".split())
    # print(da)
    # for length in [3, 4, 7]:
    #     print(da.filter(lambda word: is_long_word(word, length)))
    #
    # print("\n# reduce example 1")
    # values = [100, 5, 10, 15, 20, 25]
    # da = DynamicArray(values)
    # print(da)
    # print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    # print(da.reduce(lambda x, y: (x + y ** 2), -1))
    #
    # print("\n# reduce example 2")
    # da = DynamicArray([100])
    # print(da.reduce(lambda x, y: x + y ** 2))
    # print(da.reduce(lambda x, y: x + y ** 2, -1))
    # da.remove_at_index(0)
    # print(da.reduce(lambda x, y: x + y ** 2))
    # print(da.reduce(lambda x, y: x + y ** 2, -1))
    #
    print("\n# find_mode - example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")

# Name: Joshua Arnett
# OSU Email: arnettj@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 5
# Due Date: 08/05/2024
# Description: Defines a MinHeap class with various methods to support its functionality.
#               Also defines a heapsort function that sorts an array using the heapsort algorithm.

from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()

        # populate MinHeap with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MinHeap content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return "HEAP " + str(heap_data)

    def add(self, node: object) -> None:
        """
        Adds new item to the heap in the appropriate place.
        """
        self._heap.append(node)

        # If there is only one value in the heap, there is nothing to swap
        if self.size() > 1:
            node_index = self.size() - 1
            parent_index = (node_index - 1)//2

            node_value = self._heap.get_at_index(node_index)
            parent_value = self._heap.get_at_index(parent_index)

            in_right_place = False
            while not in_right_place:
                # If we are at the root, we stop going up the tree
                if parent_index == 0:
                    in_right_place = True

                if node_value < parent_value:
                    # If the node's value is less than its parent's, swap the values
                    self._heap.set_at_index(parent_index, node_value)
                    self._heap.set_at_index(node_index, parent_value)

                    # We update the node's index and value, as well as its parent's
                    node_index = parent_index
                    parent_index = (node_index - 1) // 2
                    # We use this condition to avoid getting a value from index -1
                    if not in_right_place:
                        node_value = self._heap.get_at_index(node_index)
                        parent_value = self._heap.get_at_index(parent_index)
                # If the node's value is >= its parent's value, it is in the right place
                else:
                    in_right_place = True

    def is_empty(self) -> bool:
        """
        Returns True if the heap is empty. Returns False otherwise.
        """
        if self._heap.is_empty():
            return True
        return False

    def get_min(self) -> object:
        """
        Returns the minimum value of the heap.
        """
        if self.is_empty():
            raise MinHeapException
        return self._heap.get_at_index(0)

    def remove_min(self) -> object:
        """
        Removes and returns the minimum value of the heap.
        """
        if self.is_empty():
            raise MinHeapException

        # Get min value
        min_value = self.get_min()

        # Get last value
        last_val = self._heap.get_at_index(self.size() - 1)

        # Remove last value
        self._heap.remove_at_index(self.size() - 1)

        # If elements still exist within the heap, set the root equal to the last value and percolate down
        if self.size() > 0:
            self._heap.set_at_index(0, last_val)
            _percolate_down(da=self._heap, parent=last_val, parent_index=0)

        return min_value

    def build_heap(self, da: DynamicArray) -> None:
        """
        Replaces the heap with a new heap, built from the values within the specified array.
        """
        # We create a new array
        self._heap = DynamicArray(da)

        # We get the first non-leaf node's index
        node_index = (self._heap.length() // 2) - 1

        # We sort the nodes according to their values, going up until we get to the root
        while node_index >= 0:
            node = self._heap.get_at_index(node_index)
            _percolate_down(da=self._heap, parent=node, parent_index=node_index)
            node_index -= 1

    def size(self) -> int:
        """
        Returns the size of the heap.
        """
        return self._heap.length()

    def clear(self) -> None:
        """
        Clears the heap.
        """
        self._heap = DynamicArray()


def heapsort(da: DynamicArray) -> None:
    """
    Sorts an array using a heapsort algorithm.
    """
    # We build a heap using the passed array (same process as build_heap() above)
    heap = da
    # We get the first non-leaf node's index
    node_index = (heap.length() // 2) - 1

    # We sort the nodes according to their values, going up until we get to the root
    while node_index >= 0:
        node = heap.get_at_index(node_index)
        _percolate_down(da=heap, parent=node, parent_index=node_index)
        node_index -= 1

    # We perform the heapsort algorithm on the heap
    k = da.length()
    while k > 0:
        # Get first value
        first_val = heap.get_at_index(0)
        # Swap first and last values
        da.set_at_index(0, heap.get_at_index(k - 1))
        da.set_at_index(k - 1, first_val)

        # Decrement k
        k -= 1
        # Percolate down
        first_val = da.get_at_index(0)
        _percolate_down(da=da, parent=first_val, parent_index=0, max_index=k)


def _percolate_down(da: DynamicArray, parent: object, parent_index, max_index=None) -> None:
    """
    Percolates a value down the array, starting from the root.
    """
    def swap_with_child(parent_index, parent, child_index, child_value):
        """
        Swap child and parent values. Returns the new parent index.
        """
        # Swap child and parent values
        da.set_at_index(parent_index, child_value)
        da.set_at_index(child_index, parent)
        # Return the new parent index
        parent_index = child_index
        return parent_index

    # Using max_index to represent 'k', which points to the end of the heap portion in heap sort
    if max_index is None:
        max_index = da.length()

    in_right_place = False
    while not in_right_place:
        left_child_index = (2 * parent_index) + 1
        right_child_index = (2 * parent_index) + 2

        # -------------------------- Getting child values ---------------------------- #
        # If a child's index is >= our max index or the existing length of the heap, the child is nonexistent
        # So we set in_right_place equal to True and the child value equal to None

        # Left child
        if left_child_index >= max_index or left_child_index >= da.length():
            in_right_place = True
            left_child_value = None
        else:
            left_child_value = da.get_at_index(left_child_index)
        # Right child
        if right_child_index >= max_index or right_child_index >= da.length():
            in_right_place = True
            right_child_value = None
        else:
            right_child_value = da.get_at_index(right_child_index)

        # --------------------------- Swapping ----------------------------- #
        # If parent value is greater than both children, we compare the children and swap with the appropriate one
        if (left_child_value is not None and right_child_value is not None and
                parent > left_child_value and parent > right_child_value):
            if left_child_value <= right_child_value:
                # Swap with left child
                parent_index = swap_with_child(parent_index, parent, left_child_index, left_child_value)
            else:
                # Swap with right child
                parent_index = swap_with_child(parent_index, parent, right_child_index, right_child_value)
        elif left_child_value is not None and parent > left_child_value:
            # Swap with left child
            parent_index = swap_with_child(parent_index, parent, left_child_index, left_child_value)
        elif right_child_value is not None and parent > right_child_value:
            # Swap with right child
            parent_index = swap_with_child(parent_index, parent, right_child_index, right_child_value)
        else:
            # If no swaps happen, the value is at the right place!
            in_right_place = True


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())

    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)

    print("--------------------------")
    print("Inserting 500 into input DA:")
    da[0] = 500
    print(da)

    print("Your MinHeap:")
    print(h)
    if h.get_min() == 500:
        print("Error: input array and heap's underlying DA reference same object in memory")

    print("\nPDF - size example 1")
    print("--------------------")
    h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    print(h.size())

    print("\nPDF - size example 2")
    print("--------------------")
    h = MinHeap([])
    print(h.size())

    print("\nPDF - clear example 1")
    print("---------------------")
    h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(h)
    print(h.clear())
    print(h)

    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 2")
    print("------------------------")
    da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

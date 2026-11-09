from __future__ import annotations
from typing import Any
from exceptions import HeapError

class Heap:
    def __init__(self)-> None:
        # Flat array to represent the binary tree
        self._data: list[tuple[Any,int,Any]]= []
        # Counter guarantees stable FIFO sorting when keys are identical, 
        # so Python never tries to compare the actual objects.
        self._counter: int=0

    def push(
            self,
            key: Any,
            obj: Any
    )-> None:
        self._data.append((key, self._counter, obj))
        self._bubble_up(len(self._data)-1)
        self._counter +=1

    def pop(self) -> Any:
        if not self._data:
            raise HeapError("Cannot pop from an empty heap.")

        if len(self._data) == 1:
            return self._data.pop()[2]

        # Swap root with the last element to preserve tree shape
        self._data[0], self._data[-1] = self._data[-1], self._data[0]
        popped_item = self._data.pop()[2]

        self._bubble_down(0)
        return popped_item

    def peek(self) -> Any:
        if not self._data:
            raise HeapError("Cannot peek into an empty heap.")
        return self._data[0][2]

    def ksmallest(
            self,
            k: int
    )-> list[Any]:
        if k<-1:
            raise HeapError(f"Invalid value for k: {k}")

        n= len(self._data)
        # If k is -1 or larger than the heap, just extract everything
        if k == -1 or k > n:
            k = n

        if k == 0 or n == 0:
            return []

        result = []

        aux_heap = Heap()
        # Push the root's priority and its array index (0) into the aux heap
        aux_heap.push((self._data[0][0], self._data[0][1]), 0)

        for _ in range(k):
            idx = aux_heap.pop()
            result.append(self._data[idx][2])

            left_idx = 2 * idx + 1
            right_idx = 2 * idx + 2

            # Add valid children to the frontier
            if left_idx < n:
                aux_heap.push((self._data[left_idx][0], self._data[left_idx][1]), left_idx)
            if right_idx < n:
                aux_heap.push((self._data[right_idx][0], self._data[right_idx][1]), right_idx)

        return result

    @classmethod
    def heapify(cls, items: list[tuple[Any, Any]]) -> Heap:

        new_heap = cls()
        n = len(items)

        # Copy items over without aliasing the original list
        for i in range(n):
            key, obj = items[i]
            new_heap._data.append((key, i, obj))
            
        new_heap._counter = n
        
        # Sift down from the last parent node up to the root
        for i in range((n - 1) // 2, -1, -1):
            new_heap._bubble_down(i)
            
        return new_heap

    def _bubble_up(self, index: int) -> None:
        """Helper to move an item up the tree."""
        while index > 0:
            parent_idx = (index - 1) // 2
            if self._data[index] < self._data[parent_idx]:
                self._data[index], self._data[parent_idx] = self._data[parent_idx], self._data[index]
                index = parent_idx
            else:
                break

    def _bubble_down(self, index: int) -> None:
        """Helper to move an item down the tree."""
        n = len(self._data)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < n and self._data[left] < self._data[smallest]:
                smallest = left
            if right < n and self._data[right] < self._data[smallest]:
                smallest = right

            if smallest != index:
                self._data[index], self._data[smallest] = self._data[smallest], self._data[index]
                index = smallest
            else:
                break

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return len(self._data) > 0

    def __repr__(self) -> str:
        return f"Heap(size={len(self._data)})"        
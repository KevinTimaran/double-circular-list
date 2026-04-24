"""Doubly circular linked list implementation used by the application."""

from __future__ import annotations

from typing import Generic, Iterator, Optional, TypeVar

from dataStructures.node import Node

T = TypeVar("T")


class DoublyCircularList(Generic[T]):
    """A generic doubly circular linked list with cursor navigation."""

    def __init__(self) -> None:
        self.head: Optional[Node[T]] = None
        self.tail: Optional[Node[T]] = None
        self.current: Optional[Node[T]] = None
        self._size: int = 0

    def isEmpty(self) -> bool:
        """Return True if the list has no elements."""
        return self._size == 0

    def append(self, value: T) -> None:
        """Insert a value at the end of the list."""
        newNode = Node(value=value)

        if self.isEmpty():
            newNode.next = newNode
            newNode.previous = newNode
            self.head = newNode
            self.tail = newNode
            self.current = newNode
            self._size = 1
            return

        assert self.head is not None
        assert self.tail is not None

        newNode.previous = self.tail
        newNode.next = self.head
        self.tail.next = newNode
        self.head.previous = newNode
        self.tail = newNode
        self._size += 1

    def prepend(self, value: T) -> None:
        """Insert a value at the beginning of the list."""
        newNode = Node(value=value)

        if self.isEmpty():
            newNode.next = newNode
            newNode.previous = newNode
            self.head = newNode
            self.tail = newNode
            self.current = newNode
            self._size = 1
            return

        assert self.head is not None
        assert self.tail is not None

        newNode.next = self.head
        newNode.previous = self.tail
        self.head.previous = newNode
        self.tail.next = newNode
        self.head = newNode
        self._size += 1

    def remove(self, value: T) -> bool:
        """Remove the first node that matches value. Return True if removed."""
        if self.isEmpty() or self.head is None:
            return False

        node = self.head
        for _ in range(self._size):
            if node.value == value:
                self._removeNode(node)
                return True
            assert node.next is not None
            node = node.next

        return False

    def _removeNode(self, node: Node[T]) -> None:
        """Remove a node from the list and fix references."""
        if self._size == 1:
            self.head = None
            self.tail = None
            self.current = None
            self._size = 0
            return

        assert node.previous is not None
        assert node.next is not None
        previousNode = node.previous
        nextNode = node.next

        previousNode.next = nextNode
        nextNode.previous = previousNode

        if self.head is node:
            self.head = nextNode
        if self.tail is node:
            self.tail = previousNode
        if self.current is node:
            self.current = nextNode

        self._size -= 1

    def find(self, value: T) -> Optional[T]:
        """Return the first matching value if found; otherwise return None."""
        if self.isEmpty() or self.head is None:
            return None

        node = self.head
        for _ in range(self._size):
            if node.value == value:
                return node.value
            assert node.next is not None
            node = node.next

        return None

    def moveNext(self) -> Optional[T]:
        """Move cursor to next node and return current value."""
        if self.current is None:
            return None

        assert self.current.next is not None
        self.current = self.current.next
        return self.current.value

    def movePrevious(self) -> Optional[T]:
        """Move cursor to previous node and return current value."""
        if self.current is None:
            return None

        assert self.current.previous is not None
        self.current = self.current.previous
        return self.current.value

    def getCurrent(self) -> Optional[T]:
        """Return the value at the cursor without moving it."""
        if self.current is None:
            return None
        return self.current.value

    def __len__(self) -> int:
        """Return the number of nodes in the list."""
        return self._size

    def __iter__(self) -> Iterator[T]:
        """Iterate from head to tail exactly once."""
        if self.head is None:
            return

        node = self.head
        for _ in range(self._size):
            yield node.value
            assert node.next is not None
            node = node.next

    def __repr__(self) -> str:
        values = [repr(value) for value in self]
        return f"DoublyCircularList([{', '.join(values)}])"

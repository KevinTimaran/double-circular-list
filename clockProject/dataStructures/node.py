"""Node definition used by the doubly circular linked list."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


@dataclass
class Node(Generic[T]):
    """Represents a single node in a doubly circular linked list."""

    value: T
    previous: Optional["Node[T]"] = None
    next: Optional["Node[T]"] = None

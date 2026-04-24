"""Service layer for generic app history."""

from __future__ import annotations

from typing import Optional

from dataStructures.doublyCircularList import DoublyCircularList


class HistoryService:
    """Stores history entries with circular navigation support."""

    def __init__(self) -> None:
        self.history: DoublyCircularList[str] = DoublyCircularList()

    def addEntry(self, message: str) -> None:
        """Add an entry to history."""
        self.history.append(message)

    def clear(self) -> None:
        """Clear all history entries."""
        self.history = DoublyCircularList()

    def getEntries(self) -> list[str]:
        """Return all history entries as a list."""
        return list(self.history)

    def getCurrentEntry(self) -> Optional[str]:
        """Return current history entry from cursor."""
        return self.history.getCurrent()

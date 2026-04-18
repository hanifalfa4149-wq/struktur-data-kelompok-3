"""Antrean truk loading dock."""

from collections import deque


class TruckQueue:
    """Queue for truck loading dock operations."""

    def __init__(self) -> None:
        self._queue: deque[str] = deque()

    def enqueue(self, truck_id: str) -> None:
        self._queue.append(truck_id)

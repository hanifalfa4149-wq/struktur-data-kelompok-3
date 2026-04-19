"""Antrean truk loading dock."""

from collections import deque


class TruckQueue:
    """Queue FIFO untuk antrean truk."""

    def __init__(self) -> None:
        """Initialize empty queue."""
        self.queue = deque()

    def enqueue(self, plat_nomor: str) -> None:
        """Add a truck plate number to the queue tail."""
        self.queue.append(plat_nomor)

    def dequeue(self) -> str | None:
        """Remove and return the first truck plate, or None when empty."""
        if self.is_empty():
            return None
        return self.queue.popleft()

    def peek(self) -> str | None:
        """Return first truck plate without removing it."""
        if self.is_empty():
            return None
        return self.queue[0]

    def is_empty(self) -> bool:
        """Check whether queue is empty."""
        return len(self.queue) == 0

    def display_queue(self) -> None:
        """Print queue as numbered list."""
        if self.is_empty():
            print("Antrean kosong")
            return

        for idx, plat in enumerate(self.queue, start=1):
            print(f"{idx}. {plat}")

    def load_from_list(self, data: list) -> None:
        """Hydrate queue from list data."""
        self.queue = deque()
        if not isinstance(data, list):
            return
        for plat in data:
            self.queue.append(str(plat))

    def load_from_dict(self, data: dict) -> None:
        """Compatibility loader required by core conventions."""
        if isinstance(data, list):
            self.load_from_list(data)
            return
        if isinstance(data, dict):
            self.load_from_list(data.get("queue", []))
            return
        self.load_from_list([])

    def to_list(self) -> list:
        """Serialize queue into JSON-safe list."""
        return list(self.queue)

    def __repr__(self) -> str:
        """Return debug representation of queue state."""
        return f"TruckQueue(size={len(self.queue)})"

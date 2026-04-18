"""Riwayat muat / undo."""


class LoadHistory:
    """Stack for load history and undo operations."""

    def __init__(self) -> None:
        self._history: list[str] = []

    def push(self, action: str) -> None:
        self._history.append(action)

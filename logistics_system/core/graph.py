"""Peta distribusi antar kota."""


class CityGraph:
    """Graph representation for distribution map between cities."""

    def __init__(self) -> None:
        self.edges: dict[str, list[str]] = {}

    def connect(self, source: str, target: str) -> None:
        self.edges.setdefault(source, []).append(target)

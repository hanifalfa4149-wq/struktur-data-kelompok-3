"""Rute kurir."""


class RouteNode:
    """Node for courier route linked list."""

    def __init__(self, city: str) -> None:
        self.city = city
        self.next: "RouteNode | None" = None

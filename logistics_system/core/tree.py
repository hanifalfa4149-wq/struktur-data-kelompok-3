"""Hierarki gudang."""


class WarehouseNode:
    """Node for warehouse hierarchy tree."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.children: list["WarehouseNode"] = []

    def add_child(self, child: "WarehouseNode") -> None:
        self.children.append(child)

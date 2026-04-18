"""Dictionary stok barang."""


class Inventory:
    """Simple inventory storage using a dictionary."""

    def __init__(self) -> None:
        self.stock: dict[str, int] = {}

    def set_stock(self, item: str, quantity: int) -> None:
        self.stock[item] = quantity

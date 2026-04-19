"""Stack muatan truk (LIFO)."""


class LoadStack:
    """Representasi stack muatan per truk."""

    def __init__(self) -> None:
        """Initialize empty stack."""
        self.items = []

    def push(self, barang_id: str, qty: int) -> None:
        """Push item pair into stack."""
        if qty is None or qty <= 0:
            return
        self.items.append([barang_id, int(qty)])

    def pop(self) -> tuple | None:
        """Pop top item as tuple, or None when empty."""
        if self.is_empty():
            return None
        barang_id, qty = self.items.pop()
        return barang_id, qty

    def peek(self) -> tuple | None:
        """Peek top item as tuple, or None when empty."""
        if self.is_empty():
            return None
        barang_id, qty = self.items[-1]
        return barang_id, qty

    def is_empty(self) -> bool:
        """Check whether stack is empty."""
        return len(self.items) == 0

    def display_stack(self) -> None:
        """Print stack from top to bottom."""
        if self.is_empty():
            print("Stack kosong")
            return

        nomor = 1
        for barang_id, qty in reversed(self.items):
            print(f"{nomor}. {barang_id} x{qty}")
            nomor += 1

    def load_from_list(self, data: list) -> None:
        """Hydrate stack from list pairs."""
        self.items = []
        if not isinstance(data, list):
            return

        for entry in data:
            if isinstance(entry, (list, tuple)) and len(entry) == 2:
                barang_id, qty = entry
                self.items.append([str(barang_id), int(qty)])

    def load_from_dict(self, data: dict) -> None:
        """Compatibility loader required by core conventions."""
        if isinstance(data, list):
            self.load_from_list(data)
            return
        if isinstance(data, dict):
            self.load_from_list(data.get("stack", []))
            return
        self.load_from_list([])

    def to_list(self) -> list:
        """Serialize stack into list of [barang_id, qty]."""
        return [[barang_id, qty] for barang_id, qty in self.items]

    def __repr__(self) -> str:
        """Return debug representation of stack state."""
        return f"LoadStack(size={len(self.items)})"

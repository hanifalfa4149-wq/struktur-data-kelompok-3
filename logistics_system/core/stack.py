"""Stack muatan truk (LIFO)."""


class LoadStack:
    """Representasi stack muatan per truk."""

    def __init__(self) -> None:
        """Inisialisasi stack kosong."""
        self.items = []

    def push(self, barang_id: str, qty: int) -> None:
        """Menambahkan pasangan item ke stack."""
        if qty is None or qty <= 0:
            return
        self.items.append([barang_id, int(qty)])

    def pop(self) -> tuple | None:
        """Mengambil item teratas sebagai tuple, atau None jika kosong."""
        if self.is_empty():
            return None
        barang_id, qty = self.items.pop()
        return barang_id, qty

    def peek(self) -> tuple | None:
        """Melihat item teratas sebagai tuple, atau None jika kosong."""
        if self.is_empty():
            return None
        barang_id, qty = self.items[-1]
        return barang_id, qty

    def is_empty(self) -> bool:
        """Memeriksa apakah stack kosong."""
        return len(self.items) == 0

    def display_stack(self) -> None:
        """Mencetak stack dari atas ke bawah."""
        if self.is_empty():
            print("Stack kosong")
            return

        nomor = 1
        for barang_id, qty in reversed(self.items):
            print(f"{nomor}. {barang_id} x{qty}")
            nomor += 1

    def load_from_list(self, data: list) -> None:
        """Membentuk ulang stack dari pasangan list."""
        self.items = []
        if not isinstance(data, list):
            return

        for entry in data:
            if isinstance(entry, (list, tuple)) and len(entry) == 2:
                barang_id, qty = entry
                self.items.append([str(barang_id), int(qty)])

    def load_from_dict(self, data: dict) -> None:
        """Pemuat kompatibilitas yang dibutuhkan oleh konvensi inti."""
        if isinstance(data, list):
            self.load_from_list(data)
            return
        if isinstance(data, dict):
            self.load_from_list(data.get("stack", []))
            return
        self.load_from_list([])

    def to_list(self) -> list:
        """Menyerialisasi stack ke list [barang_id, qty]."""
        return [[barang_id, qty] for barang_id, qty in self.items]

    def __repr__(self) -> str:
        """Mengembalikan representasi penelusuran dari state stack."""
        return f"LoadStack(size={len(self.items)})"

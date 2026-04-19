"""Manajemen inventaris gudang berbasis dictionary."""


class Inventory:
    """Store stok barang per gudang."""

    def __init__(self) -> None:
        """Initialize empty inventory data."""
        self.data = {}

    def cek_stok(self, gudang_id, barang_id) -> dict | None:
        """Return item record from a warehouse, or None if missing."""
        gudang = self.data.get(gudang_id)
        if gudang is None:
            return None
        return gudang.get(barang_id)

    def kurangi_stok(self, gudang_id, barang_id, qty) -> bool:
        """Reduce stock quantity if available."""
        if qty is None or qty <= 0:
            return False

        barang = self.cek_stok(gudang_id, barang_id)
        if barang is None:
            return False

        stok = barang.get("stok", 0)
        if stok < qty:
            return False

        barang["stok"] = stok - qty
        return True

    def tambah_stok(self, gudang_id, barang_id, qty) -> None:
        """Add stock quantity, creating warehouse/item if needed."""
        if qty is None or qty <= 0:
            return

        gudang = self.data.setdefault(gudang_id, {})
        barang = gudang.setdefault(barang_id, {"nama": barang_id, "stok": 0})
        barang["stok"] = int(barang.get("stok", 0)) + int(qty)

    def tampilkan_inventaris(self, gudang_id) -> None:
        """Print all inventory records for a warehouse."""
        gudang = self.data.get(gudang_id, {})
        if not gudang:
            print("Inventaris kosong")
            return

        for idx, (barang_id, info) in enumerate(gudang.items(), start=1):
            nama = info.get("nama", "")
            stok = info.get("stok", 0)
            print(f"{idx}. {barang_id} - {nama}: {stok}")

    def load_from_dict(self, data) -> None:
        """Hydrate inventory from a dictionary."""
        self.data = {}
        if not isinstance(data, dict):
            return

        for gudang_id, items in data.items():
            if not isinstance(items, dict):
                continue

            self.data[gudang_id] = {}
            for barang_id, info in items.items():
                if not isinstance(info, dict):
                    continue
                self.data[gudang_id][barang_id] = {
                    "nama": info.get("nama", barang_id),
                    "stok": int(info.get("stok", 0)),
                }

    def to_dict(self) -> dict:
        """Return a JSON-safe copy of inventory data."""
        return {
            gudang_id: {
                barang_id: {
                    "nama": info.get("nama", barang_id),
                    "stok": int(info.get("stok", 0)),
                }
                for barang_id, info in items.items()
            }
            for gudang_id, items in self.data.items()
        }

    def __repr__(self) -> str:
        """Return debug representation of inventory state."""
        return f"Inventory(gudang={len(self.data)})"

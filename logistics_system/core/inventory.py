"""Manajemen inventaris gudang berbasis dictionary."""


class Inventory:
    """Menyimpan stok barang per gudang."""

    def __init__(self) -> None:
        """Inisialisasi data inventaris kosong."""
        self.data = {}

    def cek_stok(self, gudang_id, barang_id) -> dict | None:
        """Mengembalikan data barang dari gudang, atau None jika tidak ada."""
        gudang = self.data.get(gudang_id)
        if gudang is None:
            return None
        return gudang.get(barang_id)

    def kurangi_stok(self, gudang_id, barang_id, qty) -> bool:
        """Mengurangi jumlah stok jika tersedia."""
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
        """Menambah jumlah stok, membuat gudang/barang bila diperlukan."""
        if qty is None or qty <= 0:
            return

        gudang = self.data.setdefault(gudang_id, {})
        barang = gudang.setdefault(barang_id, {"nama": barang_id, "stok": 0})
        barang["stok"] = int(barang.get("stok", 0)) + int(qty)

    def tampilkan_inventaris(self, gudang_id) -> None:
        """Mencetak semua data inventaris untuk sebuah gudang."""
        gudang = self.data.get(gudang_id, {})
        if not gudang:
            print("Inventaris kosong")
            return

        for idx, (barang_id, info) in enumerate(gudang.items(), start=1):
            nama = info.get("nama", "")
            stok = info.get("stok", 0)
            print(f"{idx}. {barang_id} - {nama}: {stok}")

    def load_from_dict(self, data) -> None:
        """Membentuk ulang inventaris dari sebuah dictionary."""
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
        """Mengembalikan salinan data inventaris yang aman untuk JSON."""
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
        """Mengembalikan representasi penelusuran dari state inventaris."""
        return f"Inventory(gudang={len(self.data)})"

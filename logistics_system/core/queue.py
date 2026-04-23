"""Antrean truk dermaga muat."""

from collections import deque


class TruckQueue:
    """Queue FIFO untuk antrean truk."""

    def __init__(self) -> None:
        """Inisialisasi queue kosong."""
        self.queue = deque()

    def enqueue(self, plat_nomor: str) -> None:
        """Menambahkan nomor plat truk ke bagian belakang queue."""
        self.queue.append(plat_nomor)

    def dequeue(self) -> str | None:
        """Menghapus dan mengembalikan plat truk pertama, atau None jika kosong."""
        if self.is_empty():
            return None
        return self.queue.popleft()

    def peek(self) -> str | None:
        """Mengembalikan plat truk pertama tanpa menghapusnya."""
        if self.is_empty():
            return None
        return self.queue[0]

    def is_empty(self) -> bool:
        """Memeriksa apakah queue kosong."""
        return len(self.queue) == 0

    def display_queue(self) -> None:
        """Mencetak queue sebagai daftar bernomor."""
        if self.is_empty():
            print("Antrean kosong")
            return

        for idx, plat in enumerate(self.queue, start=1):
            print(f"{idx}. {plat}")

    def load_from_list(self, data: list) -> None:
        """Membentuk ulang queue dari data list."""
        self.queue = deque()
        if not isinstance(data, list):
            return
        for plat in data:
            self.queue.append(str(plat))

    def load_from_dict(self, data: dict) -> None:
        """Pemuat kompatibilitas yang dibutuhkan oleh konvensi inti."""
        if isinstance(data, list):
            self.load_from_list(data)
            return
        if isinstance(data, dict):
            self.load_from_list(data.get("queue", []))
            return
        self.load_from_list([])

    def to_list(self) -> list:
        """Menyerialisasi queue ke list yang aman untuk JSON."""
        return list(self.queue)

    def __repr__(self) -> str:
        """Mengembalikan representasi penelusuran dari state queue."""
        return f"TruckQueue(size={len(self.queue)})"

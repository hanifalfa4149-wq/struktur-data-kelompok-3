"""Peta rute antar kota berbobot dengan BFS."""

from collections import deque


class CityGraph:
    """Graph weighted adjacency list untuk rute kota logistik."""

    def __init__(self) -> None:
        """Inisialisasi graph kota kosong."""
        self.adjacency = {}

    def tambah_rute(self, kota_a, kota_b, jarak) -> None:
        """Menambahkan rute dua arah antara dua kota."""
        if kota_a is None or kota_b is None:
            return

        jarak_int = int(jarak)
        self.adjacency.setdefault(kota_a, [])
        self.adjacency.setdefault(kota_b, [])

        if not any(neighbor == kota_b for neighbor, _ in self.adjacency[kota_a]):
            self.adjacency[kota_a].append((kota_b, jarak_int))
        if not any(neighbor == kota_a for neighbor, _ in self.adjacency[kota_b]):
            self.adjacency[kota_b].append((kota_a, jarak_int))

    def cek_koneksi_langsung(self, kota_a, kota_b) -> bool:
        """Memeriksa apakah kota_a memiliki edge langsung ke kota_b."""
        for neighbor, _ in self.adjacency.get(kota_a, []):
            if neighbor == kota_b:
                return True
        return False

    def cari_jalur(self, kota_a, kota_b) -> list[str] | None:
        """Mencari jalur menggunakan BFS dan mengembalikan list nama kota."""
        if kota_a not in self.adjacency or kota_b not in self.adjacency:
            return None

        queue = deque([(kota_a, [kota_a])])
        visited = {kota_a}

        while queue:
            current, path = queue.popleft()
            if current == kota_b:
                return path

            for neighbor, _ in self.adjacency.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    def tampilkan_peta(self) -> None:
        """Mencetak adjacency list beserta label jarak."""
        if not self.adjacency:
            print("Peta kosong")
            return

        for kota, neighbors in self.adjacency.items():
            if not neighbors:
                print(f"{kota}: -")
                continue
            detail = ", ".join(
                [f"{neighbor} ({jarak} km)" for neighbor, jarak in neighbors]
            )
            print(f"{kota}: {detail}")

    def load_from_dict(self, data: dict) -> None:
        """Membentuk ulang graph dari dictionary adjacency yang sudah terserialisasi."""
        self.adjacency = {}
        if not isinstance(data, dict):
            return

        for kota, neighbors in data.items():
            self.adjacency[kota] = []
            if not isinstance(neighbors, list):
                continue

            for entry in neighbors:
                if isinstance(entry, (list, tuple)) and len(entry) == 2:
                    neighbor, jarak = entry
                    self.adjacency[kota].append((neighbor, int(jarak)))

    def to_dict(self) -> dict:
        """Menyerialisasi data adjacency ke format yang aman untuk JSON."""
        return {
            kota: [[neighbor, jarak] for neighbor, jarak in neighbors]
            for kota, neighbors in self.adjacency.items()
        }

    def __repr__(self) -> str:
        """Mengembalikan representasi penelusuran dari state graph."""
        return f"CityGraph(cities={len(self.adjacency)})"

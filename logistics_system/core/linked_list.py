"""Rute kurir berbasis singly linked list."""


class Node:
    """Single node untuk data paket rute kurir."""

    def __init__(self, paket_id, alamat, penerima):
        """Initialize paket node."""
        self.paket_id = paket_id
        self.alamat = alamat
        self.penerima = penerima
        self.next = None


class CourierRoute:
    """Linked list sederhana untuk antrean pengantaran kurir."""

    def __init__(self) -> None:
        """Initialize empty route."""
        self.head = None
        self.size = 0

    def tambah_paket(self, paket_id, alamat, penerima) -> None:
        """Append a new package node at the tail."""
        new_node = Node(paket_id, alamat, penerima)
        if self.head is None:
            self.head = new_node
            self.size += 1
            return

        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node
        self.size += 1

    def selesai_antar(self) -> dict | None:
        """Remove head package and return it as dict."""
        if self.head is None:
            return None

        delivered = self.head
        self.head = self.head.next
        self.size -= 1
        return {
            "paket_id": delivered.paket_id,
            "alamat": delivered.alamat,
            "penerima": delivered.penerima,
        }

    def sisipkan_paket(self, posisi, paket_id, alamat, penerima) -> None:
        """Insert package node at position, append when position >= size."""
        if posisi <= 0 or self.head is None:
            new_node = Node(paket_id, alamat, penerima)
            new_node.next = self.head
            self.head = new_node
            self.size += 1
            return

        if posisi >= self.size:
            self.tambah_paket(paket_id, alamat, penerima)
            return

        prev = self.head
        current_pos = 0
        while prev is not None and current_pos < posisi - 1:
            prev = prev.next
            current_pos += 1

        new_node = Node(paket_id, alamat, penerima)
        if prev is not None:
            new_node.next = prev.next
            prev.next = new_node
            self.size += 1

    def hapus_paket(self, paket_id) -> bool:
        """Delete first package by paket_id."""
        if self.head is None:
            return False

        if self.head.paket_id == paket_id:
            self.head = self.head.next
            self.size -= 1
            return True

        prev = self.head
        current = self.head.next
        while current is not None:
            if current.paket_id == paket_id:
                prev.next = current.next
                self.size -= 1
                return True
            prev = current
            current = current.next
        return False

    def tampilkan_rute(self) -> None:
        """Print route as numbered list from head to tail."""
        if self.head is None:
            print("Rute kosong")
            return

        idx = 1
        current = self.head
        while current is not None:
            print(
                f"{idx}. {current.paket_id} - " f"{current.alamat} ({current.penerima})"
            )
            idx += 1
            current = current.next

    def load_from_list(self, data: list) -> None:
        """Hydrate route from list of dict packages."""
        self.head = None
        self.size = 0

        if not isinstance(data, list):
            return

        for paket in data:
            if not isinstance(paket, dict):
                continue
            self.tambah_paket(
                paket.get("paket_id", ""),
                paket.get("alamat", ""),
                paket.get("penerima", ""),
            )

    def load_from_dict(self, data: dict) -> None:
        """Compatibility loader required by core conventions."""
        if isinstance(data, list):
            self.load_from_list(data)
            return
        if isinstance(data, dict):
            self.load_from_list(data.get("route", []))
            return
        self.load_from_list([])

    def to_list(self) -> list[dict]:
        """Serialize route into list of package dicts."""
        result = []
        current = self.head
        while current is not None:
            result.append(
                {
                    "paket_id": current.paket_id,
                    "alamat": current.alamat,
                    "penerima": current.penerima,
                }
            )
            current = current.next
        return result

    def __repr__(self) -> str:
        """Return debug representation of route state."""
        return f"CourierRoute(size={self.size})"

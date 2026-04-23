"""Lapisan service yang mengorkestrasi seluruh operasi sistem logistik."""

try:
    from logistics_system.core.graph import CityGraph
    from logistics_system.core.inventory import Inventory
    from logistics_system.core.linked_list import CourierRoute
    from logistics_system.core.queue import TruckQueue
    from logistics_system.core.stack import LoadStack
    from logistics_system.core.tree import WarehouseTree
except ImportError:  # pragma: no cover
    from core.graph import CityGraph
    from core.inventory import Inventory
    from core.linked_list import CourierRoute
    from core.queue import TruckQueue
    from core.stack import LoadStack
    from core.tree import WarehouseTree


class LogisticsService:
    """Koordinator utama untuk operasi lintas struktur data."""

    def __init__(
        self,
        tree: WarehouseTree,
        inventory: Inventory,
        truck_queue: TruckQueue,
        graph: CityGraph,
        active_trucks=None,
        courier_routes=None,
    ):
        """Inisialisasi service dengan dependency yang sudah dibentuk ulang."""
        self.tree = tree
        self.inventory = inventory
        self.truck_queue = truck_queue
        self.graph = graph
        self.active_trucks: dict[str, LoadStack] = active_trucks or {}
        self.courier_routes: dict[str, CourierRoute] = courier_routes or {}

    def cek_stok_tervalidasi(self, gudang_id, barang_id) -> tuple[dict | None, str]:
        """IP#3: validasi gudang via tree lalu cek stok via inventory."""
        node = self.tree.find_node(gudang_id)
        if node is None:
            return None, "Gudang tidak ditemukan"

        item = self.inventory.cek_stok(gudang_id, barang_id)
        if item is None:
            return None, "Barang tidak ditemukan"

        return item, "OK"

    def proses_truk_berikutnya(self) -> tuple[str | None, str]:
        """IP#2: dequeue truk lalu buat stack muatan aktif baru."""
        plat_nomor = self.truck_queue.dequeue()
        if plat_nomor is None:
            return None, "Antrean kosong"

        new_stack = LoadStack()
        self.active_trucks[plat_nomor] = new_stack
        return plat_nomor, f"Truk {plat_nomor} siap muat"

    def muat_barang(
        self, plat_nomor, gudang_id, barang_id, qty: int
    ) -> tuple[bool, str]:
        """Muat barang ke truk aktif setelah validasi stok."""
        if plat_nomor not in self.active_trucks:
            return False, "Truk tidak aktif"

        if qty <= 0:
            return False, "Jumlah muat harus lebih dari 0"

        _, pesan_validasi = self.cek_stok_tervalidasi(gudang_id, barang_id)
        if pesan_validasi != "OK":
            return False, pesan_validasi

        sukses = self.inventory.kurangi_stok(gudang_id, barang_id, qty)
        if not sukses:
            return False, "Stok tidak cukup"

        self.active_trucks[plat_nomor].push(barang_id, qty)
        return True, f"{barang_id} x{qty} berhasil dimuat ke {plat_nomor}"

    def undo_muat(self, plat_nomor, gudang_id) -> tuple[bool, str]:
        """IP#1: undo muatan terakhir dan kembalikan ke stok gudang."""
        if plat_nomor not in self.active_trucks:
            return False, "Truk tidak aktif"

        popped = self.active_trucks[plat_nomor].pop()
        if popped is None:
            return False, "Tidak ada muatan untuk di-undo"

        barang_id, qty = popped
        self.inventory.tambah_stok(gudang_id, barang_id, qty)
        return (
            True,
            f"Undo: {barang_id} x{qty} " f"dikembalikan ke stok {gudang_id}",
        )

    def buat_rute_kurir(self, kurir_id) -> tuple[bool, str]:
        """Buat rute baru untuk kurir jika belum ada."""
        if kurir_id in self.courier_routes:
            return False, "Rute kurir sudah ada"

        self.courier_routes[kurir_id] = CourierRoute()
        return True, f"Rute kurir {kurir_id} berhasil dibuat"

    def tambah_paket_kurir(
        self, kurir_id, paket_id, alamat, penerima
    ) -> tuple[bool, str]:
        """Tambahkan paket ke rute kurir."""
        route = self.courier_routes.get(kurir_id)
        if route is None:
            return False, "Kurir tidak ditemukan"

        route.tambah_paket(paket_id, alamat, penerima)
        return True, f"Paket {paket_id} ditambahkan ke rute {kurir_id}"

    def selesai_antar(self, kurir_id) -> tuple[dict | None, str]:
        """Tandai paket terdepan kurir sebagai selesai diantar."""
        route = self.courier_routes.get(kurir_id)
        if route is None:
            return None, "Kurir tidak ditemukan"

        paket = route.selesai_antar()
        if paket is None:
            return None, "Rute kosong"

        return paket, "Paket berhasil diantar"

    def tampilkan_rute_kurir(self, kurir_id) -> tuple[bool, str]:
        """Tampilkan rute paket untuk kurir tertentu."""
        route = self.courier_routes.get(kurir_id)
        if route is None:
            return False, "Kurir tidak ditemukan"

        route.tampilkan_rute()
        return True, "OK"

    def tampilkan_tree(self) -> None:
        """Passthrough helper untuk menampilkan tree gudang."""
        self.tree.display_tree()

    def tampilkan_inventaris(self, gudang_id) -> None:
        """Passthrough helper untuk menampilkan inventaris gudang."""
        self.inventory.tampilkan_inventaris(gudang_id)

    def tampilkan_antrean(self) -> None:
        """Passthrough helper untuk menampilkan antrean truk."""
        self.truck_queue.display_queue()

    def tampilkan_muatan(self, plat_nomor) -> tuple[bool, str]:
        """Tampilkan muatan stack truk aktif."""
        stack = self.active_trucks.get(plat_nomor)
        if stack is None:
            return False, "Truk tidak aktif"

        stack.display_stack()
        return True, "OK"

    def cari_jalur_kota(self, kota_a, kota_b) -> tuple[list | None, str]:
        """Cari jalur BFS antar dua kota."""
        path = self.graph.cari_jalur(kota_a, kota_b)
        if path is None:
            return None, "Jalur tidak ditemukan"
        return path, "OK"

    def tambah_rute_kota(self, kota_a, kota_b, jarak) -> tuple[bool, str]:
        """Tambah rute dua arah antar kota."""
        try:
            jarak_int = int(jarak)
        except (TypeError, ValueError):
            return False, "Jarak tidak valid"

        if jarak_int <= 0:
            return False, "Jarak tidak valid"

        self.graph.tambah_rute(kota_a, kota_b, jarak_int)
        return True, f"Rute {kota_a} <-> {kota_b} ({jarak_int} km) ditambahkan"

    def tampilkan_peta(self) -> None:
        """Passthrough helper untuk menampilkan peta kota."""
        self.graph.tampilkan_peta()

    def __repr__(self) -> str:
        """Mengembalikan representasi penelusuran dari state service."""
        return (
            "LogisticsService("
            f"active_trucks={len(self.active_trucks)}, "
            f"courier_routes={len(self.courier_routes)}"
            ")"
        )

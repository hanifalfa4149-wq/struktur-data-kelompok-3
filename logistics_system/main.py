"""Entry point CLI sistem logistik."""

import sys

try:
    from .services.logistics import (
        CityGraph,
        CourierRoute,
        Inventory,
        LoadStack,
        LogisticsService,
        TruckQueue,
        WarehouseTree,
    )
    from .storage import load_state, save_state
except ImportError:  # pragma: no cover
    from services.logistics import (
        CityGraph,
        CourierRoute,
        Inventory,
        LoadStack,
        LogisticsService,
        TruckQueue,
        WarehouseTree,
    )
    from storage import load_state, save_state


def _baca_input(prompt: str) -> str | None:
    """Read input safely and return None when invalid."""
    try:
        return input(prompt).strip()
    except Exception:
        return None


def _pause() -> None:
    """Pause screen before returning to menu."""
    try:
        input("\nTekan Enter untuk kembali...")
    except Exception:
        pass


def _hydrate_service() -> LogisticsService:
    """Load persisted state and hydrate all runtime objects."""
    state = load_state("data/seed.json")

    tree = WarehouseTree()
    tree.load_from_dict(state.get("tree", {}))

    inventory = Inventory()
    inventory.load_from_dict(state.get("inventory", {}))

    truck_queue = TruckQueue()
    truck_queue.load_from_list(state.get("queue", []))

    graph = CityGraph()
    graph.load_from_dict(state.get("graph", {}))

    active_trucks = {}
    for plat, data in state.get("active_trucks", {}).items():
        s = LoadStack()
        s.load_from_list(data.get("stack", []))
        active_trucks[plat] = s

    courier_routes = {}
    for kid, data in state.get("courier_routes", {}).items():
        r = CourierRoute()
        r.load_from_list(data)
        courier_routes[kid] = r

    return LogisticsService(
        tree,
        inventory,
        truck_queue,
        graph,
        active_trucks,
        courier_routes,
    )


def menu_hierarki(svc: LogisticsService) -> None:
    """US-01: operasi tree gudang."""
    while True:
        print("\n=== MENU HIERARKI GUDANG ===")
        print("[1] Tampilkan seluruh hierarki")
        print("[2] Tampilkan anak dari node")
        print("[0] Kembali")

        pilihan = _baca_input("Pilih menu: ")
        if pilihan is None:
            print("Input tidak valid, coba lagi.")
            continue

        if pilihan == "0":
            return
        if pilihan == "1":
            svc.tampilkan_tree()
            print("OK")
            _pause()
            continue
        if pilihan == "2":
            node_id = _baca_input("Masukkan node_id: ")
            if not node_id:
                print("Input tidak valid, coba lagi.")
                _pause()
                continue
            children = svc.tree.get_children(node_id)
            if not children:
                print("Tidak ada anak node atau node tidak ditemukan")
            else:
                for idx, child in enumerate(children, start=1):
                    print(f"{idx}. {child['id']} - {child['name']} ({child['type']})")
            print("OK")
            _pause()
            continue

        print("Input tidak valid, coba lagi.")
        _pause()


def menu_inventaris(svc: LogisticsService) -> None:
    """US-02: operasi dictionary inventaris."""
    while True:
        print("\n=== MENU INVENTARIS STOK ===")
        print("[1] Cek stok item")
        print("[2] Tampilkan semua inventaris gudang")
        print("[0] Kembali")

        pilihan = _baca_input("Pilih menu: ")
        if pilihan is None:
            print("Input tidak valid, coba lagi.")
            continue

        if pilihan == "0":
            return
        if pilihan == "1":
            gudang_id = _baca_input("Masukkan gudang_id: ")
            barang_id = _baca_input("Masukkan barang_id: ")
            if not gudang_id or not barang_id:
                print("Input tidak valid, coba lagi.")
                _pause()
                continue
            item, pesan = svc.cek_stok_tervalidasi(gudang_id, barang_id)
            if item is not None:
                print(
                    f"{barang_id} - {item.get('nama', '')}: stok {item.get('stok', 0)}"
                )
            print(pesan)
            _pause()
            continue
        if pilihan == "2":
            gudang_id = _baca_input("Masukkan gudang_id: ")
            if not gudang_id:
                print("Input tidak valid, coba lagi.")
                _pause()
                continue
            svc.tampilkan_inventaris(gudang_id)
            print("OK")
            _pause()
            continue

        print("Input tidak valid, coba lagi.")
        _pause()


def menu_antrean(svc: LogisticsService) -> None:
    """US-03: operasi queue loading dock."""
    while True:
        print("\n=== MENU ANTREAN LOADING DOCK ===")
        print("[1] Daftarkan truk baru")
        print("[2] Lihat antrean saat ini")
        print("[3] Proses truk berikutnya")
        print("[0] Kembali")

        pilihan = _baca_input("Pilih menu: ")
        if pilihan is None:
            print("Input tidak valid, coba lagi.")
            continue

        if pilihan == "0":
            return
        if pilihan == "1":
            plat = _baca_input("Masukkan plat nomor: ")
            if not plat:
                print("Input tidak valid, coba lagi.")
                _pause()
                continue
            svc.truck_queue.enqueue(plat)
            print(f"Truk {plat} berhasil masuk antrean")
            _pause()
            continue
        if pilihan == "2":
            svc.tampilkan_antrean()
            print("OK")
            _pause()
            continue
        if pilihan == "3":
            _, pesan = svc.proses_truk_berikutnya()
            print(pesan)
            _pause()
            continue

        print("Input tidak valid, coba lagi.")
        _pause()


def menu_muat_undo(svc: LogisticsService) -> None:
    """US-04/US-05: stack loading dan undo."""
    while True:
        print("\n=== MENU MUAT BARANG & UNDO ===")
        print("[1] Muat barang ke truk aktif")
        print("[2] Undo muat terakhir")
        print("[3] Lihat muatan truk saat ini")
        print("[0] Kembali")

        pilihan = _baca_input("Pilih menu: ")
        if pilihan is None:
            print("Input tidak valid, coba lagi.")
            continue

        if pilihan == "0":
            return
        if pilihan == "1":
            plat = _baca_input("Masukkan plat nomor: ")
            gudang_id = _baca_input("Masukkan gudang_id: ")
            barang_id = _baca_input("Masukkan barang_id: ")
            qty_raw = _baca_input("Masukkan qty: ")
            try:
                qty = int(qty_raw) if qty_raw is not None else 0
            except Exception:
                print("Input tidak valid, coba lagi.")
                _pause()
                continue

            if not plat or not gudang_id or not barang_id:
                print("Input tidak valid, coba lagi.")
                _pause()
                continue

            _, pesan = svc.muat_barang(plat, gudang_id, barang_id, qty)
            print(pesan)
            _pause()
            continue
        if pilihan == "2":
            plat = _baca_input("Masukkan plat nomor: ")
            gudang_id = _baca_input("Masukkan gudang_id: ")
            if not plat or not gudang_id:
                print("Input tidak valid, coba lagi.")
                _pause()
                continue
            _, pesan = svc.undo_muat(plat, gudang_id)
            print(pesan)
            _pause()
            continue
        if pilihan == "3":
            plat = _baca_input("Masukkan plat nomor: ")
            if not plat:
                print("Input tidak valid, coba lagi.")
                _pause()
                continue
            _, pesan = svc.tampilkan_muatan(plat)
            print(pesan)
            _pause()
            continue

        print("Input tidak valid, coba lagi.")
        _pause()


def menu_kurir(svc: LogisticsService) -> None:
    """US-06: operasi linked list rute kurir."""
    while True:
        print("\n=== MENU RUTE KURIR ===")
        print("[1] Buat rute kurir baru")
        print("[2] Tambah paket ke rute")
        print("[3] Selesai antar paket pertama")
        print("[4] Lihat rute kurir")
        print("[0] Kembali")

        pilihan = _baca_input("Pilih menu: ")
        if pilihan is None:
            print("Input tidak valid, coba lagi.")
            continue

        if pilihan == "0":
            return
        if pilihan == "1":
            kurir_id = _baca_input("Masukkan kurir_id: ")
            if not kurir_id:
                print("Input tidak valid, coba lagi.")
                _pause()
                continue
            _, pesan = svc.buat_rute_kurir(kurir_id)
            print(pesan)
            _pause()
            continue
        if pilihan == "2":
            kurir_id = _baca_input("Masukkan kurir_id: ")
            paket_id = _baca_input("Masukkan paket_id: ")
            alamat = _baca_input("Masukkan alamat: ")
            penerima = _baca_input("Masukkan penerima: ")
            if not kurir_id or not paket_id or not alamat or not penerima:
                print("Input tidak valid, coba lagi.")
                _pause()
                continue
            _, pesan = svc.tambah_paket_kurir(kurir_id, paket_id, alamat, penerima)
            print(pesan)
            _pause()
            continue
        if pilihan == "3":
            kurir_id = _baca_input("Masukkan kurir_id: ")
            if not kurir_id:
                print("Input tidak valid, coba lagi.")
                _pause()
                continue
            paket, pesan = svc.selesai_antar(kurir_id)
            if paket is not None:
                print(
                    f"Paket selesai: {paket['paket_id']} "
                    f"ke {paket['alamat']} ({paket['penerima']})"
                )
            print(pesan)
            _pause()
            continue
        if pilihan == "4":
            kurir_id = _baca_input("Masukkan kurir_id: ")
            if not kurir_id:
                print("Input tidak valid, coba lagi.")
                _pause()
                continue
            _, pesan = svc.tampilkan_rute_kurir(kurir_id)
            print(pesan)
            _pause()
            continue

        print("Input tidak valid, coba lagi.")
        _pause()


def menu_peta(svc: LogisticsService) -> None:
    """US-07: operasi graph distribusi."""
    while True:
        print("\n=== MENU PETA DISTRIBUSI ===")
        print("[1] Cari jalur antara dua kota")
        print("[2] Cek koneksi langsung")
        print("[3] Tambah rute baru")
        print("[4] Tampilkan seluruh peta")
        print("[0] Kembali")

        pilihan = _baca_input("Pilih menu: ")
        if pilihan is None:
            print("Input tidak valid, coba lagi.")
            continue

        if pilihan == "0":
            return
        if pilihan == "1":
            kota_a = _baca_input("Masukkan kota asal: ")
            kota_b = _baca_input("Masukkan kota tujuan: ")
            if not kota_a or not kota_b:
                print("Input tidak valid, coba lagi.")
                _pause()
                continue
            jalur, pesan = svc.cari_jalur_kota(kota_a, kota_b)
            if jalur is not None:
                print(" -> ".join(jalur))
            print(pesan)
            _pause()
            continue
        if pilihan == "2":
            kota_a = _baca_input("Masukkan kota A: ")
            kota_b = _baca_input("Masukkan kota B: ")
            if not kota_a or not kota_b:
                print("Input tidak valid, coba lagi.")
                _pause()
                continue
            connected = svc.graph.cek_koneksi_langsung(kota_a, kota_b)
            if connected:
                print("Terkoneksi langsung")
            else:
                print("Tidak terkoneksi langsung")
            print("OK")
            _pause()
            continue
        if pilihan == "3":
            kota_a = _baca_input("Masukkan kota A: ")
            kota_b = _baca_input("Masukkan kota B: ")
            jarak_raw = _baca_input("Masukkan jarak (km): ")
            if not kota_a or not kota_b:
                print("Input tidak valid, coba lagi.")
                _pause()
                continue
            try:
                jarak = int(jarak_raw) if jarak_raw is not None else 0
            except Exception:
                print("Input tidak valid, coba lagi.")
                _pause()
                continue
            _, pesan = svc.tambah_rute_kota(kota_a, kota_b, jarak)
            print(pesan)
            _pause()
            continue
        if pilihan == "4":
            svc.tampilkan_peta()
            print("OK")
            _pause()
            continue

        print("Input tidak valid, coba lagi.")
        _pause()


def main() -> None:
    """Run full CLI menu loop."""
    svc = _hydrate_service()

    while True:
        print("\n==========================================")
        print("     SISTEM LOGISTIK - MENU UTAMA")
        print("==========================================")
        print("[1] Hierarki Gudang")
        print("[2] Inventaris Stok")
        print("[3] Antrean Loading Dock")
        print("[4] Muat Barang & Undo")
        print("[5] Rute Kurir")
        print("[6] Peta Distribusi")
        print("[0] Simpan & Keluar")

        pilihan = _baca_input("Pilih menu: ")
        if pilihan is None:
            print("Input tidak valid, coba lagi.")
            continue

        if pilihan == "1":
            menu_hierarki(svc)
            continue
        if pilihan == "2":
            menu_inventaris(svc)
            continue
        if pilihan == "3":
            menu_antrean(svc)
            continue
        if pilihan == "4":
            menu_muat_undo(svc)
            continue
        if pilihan == "5":
            menu_kurir(svc)
            continue
        if pilihan == "6":
            menu_peta(svc)
            continue
        if pilihan == "0":
            save_state(
                svc.tree,
                svc.inventory,
                svc.truck_queue,
                svc.active_trucks,
                svc.courier_routes,
                svc.graph,
            )
            print("State tersimpan. Sampai jumpa!")
            sys.exit(0)

        print("Input tidak valid, coba lagi.")


if __name__ == "__main__":
    main()

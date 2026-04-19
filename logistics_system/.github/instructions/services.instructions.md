---
applyTo: "services/**/*.py"
---

## Rules for services/logistics.py

### Imports

- This is the ONLY file in the project allowed to import from core/
- Import all 6 core classes at the top of the file
- Also import storage if needed for auto-save hooks

### Class Structure

LogisticsService takes these constructor params:

- tree: WarehouseTree
- inventory: Inventory
- truck_queue: TruckQueue
- graph: CityGraph
- active_trucks: dict[str, LoadStack] = {} (plat_nomor → LoadStack)
- courier_routes: dict[str, CourierRoute] = {} (kurir_id → CourierRoute)

### Return Convention

All methods that can fail must return: `(result, message)` tuple

- Success: `(True, "pesan sukses")` or `(data, "OK")`
- Failure: `(False, "pesan error")` or `(None, "pesan error")`
- Messages must be in Bahasa Indonesia

### Integration Point Implementation Order

**IP#2 — proses_truk_berikutnya():**

1. Call truck_queue.dequeue() → get plat_nomor
2. If None → return (None, "Antrean kosong")
3. Create new LoadStack() instance
4. Register: self.active_trucks[plat_nomor] = new_stack
5. Return (plat_nomor, "Truk {plat} siap muat")

**muat_barang(plat, gudang_id, barang_id, qty):**

1. Check plat in self.active_trucks → if not: return (False, "Truk tidak aktif")
2. Call IP#3: cek_stok_tervalidasi(gudang_id, barang_id) → validate first
3. Call inventory.kurangi_stok() → if False: return (False, "Stok tidak cukup")
4. Call active_trucks[plat].push(barang_id, qty)
5. Return (True, "BRG-XXX x{qty} berhasil dimuat ke {plat}")

**IP#1 — undo_muat(plat, gudang_id):**

1. Check plat in self.active_trucks → if not: return (False, "Truk tidak aktif")
2. Call active_trucks[plat].pop() → if None: return (False, "Tidak ada muatan untuk di-undo")
3. Call inventory.tambah_stok(gudang_id, barang_id, qty) — restore stock
4. Return (True, "Undo: {barang_id} x{qty} dikembalikan ke stok {gudang_id}")

**IP#3 — cek_stok_tervalidasi(gudang_id, barang_id):**

1. Call tree.find_node(gudang_id) → if None: return (None, "Gudang tidak ditemukan")
2. Call inventory.cek_stok(gudang_id, barang_id) → if None: return (None, "Barang tidak ditemukan")
3. Return (item_dict, "OK")

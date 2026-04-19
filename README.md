# 🚚 Sistem Backend Logistik Terintegrasi

> Capstone Project — Mata Kuliah Struktur Data  
> Python 3.x · Pure Stdlib · CLI Application

Simulasi sistem backend operasional perusahaan logistik (seperti JNE / SiCepat) yang mengimplementasikan **6 struktur data fundamental** secara terintegrasi dalam satu aplikasi CLI yang kohesif.

---

## 📋 Daftar Isi

- [Tentang Project](#tentang-project)
- [Struktur Data yang Diimplementasi](#struktur-data-yang-diimplementasi)
- [Arsitektur Sistem](#arsitektur-sistem)
- [Struktur Folder](#struktur-folder)
- [Cara Menjalankan](#cara-menjalankan)
- [Panduan Penggunaan CLI](#panduan-penggunaan-cli)
- [Data & ID Referensi](#data--id-referensi)
- [Alur Sistem End-to-End](#alur-sistem-end-to-end)
- [Integration Points](#integration-points)

---

## Tentang Project

Project ini mensimulasikan operasi internal perusahaan logistik — mulai dari manajemen hierarki gudang, kontrol inventaris, operasi loading dock truk, hingga manajemen rute kurir dan peta distribusi antar kota.

**Tujuan utama:** mengimplementasikan 6 struktur data bukan sebagai latihan terpisah, melainkan sebagai modul yang saling terintegrasi dan mencerminkan ketergantungan dunia nyata.

| | |
|---|---|
| **Tipe** | CLI Backend Application |
| **Bahasa** | Python 3.x (pure stdlib) |
| **Persistensi** | JSON (`data/seed.json`) |
| **Interface** | Command Line Interface |

---

## Struktur Data yang Diimplementasi

| Modul | Struktur Data | Kelas | Kegunaan |
|---|---|---|---|
| `core/tree.py` | N-ary Tree | `WarehouseTree` | Hierarki gudang (pusat → regional → gudang) |
| `core/inventory.py` | Dictionary / Hash Table | `Inventory` | Stok barang per gudang, O(1) lookup |
| `core/queue.py` | Queue (FIFO) | `TruckQueue` | Antrean truk di loading dock |
| `core/stack.py` | Stack (LIFO) | `LoadStack` | Riwayat muat barang + fitur undo |
| `core/linked_list.py` | Singly Linked List | `CourierRoute` | Rute pengiriman kurir berurutan |
| `core/graph.py` | Weighted Adjacency List | `CityGraph` | Peta distribusi antar kota + BFS pathfinding |

---

## Arsitektur Sistem

```
main.py
  └── services/logistics.py        ← satu-satunya orchestrator
        ├── core/tree.py
        ├── core/inventory.py
        ├── core/queue.py
        ├── core/stack.py
        ├── core/linked_list.py
        └── core/graph.py

storage.py  ← cross-cutting, dipanggil main.py & logistics.py
data/seed.json  ← state persistence
```

### Aturan Arsitektur (Non-Negotiable)

- `core/` modules bersifat **self-contained** — zero cross-imports antar file core
- Semua logika lintas modul ada **eksklusif** di `services/logistics.py`
- `main.py` hanya memanggil `services/` dan `storage` — tidak pernah langsung ke `core/`

---

## Struktur Folder

```
logistics_system/
├── main.py                   # Entry point, CLI menu loop
├── storage.py                # Save/load state ke JSON
├── ARCHITECTURE.md           # Dokumentasi arsitektur teknis
├── core/
│   ├── __init__.py
│   ├── tree.py               # N-ary Tree — WarehouseTree
│   ├── inventory.py          # Dictionary — Inventory
│   ├── queue.py              # Queue FIFO — TruckQueue
│   ├── stack.py              # Stack LIFO — LoadStack
│   ├── linked_list.py        # Singly Linked List — CourierRoute
│   └── graph.py              # Weighted Graph + BFS — CityGraph
├── services/
│   ├── __init__.py
│   └── logistics.py          # Orchestrator semua cross-module logic
├── data/
│   └── seed.json             # Initial + runtime state data
└── .github/
    ├── copilot-instructions.md
    └── instructions/
        ├── core.instructions.md
        └── services.instructions.md
```

---

## Cara Menjalankan

**Requirement:** Python 3.10 atau lebih baru (untuk `X | Y` type hints).

```bash
# Clone / buka folder project
cd logistics_system

# Jalankan aplikasi
python main.py
```

Tidak ada dependency eksternal. Semua berjalan dengan Python stdlib.

Saat pertama dijalankan, aplikasi memuat data dari `data/seed.json` secara otomatis. State disimpan kembali ke file yang sama saat memilih **Simpan & Keluar**.

---

## Panduan Penggunaan CLI

Saat aplikasi berjalan, akan muncul menu utama:

```
==========================================
     SISTEM LOGISTIK — MENU UTAMA
==========================================
  [1] Hierarki Gudang
  [2] Inventaris Stok
  [3] Antrean Loading Dock
  [4] Muat Barang & Undo
  [5] Rute Kurir
  [6] Peta Distribusi
  [0] Simpan & Keluar
```

---

### Menu 1 — Hierarki Gudang (Tree)

Menampilkan struktur organisasi gudang dari pusat hingga cabang.

```
[1] Tampilkan seluruh hierarki
[2] Tampilkan anak dari node tertentu
[0] Kembali
```

**Contoh penggunaan:**
```
Pilih menu: 1

Kantor Pusat
  +-- Regional Barat
  |     +-- Gudang Jakarta
  |     +-- Gudang Bandung
  +-- Regional Timur
  |     +-- Gudang Surabaya
  |     +-- Gudang Malang
  +-- Regional Tengah
        +-- Gudang Semarang
```

Input yang bisa digunakan untuk menu [2]: `PUSAT`, `REG-TIMUR`, `REG-BARAT`, `REG-TENGAH`, `GDG-SBY`, dll.

---

### Menu 2 — Inventaris Stok (Dictionary)

Cek dan tampilkan stok barang di gudang tertentu. Lookup berjalan O(1).

```
[1] Cek stok item tertentu
[2] Tampilkan semua inventaris gudang
[0] Kembali
```

**Contoh penggunaan:**
```
Pilih menu: 1
Masukkan Gudang ID: GDG-SBY
Masukkan Barang ID: BRG-001

BRG-001 - Laptop ASUS VivoBook: 30 unit
```

---

### Menu 3 — Antrean Loading Dock (Queue)

Manajemen antrean truk yang akan memuat barang. Sistem menggunakan FIFO — truk yang datang lebih awal dilayani lebih dulu.

```
[1] Daftarkan truk baru ke antrean
[2] Lihat antrean saat ini
[3] Proses truk berikutnya (dequeue → aktifkan loading)
[0] Kembali
```

**Contoh penggunaan:**
```
Pilih menu: 1
Masukkan plat nomor truk: B-9999-XY
→ Truk B-9999-XY berhasil masuk antrean.

Pilih menu: 3
→ Truk B-1234-CD siap muat. Stack loading aktif.
```

> **Catatan:** Data awal sudah memiliki 2 truk dalam antrean: `B-1234-CD` dan `D-5678-GH`.

---

### Menu 4 — Muat Barang & Undo (Stack)

Setiap truk aktif memiliki stack muatan sendiri. Fitur undo mengembalikan stok ke gudang secara otomatis.

```
[1] Muat barang ke truk aktif
[2] Undo muat terakhir
[3] Lihat muatan truk saat ini
[0] Kembali
```

**Contoh muat barang:**
```
Plat nomor truk: N-9999-ZZ
Gudang ID      : GDG-SBY
Barang ID      : BRG-001
Jumlah (qty)   : 5

→ BRG-001 x5 berhasil dimuat ke N-9999-ZZ.
→ Stok GDG-SBY/BRG-001: 30 → 25
```

**Contoh undo:**
```
Plat nomor truk: N-9999-ZZ
Gudang ID      : GDG-SBY

→ Undo: BRG-001 x5 dikembalikan ke stok GDG-SBY.
→ Stok GDG-SBY/BRG-001: 25 → 30 (restored)
```

> **Catatan:** Data awal sudah memiliki 1 truk aktif (`N-9999-ZZ`) dengan 2 item di stack — bisa langsung test undo.

---

### Menu 5 — Rute Kurir (Linked List)

Manajemen rute pengiriman kurir sebagai singly linked list berurutan.

```
[1] Buat rute kurir baru
[2] Tambah paket ke rute
[3] Selesai antar (hapus paket pertama)
[4] Lihat rute kurir
[0] Kembali
```

**Contoh tampilkan rute:**
```
Kurir ID: KUR-01

Rute Pengiriman KUR-01:
1. PKT-001 → Jl. Pemuda No. 12, Surabaya  (Penerima: Budi Santoso)
2. PKT-002 → Jl. Raya Darmo No. 45, Surabaya  (Penerima: Ani Wijaya)
3. PKT-003 → Jl. Ahmad Yani No. 88, Surabaya  (Penerima: Citra Dewi)
```

**Contoh selesai antar:**
```
Kurir ID: KUR-01
→ Pengiriman selesai: PKT-001 ke Budi Santoso dinyatakan terkirim.
→ Rute tersisa: 2 paket.
```

> **Catatan:** Data awal sudah memiliki rute untuk `KUR-01` (3 paket) dan `KUR-02` (2 paket).

---

### Menu 6 — Peta Distribusi (Graph)

Peta koneksi antar kota menggunakan weighted adjacency list. Path finding menggunakan BFS.

```
[1] Cari jalur antara dua kota
[2] Cek koneksi langsung
[3] Tambah rute baru
[4] Tampilkan seluruh peta
[0] Kembali
```

**Contoh cari jalur:**
```
Kota asal  : Surabaya
Kota tujuan: Jakarta

→ Jalur ditemukan: Surabaya → Semarang → Jakarta
→ Total jarak: 762 km
```

**Contoh tampilkan peta:**
```
Jakarta    → Bandung (150 km), Semarang (450 km)
Semarang   → Jakarta (450 km), Surabaya (312 km), Yogyakarta (115 km)
Surabaya   → Semarang (312 km), Malang (90 km), Banyuwangi (260 km)
Bandung    → Jakarta (150 km), Yogyakarta (310 km)
Malang     → Surabaya (90 km)
Yogyakarta → Semarang (115 km), Bandung (310 km)
Banyuwangi → Surabaya (260 km)
```

---

## Data & ID Referensi

### Gudang & Regional

| ID | Nama | Tipe |
|---|---|---|
| `PUSAT` | Kantor Pusat | pusat |
| `REG-TIMUR` | Regional Timur | regional |
| `REG-BARAT` | Regional Barat | regional |
| `REG-TENGAH` | Regional Tengah | regional |
| `GDG-SBY` | Gudang Surabaya | gudang |
| `GDG-MLG` | Gudang Malang | gudang |
| `GDG-JKT` | Gudang Jakarta | gudang |
| `GDG-BDG` | Gudang Bandung | gudang |
| `GDG-SMG` | Gudang Semarang | gudang |

### Barang (Inventory)

| ID | Nama Barang | SBY | MLG | JKT | BDG | SMG |
|---|---|:---:|:---:|:---:|:---:|:---:|
| `BRG-001` | Laptop ASUS VivoBook | 30 | 15 | 50 | - | - |
| `BRG-002` | Mouse Wireless Logitech | 150 | - | 200 | - | 120 |
| `BRG-003` | Keyboard Mechanical Rexus | 75 | - | - | 55 | - |
| `BRG-004` | Monitor LG 24 inch | 20 | - | - | - | - |
| `BRG-005` | Headset Gaming HyperX | 60 | - | - | - | - |
| `BRG-006` | Webcam Logitech C920 | - | 45 | - | 30 | - |
| `BRG-007` | SSD External Samsung 1TB | - | 90 | - | - | 65 |
| `BRG-008` | Printer Canon PIXMA | - | - | 25 | - | - |
| `BRG-009` | Router TP-Link Archer | - | - | 40 | - | 35 |
| `BRG-010` | UPS APC 650VA | - | - | 18 | - | - |
| `BRG-011` | Speaker Bluetooth JBL | - | - | - | 80 | - |
| `BRG-012` | Flash Disk Sandisk 64GB | - | - | - | - | 300 |

### Truk & Kurir

| ID | Tipe | Status Awal |
|---|---|---|
| `B-1234-CD` | Truk | Dalam antrean (posisi 1) |
| `D-5678-GH` | Truk | Dalam antrean (posisi 2) |
| `N-9999-ZZ` | Truk | Aktif loading (stack: BRG-002×10, BRG-001×2) |
| `KUR-01` | Kurir | Aktif — 3 paket (PKT-001, PKT-002, PKT-003) |
| `KUR-02` | Kurir | Aktif — 2 paket (PKT-004, PKT-005) |

### Jalur BFS yang Valid untuk Testing

| Dari | Ke | Jalur |
|---|---|---|
| Surabaya | Jakarta | Surabaya → Semarang → Jakarta |
| Malang | Bandung | Malang → Surabaya → Semarang → Jakarta → Bandung |
| Banyuwangi | Yogyakarta | Banyuwangi → Surabaya → Semarang → Yogyakarta |
| Malang | Banyuwangi | Tidak ada jalur langsung — test return None |

---

## Alur Sistem End-to-End

Berikut adalah user journey lengkap yang menggunakan semua 6 struktur data secara berurutan:

```
[1] TREE     Admin melihat gudang di Regional Timur
             → display_tree('REG-TIMUR')
             → Output: Gudang Surabaya, Gudang Malang

[2] DICT     Kepala Gudang cek stok Laptop di GDG-SBY
             → cek_stok('GDG-SBY', 'BRG-001')
             → Output: Laptop ASUS VivoBook — 30 unit

[3] QUEUE    Sopir B-1234-CD masuk antrean loading dock
             → enqueue('B-1234-CD')
             → Queue: [B-1234-CD]

[4] QUEUE    System memproses truk berikutnya          ← Integration Point #2
    + STACK  → dequeue() → 'B-1234-CD'
             → LoadStack baru dibuat untuk B-1234-CD

[5] STACK    Sopir muat BRG-001 x5                     ← Integration Point #3
    + DICT   → tree.find_node('GDG-SBY') ✓ (validasi)
             → inventory.kurangi_stok('GDG-SBY', 'BRG-001', 5)
             → stack.push('BRG-001', 5)
             → Stok: 30 → 25

[6] STACK    Sopir salah, undo muat terakhir            ← Integration Point #1
    + DICT   → stack.pop() → ('BRG-001', 5)
             → inventory.tambah_stok('GDG-SBY', 'BRG-001', 5)
             → Stok: 25 → 30 (restored)

[7] GRAPH    Manajer cek jalur Surabaya → Jakarta
             → BFS: Surabaya → Semarang → Jakarta
             → Total: 762 km

[8] LL       Kurir KUR-01 selesai antar paket pertama
             → selesai_antar('KUR-01')
             → PKT-001 dihapus dari head linked list
             → Sisa rute: PKT-002 → PKT-003
```

---

## Integration Points

Tiga titik integrasi antar modul — semuanya dimediasi eksklusif oleh `services/logistics.py`:

### IP#1 — Stack ↔ Inventory (Undo Load)
```
User: "Undo muat terakhir"
  → logistics.undo_muat(plat, gudang_id)
      → stack.pop()              # ambil (barang_id, qty)
      → inventory.tambah_stok()  # kembalikan stok
```

### IP#2 — Queue ↔ Stack (Truck Starts Loading)
```
User: "Proses truk berikutnya"
  → logistics.proses_truk_berikutnya()
      → queue.dequeue()          # ambil plat_nomor
      → new LoadStack()          # buat stack baru untuk truk ini
      → active_trucks[plat] = stack
```

### IP#3 — Tree ↔ Inventory (Warehouse Validation)
```
User: operasi inventory apapun
  → logistics.cek_stok_tervalidasi(gudang_id, barang_id)
      → tree.find_node(gudang_id)   # validasi gudang exist
      → inventory.cek_stok()        # baru boleh akses stok
```

---

*Sistem Logistik Terintegrasi — Capstone Mata Kuliah Struktur Data*

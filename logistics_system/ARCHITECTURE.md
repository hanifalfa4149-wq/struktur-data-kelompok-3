# Architecture — Integrated Logistics Backend System

## Dependency Graph

main.py
└── services/logistics.py
├── core/tree.py
├── core/inventory.py
├── core/queue.py
├── core/stack.py
├── core/linked_list.py
└── core/graph.py
storage.py  ← imported by main.py AND logistics.py
data/seed.json ← read/written by storage.py

## Forbidden Dependencies — CI Should Reject These
- core/X.py importing core/Y.py
- main.py importing anything from core/
- core/*.py importing from services/

## Startup Sequence
1. main.py calls storage.load_state("data/seed.json")
2. Hydrate 6 objects from returned dict
3. Instantiate LogisticsService with all 6 objects
4. Enter CLI menu loop

## Shutdown Sequence
1. User selects [0] Keluar
2. main.py calls storage.save_state() with all live objects
3. Print confirmation, exit

## Full End-to-End User Journey (all 6 DS exercised)
| Step | Actor         | Action                              | DS Used       |
|------|---------------|-------------------------------------|---------------|
| 1    | Admin         | Tampilkan gudang Regional Timur     | Tree          |
| 2    | Kepala Gudang | Cek stok Laptop di GDG-SBY          | Dictionary    |
| 3    | Sopir         | Masuk antrean: B-1234-CD            | Queue         |
| 4    | System        | Proses truk berikutnya              | Queue + Stack |
| 5    | Sopir         | Muat BRG-001 x5                     | Stack + Dict  |
| 6    | Sopir         | Undo muat terakhir                  | Stack + Dict  |
| 7    | Manajer       | Cari jalur Surabaya → Jakarta       | Graph (BFS)   |
| 8    | Kurir         | Selesai antar paket pertama         | Linked List   |

## Key Invariants (must always hold)
- stack.pop() and inventory.tambah_stok() are ATOMIC — both happen in one logistics.py call
- A truck cannot load items without first being dequeued from TruckQueue
- No inventory operation runs on a gudang_id that doesn't exist in WarehouseTree
- JSON state saved on exit must produce identical system state when reloaded

## State Schema (data/seed.json extended at runtime)
```json
{
  "tree": { ...nested tree... },
  "inventory": { "GDG-SBY": { "BRG-001": { "nama": "Laptop", "stok": 30 } } },
  "graph": { "Jakarta": [["Bandung", 150]] },
  "queue": ["B-1234-CD"],
  "active_trucks": { "B-1234-CD": { "stack": [["BRG-001", 5]] } },
  "courier_routes": { "KUR-01": [{ "paket_id": "PKT-001", "alamat": "...", "penerima": "..." }] }
}
```


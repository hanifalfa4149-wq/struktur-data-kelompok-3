---
applyTo: "core/**/*.py"
---

## Rules for All core/ Modules

### Isolation

- ZERO imports from other core/ files — this is non-negotiable
- Only allowed imports: Python stdlib (json, collections.deque for queue only)
- Each class must be fully functional in isolation

### Required Methods on Every Class

Every core class must implement these 3 methods in addition to its own:

- `load_from_dict(self, data: dict) -> None` — hydrate from JSON-parsed dict
- `to_dict(self) -> dict` OR `to_list(self) -> list` — serialize to JSON-safe format
- `__repr__(self) -> str` — useful debug string showing internal state

### Implementation Rules per Module

**tree.py — WarehouseTree**

- Internal storage: flat dict `self.nodes = {}` mapping node_id → node_dict
- Node dict shape: `{ "id": str, "name": str, "type": str, "children": [child_ids] }`
- `self.root_id = None`
- find_node() must be O(1) via dict lookup, NOT recursive search
- display_tree() uses recursive DFS with indentation prefix "+--"
- load_from_dict() parses nested JSON tree into flat self.nodes

**inventory.py — Inventory**

- Internal: `self.data = {}` nested dict: `{ gudang_id: { barang_id: { nama, stok } } }`
- cek_stok() must be O(1) — two dict lookups, no iteration
- kurangi_stok() returns False (not exception) if stok insufficient or item missing
- tambah_stok() creates item entry if it doesn't exist yet

**queue.py — TruckQueue**

- Use `collections.deque` internally as `self.queue`
- enqueue() = deque.append(), dequeue() = deque.popleft()
- dequeue() returns None if empty, never raises exception
- load_from_list() / to_list() for JSON serialization

**stack.py — LoadStack**

- Internal: `self.items = []` — plain Python list used as stack
- push() = list.append(), pop() = list.pop() wrapped in class methods
- Each truck gets its own LoadStack instance (managed by logistics.py)
- pop() returns None if empty, never raises exception
- Items stored as tuples: (barang_id: str, qty: int)

**linked_list.py — Node + CourierRoute**

- Manual Node class: `self.paket_id`, `self.alamat`, `self.penerima`, `self.next = None`
- CourierRoute: `self.head = None`, `self.size = 0`
- tambah_paket() appends to tail — traverse to end
- selesai_antar() removes head and returns its data as dict
- sisipkan_paket(posisi): 0 = insert at head, >= size = append to tail
- hapus_paket(paket_id) traverses list, returns False if not found

**graph.py — CityGraph**

- Internal: `self.adjacency = {}` → `{ kota: [(neighbor, jarak_km), ...] }`
- tambah_rute() always adds bidirectional edges
- cari_jalur() uses BFS — returns list of city name strings or None
- cek_koneksi_langsung() checks direct edge only, NOT transitive
- BFS must track visited nodes to avoid infinite loops

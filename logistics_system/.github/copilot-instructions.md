# Integrated Logistics Backend System

# Capstone Project — Mata Kuliah Struktur Data

## Project Identity

- Type: Python 3.x CLI application, pure stdlib only
- Purpose: Simulate logistics company backend operations (JNE/SiCepat)
- Interface: Command Line Interface only — no web, no GUI, no REST API
- Persistence: JSON files only (data/seed.json + storage.py)

## Hard Constraints — Never Violate

- NO external data structure libraries (no sortedcontainers, networkx, etc.)
- collections.deque is the ONLY allowed built-in collection (Queue only)
- All 6 data structures must be implemented from scratch as classes
- core/ modules have ZERO cross-imports between each other
- All cross-module logic lives EXCLUSIVELY in services/logistics.py
- main.py only imports from services/ and storage — never from core/ directly
- No SQL, no databases — JSON persistence only

## Module → Data Structure Mapping

- core/tree.py → N-ary Tree (class: WarehouseTree)
- core/inventory.py → Dictionary / Hash Table (class: Inventory)
- core/queue.py → Queue FIFO (class: TruckQueue)
- core/stack.py → Stack LIFO (class: LoadStack)
- core/linked_list.py → Singly Linked List (class: Node, CourierRoute)
- core/graph.py → Weighted Adjacency List + BFS (class: CityGraph)

## 3 Integration Points — All mediated by services/logistics.py

- IP#1 Undo Load: stack.pop() → inventory.tambah_stok()
- IP#2 Process Truck: queue.dequeue() → create new LoadStack instance
- IP#3 Validate Gudang: tree.find_node() → inventory.cek_stok()

## Dependency Direction (strictly one-way)

main.py → services/logistics.py → core/\*
storage.py is cross-cutting — callable from main.py and logistics.py

## Code Style

- User-facing strings: Bahasa Indonesia
- Code identifiers: English or Bahasa Indonesia snake_case (follow existing pattern)
- Classes: PascalCase
- Constants: UPPER_SNAKE_CASE
- Every public method must have a docstring
- Methods that can fail: return tuple (bool, str) → (success, message)
- Never crash on bad user input — always validate and return to menu

## Key Domain IDs

- Warehouse IDs: GDG-SBY, GDG-JKT, GDG-BDG, GDG-MLG, GDG-SMG
- Regional IDs: REG-TIMUR, REG-BARAT, REG-TENGAH
- Root ID: PUSAT
- Item IDs: BRG-001 (Laptop), BRG-002 (Mouse), BRG-003 (Keyboard)
- Truck plates: string format e.g. B-1234-CD
- Courier IDs: KUR-01, KUR-02, etc.

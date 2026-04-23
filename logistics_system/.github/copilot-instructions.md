## Web Enhancement Layer (tambahan, tidak mengubah core)

### Stack Tambahan

- Backend API : FastAPI (Python) — di folder api/
- Frontend : Vanilla HTML/CSS/JS — di folder web/
- Database : Supabase (PostgreSQL)
- Deploy : Vercel (static FE + Python serverless functions)

### Arsitektur Request

- Read operations : FE → Supabase JS SDK langsung
- Write/mutating : FE → FastAPI (api/) → Supabase → return result
- Core logic : FastAPI memanggil services/logistics.py (unchanged)

### Supabase Tables

- warehouse_nodes : tree hierarchy (id, name, type, parent_id)
- inventory_items : stok per gudang (gudang_id, barang_id, nama, stok)
- truck_queue : antrean truk (id, plat_nomor, joined_at)
- active_truck_loads : stack per truk (plat_nomor, barang_id, qty, loaded_at)
- courier_packages : rute kurir (kurir_id, paket_id, alamat, penerima, urutan)
- city_routes : graph edges (kota_a, kota_b, jarak_km)

### Rules untuk api/ folder

- Setiap route file hanya boleh import dari services/ dan db.py
- db.py adalah satu-satunya file yang tau tentang Supabase
- Semua endpoint return format: { "success": bool, "message": str, "data": any }
- Load state dari Supabase di awal setiap request (stateless per request)
- Gunakan os.environ untuk semua credentials — never hardcode

### Rules untuk web/ folder

- Vanilla JS only — no frameworks, no npm, no bundler
- Semua fetch ke API di-centralize di js/api.js
- Semua Supabase read langsung di-centralize di js/supabase.js
- Satu JS file per modul (tree.js, inventory.js, dst)
- SUPABASE_URL dan SUPABASE_ANON_KEY boleh di FE (public key)
- SUPABASE_SERVICE_KEY tidak boleh pernah ada di FE

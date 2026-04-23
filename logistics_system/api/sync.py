"""Persistence helpers to sync in-memory state back to Supabase."""

from datetime import datetime, timedelta, timezone

from supabase import Client


def sync_inventory(supabase: Client, inventory) -> None:
    """Upsert inventory rows from inventory.to_dict()."""
    rows: list[dict] = []
    inventory_dict = inventory.to_dict()

    for gudang_id, items in inventory_dict.items():
        for barang_id, info in items.items():
            rows.append(
                {
                    "gudang_id": gudang_id,
                    "barang_id": barang_id,
                    "nama": info.get("nama", barang_id),
                    "stok": int(info.get("stok", 0)),
                }
            )

    if rows:
        supabase.table("inventory_items").upsert(
            rows, on_conflict="gudang_id,barang_id"
        ).execute()


def sync_truck_queue(supabase: Client, truck_queue) -> None:
    """Replace all truck_queue rows with the latest ordered queue snapshot."""
    supabase.table("truck_queue").delete().neq("id", 0).execute()

    queue_rows = [{"plat_nomor": plat} for plat in truck_queue.to_list()]
    if queue_rows:
        supabase.table("truck_queue").insert(queue_rows).execute()


def sync_active_trucks(supabase: Client, active_trucks: dict) -> None:
    """Replace truck load rows while preserving stack order."""
    now = datetime.now(timezone.utc)

    for plat_nomor, stack_obj in active_trucks.items():
        supabase.table("active_truck_loads").delete().eq(
            "plat_nomor", plat_nomor
        ).execute()

        rows: list[dict] = []
        for index, item in enumerate(stack_obj.to_list()):
            if not isinstance(item, (list, tuple)) or len(item) != 2:
                continue
            barang_id, qty = item
            loaded_at = (now + timedelta(milliseconds=index)).isoformat()
            rows.append(
                {
                    "plat_nomor": plat_nomor,
                    "barang_id": str(barang_id),
                    "qty": int(qty),
                    "loaded_at": loaded_at,
                }
            )

        if rows:
            supabase.table("active_truck_loads").insert(rows).execute()


def sync_courier_routes(supabase: Client, courier_routes: dict) -> None:
    """Replace courier rows while preserving urutan order."""
    for kurir_id, route in courier_routes.items():
        delete_query = supabase.table("courier_packages").delete()
        delete_query.eq("kurir_id", kurir_id).execute()

        rows: list[dict] = []
        for index, package in enumerate(route.to_list(), start=1):
            rows.append(
                {
                    "kurir_id": kurir_id,
                    "paket_id": package.get("paket_id", ""),
                    "alamat": package.get("alamat", ""),
                    "penerima": package.get("penerima", ""),
                    "urutan": index,
                }
            )

        if rows:
            supabase.table("courier_packages").insert(rows).execute()


def sync_graph(supabase: Client, graph) -> None:
    """Upsert unique city route edges from graph.to_dict()."""
    graph_dict = graph.to_dict()
    rows: list[dict] = []
    seen_edges: set[tuple[str, str]] = set()

    for kota_a, neighbors in graph_dict.items():
        for neighbor in neighbors:
            if not isinstance(neighbor, (list, tuple)) or len(neighbor) != 2:
                continue
            kota_b, jarak_km = neighbor
            a = str(kota_a)
            b = str(kota_b)
            edge_key = tuple(sorted((a, b)))
            if edge_key in seen_edges:
                continue
            seen_edges.add(edge_key)
            rows.append(
                {
                    "kota_a": edge_key[0],
                    "kota_b": edge_key[1],
                    "jarak_km": int(jarak_km),
                }
            )

    if rows:
        supabase.table("city_routes").upsert(
            rows, on_conflict="kota_a,kota_b"
        ).execute()

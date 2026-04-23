"""State hydration helpers from Supabase into in-memory structures."""

from collections import defaultdict

from api.db import get_client
from core.graph import CityGraph
from core.inventory import Inventory
from core.linked_list import CourierRoute
from core.queue import TruckQueue
from core.stack import LoadStack
from core.tree import WarehouseTree
from services.logistics import LogisticsService


def _fetch_table(table_name: str, order_by: str | None = None) -> list[dict]:
    """Fetch rows from Supabase, optionally sorted by one column."""
    client = get_client()
    query = client.table(table_name).select("*")
    if order_by:
        query = query.order(order_by)
    response = query.execute()
    return response.data or []


def _hydrate_tree(rows: list[dict]) -> WarehouseTree:
    """Rebuild WarehouseTree from flat warehouse_nodes rows."""
    tree = WarehouseTree()
    if not rows:
        return tree

    node_map: dict[str, dict] = {}
    root_id: str | None = None

    for row in rows:
        node_id = row.get("id")
        if node_id is None:
            continue
        node_id = str(node_id)
        node_map[node_id] = {
            "id": node_id,
            "name": row.get("name", ""),
            "type": row.get("type", ""),
            "children": [],
            "parent_id": row.get("parent_id"),
        }

    for node in node_map.values():
        parent_id = node.get("parent_id")
        if parent_id is None:
            root_id = node["id"]
            continue
        parent_key = str(parent_id)
        parent = node_map.get(parent_key)
        if parent is not None:
            parent["children"].append(node)

    if root_id is None:
        return tree

    def _strip_internal(node: dict) -> dict:
        return {
            "id": node["id"],
            "name": node["name"],
            "type": node["type"],
            "children": [_strip_internal(child) for child in node["children"]],
        }

    nested_tree = _strip_internal(node_map[root_id])
    tree.load_from_dict(nested_tree)
    return tree


def load_logistics_service() -> LogisticsService:
    """Load persisted tables from Supabase into LogisticsService."""
    tree_rows = _fetch_table("warehouse_nodes")
    inventory_rows = _fetch_table("inventory_items")
    queue_rows = _fetch_table("truck_queue", order_by="joined_at")
    active_load_rows = _fetch_table("active_truck_loads", order_by="loaded_at")
    courier_rows = _fetch_table("courier_packages", order_by="urutan")
    city_route_rows = _fetch_table("city_routes")

    tree = _hydrate_tree(tree_rows)

    inventory = Inventory()
    inventory_dict: dict[str, dict[str, dict]] = {}
    for row in inventory_rows:
        gudang_id = row.get("gudang_id")
        barang_id = row.get("barang_id")
        if not gudang_id or not barang_id:
            continue
        gudang_key = str(gudang_id)
        barang_key = str(barang_id)
        inventory_dict.setdefault(gudang_key, {})[barang_key] = {
            "nama": row.get("nama", barang_key),
            "stok": int(row.get("stok", 0)),
        }
    inventory.load_from_dict(inventory_dict)

    truck_queue = TruckQueue()
    truck_queue.load_from_list(
        [str(row["plat_nomor"]) for row in queue_rows if row.get("plat_nomor")]
    )

    active_trucks: dict[str, LoadStack] = {}
    grouped_loads: dict[str, list[dict]] = defaultdict(list)
    for row in active_load_rows:
        plat_nomor = row.get("plat_nomor")
        if not plat_nomor:
            continue
        grouped_loads[str(plat_nomor)].append(row)

    for plat_nomor, loads in grouped_loads.items():
        stack_obj = LoadStack()
        for load in loads:
            barang_id = load.get("barang_id")
            qty = load.get("qty")
            if barang_id is None or qty is None:
                continue
            stack_obj.push(str(barang_id), int(qty))
        active_trucks[plat_nomor] = stack_obj

    courier_routes: dict[str, CourierRoute] = {}
    grouped_packages: dict[str, list[dict]] = defaultdict(list)
    for row in courier_rows:
        kurir_id = row.get("kurir_id")
        if not kurir_id:
            continue
        grouped_packages[str(kurir_id)].append(row)

    for kurir_id, packages in grouped_packages.items():
        route = CourierRoute()
        for package in packages:
            paket_id = package.get("paket_id")
            alamat = package.get("alamat")
            penerima = package.get("penerima")
            if paket_id is None:
                continue
            route.tambah_paket(
                str(paket_id),
                "" if alamat is None else str(alamat),
                "" if penerima is None else str(penerima),
            )
        courier_routes[kurir_id] = route

    graph = CityGraph()
    for row in city_route_rows:
        kota_a = row.get("kota_a")
        kota_b = row.get("kota_b")
        jarak_km = row.get("jarak_km")
        if kota_a is None or kota_b is None or jarak_km is None:
            continue
        graph.tambah_rute(str(kota_a), str(kota_b), int(jarak_km))

    return LogisticsService(
        tree=tree,
        inventory=inventory,
        truck_queue=truck_queue,
        graph=graph,
        active_trucks=active_trucks,
        courier_routes=courier_routes,
    )

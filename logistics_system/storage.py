"""Memuat dan menyimpan state sistem logistik dalam format JSON."""

import json


def save_state(
    tree,
    inventory,
    truck_queue,
    active_trucks,
    courier_routes,
    graph,
    filepath="data/seed.json",
) -> None:
    """Menyimpan objek saat program berjalan ke state JSON."""
    state = {
        "tree": tree.to_dict(),
        "inventory": inventory.data,
        "graph": graph.adjacency,
        "queue": truck_queue.to_list(),
        "active_trucks": {
            plat: {"stack": stack.to_list()} for plat, stack in active_trucks.items()
        },
        "courier_routes": {
            kid: route.to_list() for kid, route in courier_routes.items()
        },
    }

    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(state, file, indent=2)
    except Exception as err:
        print(f"Error menyimpan state: {err}")


def load_state(filepath="data/seed.json") -> dict:
    """Memuat state JSON mentah untuk dibentuk ulang oleh pemanggil."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Warning: file state tidak ditemukan: {filepath}")
        return {}
    except json.JSONDecodeError as err:
        print(f"Warning: format JSON tidak valid: {err}")
        return {}
    except Exception as err:
        print(f"Warning: gagal memuat state: {err}")
        return {}

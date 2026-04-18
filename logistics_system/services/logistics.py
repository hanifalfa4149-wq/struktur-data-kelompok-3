"""Orchestrator that connects all logistics modules."""

from core.graph import CityGraph
from core.inventory import Inventory
from core.linked_list import RouteNode
from core.queue import TruckQueue
from core.stack import LoadHistory
from core.tree import WarehouseNode


class LogisticsService:
    """Main service orchestrating data structures used by the app."""

    def __init__(self) -> None:
        self.warehouse_tree = WarehouseNode("Pusat")
        self.inventory = Inventory()
        self.truck_queue = TruckQueue()
        self.load_history = LoadHistory()
        self.route_head: RouteNode | None = None
        self.city_graph = CityGraph()

    def run(self) -> None:
        """Display a minimal main menu placeholder."""
        print("=== Logistics System ===")
        print("Sistem siap digunakan.")

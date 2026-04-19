"""Hierarki gudang berbasis n-ary tree dengan penyimpanan flat dict."""


class WarehouseTree:
    """Representasi hierarki gudang dengan lookup O(1)."""

    def __init__(self) -> None:
        """Initialize empty tree."""
        self.nodes = {}
        self.root_id = None

    def add_node(self, parent_id, node_id, name, type) -> None:
        """Add node under parent_id, or set as root when parent_id is None."""
        if node_id in self.nodes:
            raise ValueError(f"Node dengan id '{node_id}' sudah ada")

        if parent_id is None:
            self.root_id = node_id
        else:
            parent = self.nodes.get(parent_id)
            if parent is None:
                raise ValueError(f"Parent '{parent_id}' tidak ditemukan")
            parent["children"].append(node_id)

        self.nodes[node_id] = {
            "id": node_id,
            "name": name,
            "type": type,
            "children": [],
        }

    def get_children(self, node_id) -> list[dict]:
        """Return child node dictionaries for node_id."""
        node = self.nodes.get(node_id)
        if node is None:
            return []

        result = []
        for child_id in node["children"]:
            child = self.nodes.get(child_id)
            if child is not None:
                result.append(
                    {
                        "id": child["id"],
                        "name": child["name"],
                        "type": child["type"],
                        "children": list(child["children"]),
                    }
                )
        return result

    def find_node(self, node_id) -> dict | None:
        """Find node by id using O(1) dictionary lookup."""
        return self.nodes.get(node_id)

    def display_tree(self, node_id=None, indent=0, is_last=True, prefix="") -> None:
        """Display tree recursively using DFS and +-- formatting."""
        del is_last  # kept for signature compatibility
        del prefix

        start_id = self.root_id if node_id is None else node_id
        start_node = self.nodes.get(start_id)
        if start_node is None:
            return

        base_prefix = " " * max(indent, 0)
        print(f"{base_prefix}{start_node['name']}")

        def _display_children(current_id, line_prefix):
            children = self.nodes[current_id]["children"]
            total = len(children)
            for idx, child_id in enumerate(children):
                child = self.nodes.get(child_id)
                if child is None:
                    continue

                is_child_last = idx == total - 1
                print(f"{line_prefix}+-- {child['name']}")
                next_prefix = line_prefix + ("      " if is_child_last else "|     ")
                _display_children(child_id, next_prefix)

        _display_children(start_id, base_prefix + "  ")

    def load_from_dict(self, data: dict) -> None:
        """Load nested tree dict into flat node storage."""
        self.nodes = {}
        self.root_id = None

        if not isinstance(data, dict) or "id" not in data:
            return

        def _walk(node_dict, parent_id=None):
            node_id = node_dict.get("id")
            if node_id is None:
                return

            self.nodes[node_id] = {
                "id": node_id,
                "name": node_dict.get("name", ""),
                "type": node_dict.get("type", ""),
                "children": [],
            }

            if parent_id is None:
                self.root_id = node_id
            else:
                parent = self.nodes.get(parent_id)
                if parent is not None:
                    parent["children"].append(node_id)

            for child in node_dict.get("children", []):
                if isinstance(child, dict):
                    _walk(child, node_id)

        _walk(data)

    def to_dict(self) -> dict:
        """Serialize flat storage into nested tree dict."""
        if self.root_id is None or self.root_id not in self.nodes:
            return {}

        def _build(node_id):
            node = self.nodes[node_id]
            return {
                "id": node["id"],
                "name": node["name"],
                "type": node["type"],
                "children": [
                    _build(child_id)
                    for child_id in node["children"]
                    if child_id in self.nodes
                ],
            }

        return _build(self.root_id)

    def __repr__(self) -> str:
        """Return debug representation of the tree."""
        return f"WarehouseTree(root_id={self.root_id!r}, " f"nodes={len(self.nodes)})"

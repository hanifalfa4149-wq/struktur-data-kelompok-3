from api.state import load_logistics_service
from fastapi import APIRouter

router = APIRouter(prefix="/api/tree", tags=["tree"])


@router.get("/")
def get_tree() -> dict:
    """Return full warehouse tree."""
    svc = load_logistics_service()
    svc.tampilkan_tree()
    return {
        "success": True,
        "message": "OK",
        "data": svc.tree.to_dict(),
    }


@router.get("/children/{node_id}")
def get_tree_children(node_id: str) -> dict:
    """Return child nodes for a warehouse node id."""
    svc = load_logistics_service()
    children = svc.tree.get_children(node_id)
    if not children and svc.tree.find_node(node_id) is None:
        return {
            "success": False,
            "message": "Node tidak ditemukan",
            "data": None,
        }

    return {
        "success": True,
        "message": "OK",
        "data": children,
    }

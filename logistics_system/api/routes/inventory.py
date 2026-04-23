from api.state import load_logistics_service
from fastapi import APIRouter

router = APIRouter(prefix="/api/inventory", tags=["inventory"])


@router.get("/{gudang_id}")
def get_inventory_gudang(gudang_id: str) -> dict:
    """Return all inventory items in one warehouse."""
    svc = load_logistics_service()
    svc.tampilkan_inventaris(gudang_id)
    items = svc.inventory.to_dict().get(gudang_id, {})
    return {
        "success": True,
        "message": "OK",
        "data": items,
    }


@router.get("/{gudang_id}/{barang_id}")
def get_inventory_item(gudang_id: str, barang_id: str) -> dict:
    """Return one inventory item after warehouse validation."""
    svc = load_logistics_service()
    item, message = svc.cek_stok_tervalidasi(gudang_id, barang_id)
    if item is None:
        return {
            "success": False,
            "message": message,
            "data": None,
        }

    return {
        "success": True,
        "message": message,
        "data": item,
    }

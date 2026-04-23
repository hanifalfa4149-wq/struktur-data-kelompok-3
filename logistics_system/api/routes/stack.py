from fastapi import APIRouter
from pydantic import BaseModel

from logistics_system.api.db import get_client
from logistics_system.api.state import load_logistics_service
from logistics_system.api.sync import sync_active_trucks, sync_inventory

router = APIRouter(prefix="/api/stack", tags=["stack"])


class MuatBarangPayload(BaseModel):
    plat_nomor: str
    gudang_id: str
    barang_id: str
    qty: int


class UndoMuatPayload(BaseModel):
    plat_nomor: str
    gudang_id: str


@router.get("/{plat_nomor}")
def get_stack(plat_nomor: str) -> dict:
    """Return load stack content for one active truck."""
    svc = load_logistics_service()
    success, message = svc.tampilkan_muatan(plat_nomor)
    if not success:
        return {
            "success": False,
            "message": message,
            "data": None,
        }

    return {
        "success": True,
        "message": "OK",
        "data": svc.active_trucks[plat_nomor].to_list(),
    }


@router.post("/load")
def muat_barang(payload: MuatBarangPayload) -> dict:
    """Load goods to an active truck and persist inventory + stack changes."""
    svc = load_logistics_service()
    success, message = svc.muat_barang(
        payload.plat_nomor,
        payload.gudang_id,
        payload.barang_id,
        payload.qty,
    )
    if not success:
        return {
            "success": False,
            "message": message,
            "data": None,
        }

    client = get_client()
    sync_inventory(client, svc.inventory)
    sync_active_trucks(client, svc.active_trucks)
    return {
        "success": True,
        "message": message,
        "data": svc.active_trucks[payload.plat_nomor].to_list(),
    }


@router.post("/undo")
def undo_muat(payload: UndoMuatPayload) -> dict:
    """Undo last load from active truck and persist affected structures."""
    svc = load_logistics_service()
    success, message = svc.undo_muat(payload.plat_nomor, payload.gudang_id)
    if not success:
        return {
            "success": False,
            "message": message,
            "data": None,
        }

    client = get_client()
    sync_inventory(client, svc.inventory)
    sync_active_trucks(client, svc.active_trucks)
    return {
        "success": True,
        "message": message,
        "data": svc.active_trucks[payload.plat_nomor].to_list(),
    }

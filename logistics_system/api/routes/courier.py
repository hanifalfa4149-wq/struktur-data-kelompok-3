from fastapi import APIRouter
from pydantic import BaseModel

from logistics_system.api.db import get_client
from logistics_system.api.state import load_logistics_service
from logistics_system.api.sync import sync_courier_routes

router = APIRouter(prefix="/api/courier", tags=["courier"])


class BuatRutePayload(BaseModel):
    kurir_id: str


class TambahPaketPayload(BaseModel):
    kurir_id: str
    paket_id: str
    alamat: str
    penerima: str


class SelesaiAntarPayload(BaseModel):
    kurir_id: str


@router.get("/{kurir_id}")
def get_rute_kurir(kurir_id: str) -> dict:
    """Return package route list for one courier."""
    svc = load_logistics_service()
    success, message = svc.tampilkan_rute_kurir(kurir_id)
    if not success:
        return {
            "success": False,
            "message": message,
            "data": None,
        }

    return {
        "success": True,
        "message": "OK",
        "data": svc.courier_routes[kurir_id].to_list(),
    }


@router.post("/create")
def buat_rute(payload: BuatRutePayload) -> dict:
    """Create route for courier and persist route changes."""
    svc = load_logistics_service()
    success, message = svc.buat_rute_kurir(payload.kurir_id)
    if not success:
        return {
            "success": False,
            "message": message,
            "data": None,
        }

    sync_courier_routes(get_client(), svc.courier_routes)
    return {
        "success": True,
        "message": message,
        "data": {"kurir_id": payload.kurir_id},
    }


@router.post("/add-package")
def tambah_paket(payload: TambahPaketPayload) -> dict:
    """Append package into courier route and persist route changes."""
    svc = load_logistics_service()
    success, message = svc.tambah_paket_kurir(
        payload.kurir_id,
        payload.paket_id,
        payload.alamat,
        payload.penerima,
    )
    if not success:
        return {
            "success": False,
            "message": message,
            "data": None,
        }

    sync_courier_routes(get_client(), svc.courier_routes)
    return {
        "success": True,
        "message": message,
        "data": svc.courier_routes[payload.kurir_id].to_list(),
    }


@router.post("/delivered")
def selesai_antar(payload: SelesaiAntarPayload) -> dict:
    """Mark first package delivered and persist route changes."""
    svc = load_logistics_service()
    paket, message = svc.selesai_antar(payload.kurir_id)
    if paket is None:
        return {
            "success": False,
            "message": message,
            "data": None,
        }

    sync_courier_routes(get_client(), svc.courier_routes)
    return {
        "success": True,
        "message": message,
        "data": paket,
    }

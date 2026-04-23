from fastapi import APIRouter, Query
from pydantic import BaseModel

from logistics_system.api.db import get_client
from logistics_system.api.state import load_logistics_service
from logistics_system.api.sync import sync_graph

router = APIRouter(prefix="/api/graph", tags=["graph"])


class TambahRutePayload(BaseModel):
    kota_a: str
    kota_b: str
    jarak_km: int


@router.get("/")
def get_graph() -> dict:
    """Return full city route graph."""
    svc = load_logistics_service()
    return {
        "success": True,
        "message": "OK",
        "data": svc.graph.to_dict(),
    }


@router.get("/path")
def cari_jalur(
    kota_a: str = Query(...),
    kota_b: str = Query(...),
) -> dict:
    """Find BFS path between two cities."""
    svc = load_logistics_service()
    path, message = svc.cari_jalur_kota(kota_a, kota_b)
    if path is None:
        return {
            "success": False,
            "message": message,
            "data": None,
        }

    return {
        "success": True,
        "message": message,
        "data": path,
    }


@router.post("/add-route")
def tambah_rute(payload: TambahRutePayload) -> dict:
    """Add a bidirectional city route and persist graph updates."""
    svc = load_logistics_service()
    success, message = svc.tambah_rute_kota(
        payload.kota_a,
        payload.kota_b,
        payload.jarak_km,
    )
    if not success:
        return {
            "success": False,
            "message": message,
            "data": None,
        }

    sync_graph(get_client(), svc.graph)
    return {
        "success": True,
        "message": message,
        "data": svc.graph.to_dict(),
    }


@router.get("/check")
def cek_koneksi(
    kota_a: str = Query(...),
    kota_b: str = Query(...),
) -> dict:
    """Check direct edge connectivity between two cities."""
    svc = load_logistics_service()
    terkoneksi = svc.graph.cek_koneksi_langsung(kota_a, kota_b)
    return {
        "success": True,
        "message": "OK",
        "data": {"connected": terkoneksi},
    }

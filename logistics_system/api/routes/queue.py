from api.db import get_client
from api.state import load_logistics_service
from api.sync import sync_active_trucks, sync_truck_queue
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/queue", tags=["queue"])


class EnqueuePayload(BaseModel):
    plat_nomor: str


@router.get("/")
def get_queue() -> dict:
    """Return current truck queue."""
    svc = load_logistics_service()
    return {
        "success": True,
        "message": "OK",
        "data": svc.truck_queue.to_list(),
    }


@router.post("/enqueue")
def enqueue_truck(payload: EnqueuePayload) -> dict:
    """Add one truck plate into queue and persist it."""
    svc = load_logistics_service()
    svc.truck_queue.enqueue(payload.plat_nomor)
    sync_truck_queue(get_client(), svc.truck_queue)

    return {
        "success": True,
        "message": f"Truk {payload.plat_nomor} ditambahkan ke antrean",
        "data": svc.truck_queue.to_list(),
    }


@router.post("/process")
def process_queue() -> dict:
    """Process next truck, activate its load stack, and persist updates."""
    svc = load_logistics_service()
    plat_nomor, message = svc.proses_truk_berikutnya()
    if plat_nomor is None:
        return {
            "success": False,
            "message": message,
            "data": None,
        }

    client = get_client()
    sync_truck_queue(client, svc.truck_queue)
    sync_active_trucks(client, svc.active_trucks)
    return {
        "success": True,
        "message": message,
        "data": {"plat_nomor": plat_nomor},
    }

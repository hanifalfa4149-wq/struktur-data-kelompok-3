import { CONFIG } from "./config.js";

async function postJson(path, payload) {
  try {
    const response = await fetch(`${CONFIG.API_BASE}${path}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const json = await response.json();
    return json;
  } catch (error) {
    return {
      success: false,
      message: error.message,
      data: null,
    };
  }
}

export async function enqueue(platNomor) {
  return postJson("/queue/enqueue", { plat_nomor: platNomor });
}

export async function processNextTruck() {
  return postJson("/queue/process", {});
}

export async function loadBarang(platNomor, gudangId, barangId, qty) {
  return postJson("/stack/load", {
    plat_nomor: platNomor,
    gudang_id: gudangId,
    barang_id: barangId,
    qty,
  });
}

export async function undoMuat(platNomor, gudangId) {
  return postJson("/stack/undo", {
    plat_nomor: platNomor,
    gudang_id: gudangId,
  });
}

export async function createRoute(kurirId) {
  return postJson("/courier/create", { kurir_id: kurirId });
}

export async function addPackage(kurirId, paketId, alamat, penerima) {
  return postJson("/courier/add-package", {
    kurir_id: kurirId,
    paket_id: paketId,
    alamat,
    penerima,
  });
}

export async function markDelivered(kurirId) {
  return postJson("/courier/delivered", { kurir_id: kurirId });
}

export async function addRoute(kotaA, kotaB, jarakKm) {
  return postJson("/graph/add-route", {
    kota_a: kotaA,
    kota_b: kotaB,
    jarak_km: jarakKm,
  });
}

export async function findPath(kotaA, kotaB) {
  try {
    const params = new URLSearchParams({ kota_a: kotaA, kota_b: kotaB });
    const response = await fetch(`${CONFIG.API_BASE}/graph/path?${params}`);
    const json = await response.json();
    return json;
  } catch (error) {
    return {
      success: false,
      message: error.message,
      data: null,
    };
  }
}

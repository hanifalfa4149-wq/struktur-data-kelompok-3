import { CONFIG } from "./config.js";
import { supabaseClient } from "./supabase-client.js";

function missingKeyResult() {
  return {
    success: false,
    message: "SUPABASE_ANON_KEY belum diisi pada config.js",
    data: [],
  };
}

function successResult(data) {
  return {
    success: true,
    message: "OK",
    data,
  };
}

function errorResult(error) {
  return {
    success: false,
    message: error?.message || "Gagal mengambil data dari Supabase",
    data: [],
  };
}

export async function getTree() {
  if (!CONFIG.SUPABASE_ANON_KEY) {
    return missingKeyResult();
  }

  const { data, error } = await supabaseClient
    .from("warehouse_nodes")
    .select("*");

  if (error) {
    return errorResult(error);
  }
  return successResult(data || []);
}

export async function getInventory(gudangId) {
  if (!CONFIG.SUPABASE_ANON_KEY) {
    return missingKeyResult();
  }

  const { data, error } = await supabaseClient
    .from("inventory_items")
    .select("*")
    .eq("gudang_id", gudangId);

  if (error) {
    return errorResult(error);
  }
  return successResult(data || []);
}

export async function getQueue() {
  if (!CONFIG.SUPABASE_ANON_KEY) {
    return missingKeyResult();
  }

  const { data, error } = await supabaseClient
    .from("truck_queue")
    .select("*")
    .order("joined_at", { ascending: true });

  if (error) {
    return errorResult(error);
  }
  return successResult(data || []);
}

export async function getActiveTrucks() {
  if (!CONFIG.SUPABASE_ANON_KEY) {
    return missingKeyResult();
  }

  const { data, error } = await supabaseClient
    .from("active_truck_loads")
    .select("*")
    .order("plat_nomor", { ascending: true })
    .order("loaded_at", { ascending: true });

  if (error) {
    return errorResult(error);
  }
  return successResult(data || []);
}

export async function getCourierRoute(kurirId) {
  if (!CONFIG.SUPABASE_ANON_KEY) {
    return missingKeyResult();
  }

  const { data, error } = await supabaseClient
    .from("courier_packages")
    .select("*")
    .eq("kurir_id", kurirId)
    .order("urutan", { ascending: true });

  if (error) {
    return errorResult(error);
  }
  return successResult(data || []);
}

export async function getGraph() {
  if (!CONFIG.SUPABASE_ANON_KEY) {
    return missingKeyResult();
  }

  const { data, error } = await supabaseClient.from("city_routes").select("*");

  if (error) {
    return errorResult(error);
  }
  return successResult(data || []);
}

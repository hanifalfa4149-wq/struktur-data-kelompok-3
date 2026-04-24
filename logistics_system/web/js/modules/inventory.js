import { showToast } from "../app.js";
import { getInventory } from "../supabase.js";

function renderMessage(text, ok = true) {
  const msgEl = document.getElementById("inventory-info");
  msgEl.innerHTML = `<span class="${ok ? "text-success" : "text-error"}">${text}</span>`;
}

function renderTable(items) {
  const result = document.getElementById("inventory-result");
  if (!items.length) {
    result.innerHTML = '<div class="empty-state">📭 Belum ada data</div>';
    return;
  }

  const rows = items
    .map(
      (item) => `<tr><td class="mono">${item.barang_id}</td><td>${item.nama || "-"}</td><td>${item.stok ?? 0}</td></tr>`,
    )
    .join("");

  result.innerHTML = `<table><thead><tr><th>Barang ID</th><th>Nama</th><th>Stok</th></tr></thead><tbody>${rows}</tbody></table>`;
}

export async function initInventoryModule() {
  const gudangForm = document.getElementById("inventory-gudang-form");
  const itemForm = document.getElementById("inventory-item-form");

  gudangForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const gudangId = document.getElementById("inv-gudang-id").value.trim();
    if (!gudangId) {
      renderMessage("Isi gudang_id terlebih dahulu.", false);
      return;
    }

    const res = await getInventory(gudangId);
    if (!res.success) {
      renderMessage(res.message, false);
      renderTable([]);
      showToast(res.message, "error");
      return;
    }

    renderMessage(`Data gudang ${gudangId} berhasil dimuat.`);
    renderTable(res.data);
  });

  itemForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const gudangId = document.getElementById("inv-item-gudang-id").value.trim();
    const barangId = document.getElementById("inv-barang-id").value.trim();

    if (!gudangId || !barangId) {
      renderMessage("Isi gudang_id dan barang_id terlebih dahulu.", false);
      return;
    }

    const res = await getInventory(gudangId);
    if (!res.success) {
      renderMessage(res.message, false);
      showToast(res.message, "error");
      return;
    }

    const item = res.data.find((row) => String(row.barang_id) === barangId);
    if (!item) {
      renderMessage("Barang tidak ditemukan.", false);
      renderTable([]);
      return;
    }

    renderMessage("Detail barang ditemukan.");
    renderTable([item]);
  });
}

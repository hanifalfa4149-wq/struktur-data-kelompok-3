import { loadBarang, undoMuat } from "../api.js";
import { setLoading, showToast } from "../app.js";
import { getActiveTrucks } from "../supabase.js";

function setStackMessage(message, ok = true) {
  const info = document.getElementById("stack-info");
  info.innerHTML = `<span class="${ok ? "text-success" : "text-error"}">${message}</span>`;
}

function renderStack(rows) {
  const result = document.getElementById("stack-result");
  if (!rows.length) {
    result.innerHTML = '<div class="muted">Stack muatan kosong.</div>';
    return;
  }

  const html = rows
    .map(
      (row, index) =>
        `<li>${index + 1}. ${row.barang_id} x${row.qty} <span class="muted">(${new Date(
          row.loaded_at,
        ).toLocaleString()})</span></li>`,
    )
    .join("");
  result.innerHTML = `<ol>${html}</ol>`;
}

async function refreshStackByPlate(platNomor) {
  const res = await getActiveTrucks();
  if (!res.success) {
    setStackMessage(res.message, false);
    renderStack([]);
    return;
  }

  const rows = res.data.filter(
    (row) => String(row.plat_nomor) === String(platNomor),
  );
  renderStack(rows);
  setStackMessage(`Data stack untuk ${platNomor} berhasil dimuat.`, true);
}

export async function initStackModule() {
  const viewForm = document.getElementById("stack-view-form");
  const loadForm = document.getElementById("stack-load-form");
  const undoForm = document.getElementById("stack-undo-form");

  viewForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const plate = document.getElementById("stack-view-plat").value.trim();
    if (!plate) {
      setStackMessage("Isi plat_nomor terlebih dahulu.", false);
      return;
    }
    await refreshStackByPlate(plate);
  });

  loadForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = loadForm.querySelector("button[type='submit']");
    const plate = document.getElementById("stack-load-plat").value.trim();
    const gudang = document.getElementById("stack-load-gudang").value.trim();
    const barang = document.getElementById("stack-load-barang").value.trim();
    const qty = Number(document.getElementById("stack-load-qty").value);

    if (!plate || !gudang || !barang || !qty) {
      setStackMessage("Semua field muat harus diisi.", false);
      return;
    }

    setLoading(button, true);
    const res = await loadBarang(plate, gudang, barang, qty);
    setLoading(button, false);

    if (!res.success) {
      setStackMessage(res.message, false);
      showToast(res.message, "error");
      return;
    }

    setStackMessage(res.message, true);
    showToast(res.message, "success");
    await refreshStackByPlate(plate);
  });

  undoForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = undoForm.querySelector("button[type='submit']");
    const plate = document.getElementById("stack-undo-plat").value.trim();
    const gudang = document.getElementById("stack-undo-gudang").value.trim();

    if (!plate || !gudang) {
      setStackMessage("Isi plat_nomor dan gudang_id untuk undo.", false);
      return;
    }

    setLoading(button, true);
    const res = await undoMuat(plate, gudang);
    setLoading(button, false);

    if (!res.success) {
      setStackMessage(res.message, false);
      showToast(res.message, "error");
      return;
    }

    setStackMessage(res.message, true);
    showToast(res.message, "success");
    await refreshStackByPlate(plate);
  });
}

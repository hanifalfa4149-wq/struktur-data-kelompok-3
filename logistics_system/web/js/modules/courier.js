import { addPackage, createRoute, markDelivered } from "../api.js";
import { setLoading, showToast } from "../app.js";
import { getCourierRoute } from "../supabase.js";

function setCourierMessage(message, ok = true) {
  const info = document.getElementById("courier-info");
  info.innerHTML = `<span class="${ok ? "text-success" : "text-error"}">${message}</span>`;
}

function renderCourierRows(rows) {
  const result = document.getElementById("courier-result");
  if (!rows.length) {
    result.innerHTML = '<div class="empty-state">📭 Belum ada data</div>';
    return;
  }

  const html = rows
    .map(
      (row) =>
        `<li class="timeline-item"><div class="timeline-title">#${row.urutan} <span class="mono">${row.paket_id}</span></div><div class="timeline-sub">${row.alamat} • ${row.penerima}</div></li>`,
    )
    .join("");

  result.innerHTML = `<ul class="timeline-list">${html}</ul>`;
}

function animateTopDelivered() {
  const firstItem = document.querySelector("#courier-result .timeline-item");
  if (!firstItem) {
    return Promise.resolve();
  }

  firstItem.classList.add("delivered-out");
  return new Promise((resolve) => {
    setTimeout(resolve, 220);
  });
}

async function refreshRoute(kurirId) {
  const res = await getCourierRoute(kurirId);
  if (!res.success) {
    setCourierMessage(res.message, false);
    renderCourierRows([]);
    return;
  }

  setCourierMessage(`Rute kurir ${kurirId} berhasil dimuat.`);
  renderCourierRows(res.data);
}

export async function initCourierModule() {
  const viewForm = document.getElementById("courier-view-form");
  const createForm = document.getElementById("courier-create-form");
  const addForm = document.getElementById("courier-add-form");
  const deliveredForm = document.getElementById("courier-delivered-form");

  viewForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const kurirId = document.getElementById("courier-view-id").value.trim();
    if (!kurirId) {
      setCourierMessage("Isi kurir_id terlebih dahulu.", false);
      return;
    }
    await refreshRoute(kurirId);
  });

  createForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = createForm.querySelector("button[type='submit']");
    const kurirId = document.getElementById("courier-create-id").value.trim();
    if (!kurirId) {
      setCourierMessage("Isi kurir_id terlebih dahulu.", false);
      return;
    }

    setLoading(button, true);
    const res = await createRoute(kurirId);
    setLoading(button, false);

    if (!res.success) {
      setCourierMessage(res.message, false);
      showToast(res.message, "error");
      return;
    }

    setCourierMessage(res.message, true);
    showToast(res.message, "success");
    await refreshRoute(kurirId);
  });

  addForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = addForm.querySelector("button[type='submit']");
    const kurirId = document.getElementById("courier-add-id").value.trim();
    const paketId = document.getElementById("courier-paket-id").value.trim();
    const alamat = document.getElementById("courier-alamat").value.trim();
    const penerima = document.getElementById("courier-penerima").value.trim();

    if (!kurirId || !paketId || !alamat || !penerima) {
      setCourierMessage("Semua field tambah paket harus diisi.", false);
      return;
    }

    setLoading(button, true);
    const res = await addPackage(kurirId, paketId, alamat, penerima);
    setLoading(button, false);

    if (!res.success) {
      setCourierMessage(res.message, false);
      showToast(res.message, "error");
      return;
    }

    setCourierMessage(res.message, true);
    showToast(res.message, "success");
    await refreshRoute(kurirId);
  });

  deliveredForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = deliveredForm.querySelector("button[type='submit']");
    const kurirId = document.getElementById("courier-delivered-id").value.trim();

    if (!kurirId) {
      setCourierMessage("Isi kurir_id terlebih dahulu.", false);
      return;
    }

    setLoading(button, true);
    const res = await markDelivered(kurirId);
    setLoading(button, false);

    if (!res.success) {
      setCourierMessage(res.message, false);
      showToast(res.message, "error");
      return;
    }

    setCourierMessage(res.message, true);
    showToast(res.message, "success");
    await animateTopDelivered();
    await refreshRoute(kurirId);
  });
}

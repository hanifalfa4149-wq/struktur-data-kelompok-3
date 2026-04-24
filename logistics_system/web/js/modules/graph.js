import { addRoute, findPath } from "../api.js";
import { setLoading, showToast } from "../app.js";
import { getGraph } from "../supabase.js";

function setGraphMessage(message, ok = true) {
  const info = document.getElementById("graph-info");
  info.innerHTML = `<span class="${ok ? "text-success" : "text-error"}">${message}</span>`;
}

function renderGraphTable(rows) {
  const result = document.getElementById("graph-result");
  if (!rows.length) {
    result.innerHTML = '<div class="empty-state">📭 Belum ada data</div>';
    return;
  }

  const tableRows = rows
    .map(
      (row) =>
        `<tr><td class="mono">${row.kota_a}</td><td class="mono">${row.kota_b}</td><td><span class="km-badge">${row.jarak_km} km</span></td></tr>`,
    )
    .join("");

  result.innerHTML = `<table><thead><tr><th>Kota A</th><th>Kota B</th><th>Jarak (km)</th></tr></thead><tbody>${tableRows}</tbody></table>`;
}

function renderPath(path) {
  const el = document.getElementById("graph-path-result");
  if (!path || !path.length) {
    el.innerHTML = '<div class="empty-state">📭 Belum ada data</div>';
    return;
  }

  const chain = path
    .map((kota) => `<span class="path-node">${kota}</span>`)
    .join('<span class="path-arrow">→</span>');
  el.innerHTML = `<div class="path-chain">${chain}</div>`;
}

async function refreshGraph() {
  const res = await getGraph();
  if (!res.success) {
    setGraphMessage(res.message, false);
    renderGraphTable([]);
    return;
  }

  setGraphMessage("Peta kota berhasil dimuat.", true);
  renderGraphTable(res.data);
}

export async function initGraphModule() {
  const pathForm = document.getElementById("graph-path-form");
  const addRouteForm = document.getElementById("graph-add-route-form");

  pathForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = pathForm.querySelector("button[type='submit']");
    const kotaA = document.getElementById("graph-path-kota-a").value.trim();
    const kotaB = document.getElementById("graph-path-kota-b").value.trim();

    if (!kotaA || !kotaB) {
      setGraphMessage("Isi kota_a dan kota_b terlebih dahulu.", false);
      return;
    }

    setLoading(button, true);
    const res = await findPath(kotaA, kotaB);
    setLoading(button, false);

    if (!res.success) {
      setGraphMessage(res.message, false);
      renderPath([]);
      showToast(res.message, "error");
      return;
    }

    setGraphMessage("Jalur ditemukan.", true);
    renderPath(res.data);
    showToast("Pencarian jalur berhasil", "success");
  });

  addRouteForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = addRouteForm.querySelector("button[type='submit']");
    const kotaA = document.getElementById("graph-add-kota-a").value.trim();
    const kotaB = document.getElementById("graph-add-kota-b").value.trim();
    const jarakKm = Number(document.getElementById("graph-add-jarak").value);

    if (!kotaA || !kotaB || !jarakKm) {
      setGraphMessage("Isi kota_a, kota_b, dan jarak terlebih dahulu.", false);
      return;
    }

    setLoading(button, true);
    const res = await addRoute(kotaA, kotaB, jarakKm);
    setLoading(button, false);

    if (!res.success) {
      setGraphMessage(res.message, false);
      showToast(res.message, "error");
      return;
    }

    setGraphMessage(res.message, true);
    showToast(res.message, "success");
    await refreshGraph();
    addRouteForm.reset();
  });

  await refreshGraph();
}

import { enqueue, processNextTruck } from "../api.js";
import { setLoading, showToast } from "../app.js";
import { getQueue } from "../supabase.js";

function renderQueue(items) {
  const result = document.getElementById("queue-result");
  if (!items.length) {
    result.innerHTML = '<div class="empty-state">🅿️ Loading dock kosong</div>';
    return;
  }

  const html = items
    .map((item, index) => {
      const joinedAt = item.joined_at
        ? new Date(item.joined_at).toLocaleString("id-ID")
        : "Waktu tidak tersedia";
      return `<article class="queue-card"><div class="queue-plate">${item.plat_nomor}</div><div class="queue-joined">Posisi #${index + 1} • ${joinedAt}</div></article>`;
    })
    .join("");
  result.innerHTML = `<div class="queue-strip">${html}</div>`;
}

function setQueueMessage(message, ok = true) {
  const msg = document.getElementById("queue-info");
  msg.innerHTML = `<span class="${ok ? "text-success" : "text-error"}">${message}</span>`;
}

async function refreshQueue() {
  const res = await getQueue();
  if (!res.success) {
    setQueueMessage(res.message, false);
    renderQueue([]);
    return;
  }

  renderQueue(res.data);
  setQueueMessage("Antrean terbaru berhasil dimuat.", true);
}

export async function initQueueModule() {
  const form = document.getElementById("queue-enqueue-form");
  const processBtn = document.getElementById("queue-process-btn");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const plat = document.getElementById("queue-plat-nomor").value.trim();
    const submitBtn = form.querySelector("button[type='submit']");

    if (!plat) {
      setQueueMessage("Isi plat_nomor terlebih dahulu.", false);
      return;
    }

    setLoading(submitBtn, true);
    const res = await enqueue(plat);
    setLoading(submitBtn, false);

    if (!res.success) {
      setQueueMessage(res.message, false);
      showToast(res.message, "error");
      return;
    }

    setQueueMessage(res.message, true);
    showToast(res.message, "success");
    await refreshQueue();
    form.reset();
  });

  processBtn.addEventListener("click", async () => {
    setLoading(processBtn, true);
    const res = await processNextTruck();
    setLoading(processBtn, false);

    if (!res.success) {
      setQueueMessage(res.message, false);
      showToast(res.message, "error");
      return;
    }

    setQueueMessage(res.message, true);
    showToast(res.message, "success");
    await refreshQueue();
  });

  await refreshQueue();
}

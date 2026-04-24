import { initCourierModule } from "./modules/courier.js";
import { initGraphModule } from "./modules/graph.js";
import { initInventoryModule } from "./modules/inventory.js";
import { initQueueModule } from "./modules/queue.js";
import { initStackModule } from "./modules/stack.js";
import { initTreeModule } from "./modules/tree.js";

const MODULE_TITLES = {
  hierarki: "Hierarki",
  inventaris: "Inventaris",
  antrean: "Antrean",
  stack: "Muat & Undo",
  kurir: "Kurir",
  peta: "Peta",
};

export function showToast(message, type = "success") {
  const container = document.getElementById("toast-container");
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = message;

  container.appendChild(toast);

  requestAnimationFrame(() => {
    toast.classList.add("show");
  });

  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => {
      toast.remove();
    }, 240);
  }, 3000);
}

export function setLoading(buttonEl, loading) {
  if (!buttonEl) {
    return;
  }

  if (loading) {
    if (!buttonEl.dataset.originalText) {
      buttonEl.dataset.originalText = buttonEl.textContent;
    }
    buttonEl.classList.add("is-loading");
    buttonEl.disabled = true;
    buttonEl.textContent = "Memuat...";
    return;
  }

  buttonEl.classList.remove("is-loading");
  buttonEl.disabled = false;
  if (buttonEl.dataset.originalText) {
    buttonEl.textContent = buttonEl.dataset.originalText;
  }
}

function updateTopbar(tabName) {
  const activeModuleEl = document.getElementById("active-module");
  if (activeModuleEl) {
    activeModuleEl.textContent = MODULE_TITLES[tabName] || "Dashboard";
  }
}

function activateTab(tabName) {
  document.querySelectorAll(".tab-btn").forEach((button) => {
    const active = button.dataset.tab === tabName;
    button.classList.toggle("active", active);
  });

  document.querySelectorAll(".panel").forEach((panel) => {
    panel.classList.toggle("active", panel.id === `panel-${tabName}`);
  });

  updateTopbar(tabName);
}

function initTabs() {
  document.querySelectorAll(".tab-btn").forEach((button) => {
    button.addEventListener("click", () => {
      activateTab(button.dataset.tab);
    });
  });
}

function setupClock() {
  const clockEl = document.getElementById("live-clock");
  if (!clockEl) {
    return;
  }

  const tick = () => {
    clockEl.textContent = new Date().toLocaleTimeString("id-ID", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  };

  tick();
  setInterval(tick, 1000);
}

function resolveResultStatus(messageEl, resultEl) {
  if (!messageEl || !resultEl) {
    return;
  }

  const success = messageEl.querySelector(".text-success");
  const error = messageEl.querySelector(".text-error");
  resultEl.classList.remove("state-success", "state-error");

  if (success) {
    resultEl.classList.add("state-success");
  } else if (error) {
    resultEl.classList.add("state-error");
  }
}

function countRowsInTable(resultEl) {
  if (!resultEl) {
    return 0;
  }
  return resultEl.querySelectorAll("tbody tr").length;
}

function updateStatValue(id, value) {
  const target = document.getElementById(id);
  if (target) {
    target.textContent = String(value);
  }
}

function initDashboardWatchers() {
  const binds = [
    ["tree-info", "tree-result"],
    ["inventory-info", "inventory-result"],
    ["queue-info", "queue-result"],
    ["stack-info", "stack-result"],
    ["courier-info", "courier-result"],
    ["graph-info", "graph-result"],
  ];

  binds.forEach(([infoId, resultId]) => {
    const infoEl = document.getElementById(infoId);
    const resultEl = document.getElementById(resultId);
    if (!infoEl || !resultEl) {
      return;
    }

    const observer = new MutationObserver(() => {
      resolveResultStatus(infoEl, resultEl);
      updateStatValue("stat-tree-total", document.querySelectorAll("#tree-result .tree-node").length);
      updateStatValue("stat-inventory-count", countRowsInTable(document.getElementById("inventory-result")));
      updateStatValue(
        "stat-queue-count",
        document.querySelectorAll("#queue-result .queue-card, #queue-result li").length,
      );
    });

    observer.observe(infoEl, { childList: true, subtree: true, characterData: true });
    observer.observe(resultEl, { childList: true, subtree: true, characterData: true });
    resolveResultStatus(infoEl, resultEl);
  });
}

document.addEventListener("DOMContentLoaded", async () => {
  setupClock();
  initTabs();
  initDashboardWatchers();
  activateTab("hierarki");

  await initTreeModule();
  await initInventoryModule();
  await initQueueModule();
  await initStackModule();
  await initCourierModule();
  await initGraphModule();
});

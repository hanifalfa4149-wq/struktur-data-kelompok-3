import { initCourierModule } from "./modules/courier.js";
import { initGraphModule } from "./modules/graph.js";
import { initInventoryModule } from "./modules/inventory.js";
import { initQueueModule } from "./modules/queue.js";
import { initStackModule } from "./modules/stack.js";
import { initTreeModule } from "./modules/tree.js";

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
    }, 180);
  }, 2600);
}

export function setLoading(buttonEl, loading) {
  if (!buttonEl) {
    return;
  }

  if (loading) {
    if (!buttonEl.dataset.originalText) {
      buttonEl.dataset.originalText = buttonEl.textContent;
    }
    buttonEl.disabled = true;
    buttonEl.textContent = "Loading...";
    return;
  }

  buttonEl.disabled = false;
  if (buttonEl.dataset.originalText) {
    buttonEl.textContent = buttonEl.dataset.originalText;
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
}

function initTabs() {
  document.querySelectorAll(".tab-btn").forEach((button) => {
    button.addEventListener("click", () => {
      activateTab(button.dataset.tab);
    });
  });
}

document.addEventListener("DOMContentLoaded", async () => {
  initTabs();
  activateTab("hierarki");

  await initTreeModule();
  await initInventoryModule();
  await initQueueModule();
  await initStackModule();
  await initCourierModule();
  await initGraphModule();
});

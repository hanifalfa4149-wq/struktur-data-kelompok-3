import { showToast } from "../app.js";
import { getTree } from "../supabase.js";

let treeRows = [];

function typeBadge(type) {
  const normalized = String(type || "").toLowerCase();
  if (normalized === "pusat") {
    return '<span class="badge pusat">pusat</span>';
  }
  if (normalized === "regional") {
    return '<span class="badge regional">regional</span>';
  }
  return '<span class="badge gudang">gudang</span>';
}

function buildTree(rows, parentId = null, depth = 0) {
  const children = rows.filter((row) => {
    if (parentId === null) {
      return row.parent_id === null;
    }
    return String(row.parent_id) === String(parentId);
  });

  return children
    .map((node) => {
      const indent = depth * 16;
      const label = `<div class="tree-node" style="padding-left:${indent}px">${
        typeBadge(node.type)
      } <strong>${node.name || node.id}</strong> <span class="muted">(${node.id})</span></div>`;
      const subtree = buildTree(rows, node.id, depth + 1);
      return `${label}${subtree}`;
    })
    .join("");
}

function renderTreeResult(message, html, ok = true) {
  const info = document.getElementById("tree-info");
  const result = document.getElementById("tree-result");
  info.innerHTML = `<span class="${ok ? "text-success" : "text-error"}">${message}</span>`;
  result.innerHTML = html || '<div class="muted">Tidak ada data.</div>';
}

function renderChildren(nodeId) {
  const exists = treeRows.some((row) => String(row.id) === String(nodeId));
  if (!exists) {
    renderTreeResult("Node tidak ditemukan.", "", false);
    return;
  }

  const children = treeRows.filter(
    (row) => String(row.parent_id) === String(nodeId),
  );
  if (!children.length) {
    renderTreeResult("Node tidak memiliki anak.", "", true);
    return;
  }

  const html = children
    .map(
      (child) =>
        `<div class="list-row">${typeBadge(child.type)} <strong>${
          child.name || child.id
        }</strong> <span class="muted">(${child.id})</span></div>`,
    )
    .join("");
  renderTreeResult(`Ditemukan ${children.length} node anak.`, html, true);
}

async function loadAndRenderTree() {
  const res = await getTree();
  if (!res.success) {
    renderTreeResult(res.message, "", false);
    showToast(res.message, "error");
    return;
  }

  treeRows = res.data;
  const html = buildTree(treeRows);
  renderTreeResult("Hierarki berhasil dimuat.", html, true);
}

export async function initTreeModule() {
  const form = document.getElementById("tree-children-form");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const nodeId = document.getElementById("tree-node-id").value.trim();
    if (!nodeId) {
      renderTreeResult("Isi node_id terlebih dahulu.", "", false);
      return;
    }
    renderChildren(nodeId);
  });

  await loadAndRenderTree();
}

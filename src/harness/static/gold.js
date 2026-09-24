const state = { page: 1, pageSize: 20, q: "", subject: "all", status: "all", split: "all" };
const $ = (selector) => document.querySelector(selector);

async function api(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#039;"}[char]));
}

function formatNumber(value) { return new Intl.NumberFormat().format(value ?? 0); }

function renderStats(summary) {
  $("#stat-cases").textContent = formatNumber(summary.cases);
  $("#stat-answer").textContent = formatNumber(summary.statuses?.answer || 0);
  $("#stat-refuse").textContent = formatNumber(summary.statuses?.refuse || 0);
  $("#stat-clarify").textContent = formatNumber(summary.statuses?.clarify || 0);
  $("#dataset-file").textContent = `${formatNumber(summary.cases)} cases`;
  const select = $("#subject");
  if (select.options.length <= 1) {
    Object.entries(summary.subjects || {}).sort().forEach(([subject, count]) => {
      const option = document.createElement("option");
      option.value = subject; option.textContent = `${subject} · ${formatNumber(count)}`;
      select.append(option);
    });
  }
}

function statusClass(status) {
  return status === "answer" ? "family" : (status === "refuse" ? "draft" : "tool");
}

function renderRecords(data) {
  renderStats(data.summary);
  $("#result-count").textContent = `${formatNumber(data.total)} matching case${data.total === 1 ? "" : "s"}`;
  const filtered = state.q || state.subject !== "all" || state.status !== "all" || state.split !== "all";
  $("#filter-note").textContent = filtered ? "filtered view" : "All gold cases";
  $("#page-label").textContent = `${data.page} / ${data.pages}`;
  $("#prev").disabled = data.page <= 1;
  $("#next").disabled = data.page >= data.pages;
  const list = $("#record-list");
  list.innerHTML = data.items.map((record, index) => {
    const tags = [
      `<span class="tag">${escapeHtml(record.subject)}</span>`,
      `<span class="tag ${statusClass(record.expected_status)}">expects ${escapeHtml(record.expected_status)}</span>`,
      `<span class="tag">${escapeHtml(record.split)}</span>`,
    ];
    if (record.expected_unit) tags.push(`<span class="tag">unit ${escapeHtml(String(record.expected_unit).replace("unit-", ""))}</span>`);
    return `<article class="record-card" data-record-id="${escapeHtml(record.id)}" style="animation-delay:${index * 35}ms"><div><h3>${escapeHtml(record.id)}</h3><p>${escapeHtml(record.query)}</p></div><div class="record-id">${escapeHtml(record.expected_path || "no file — behavior only")}</div><div class="record-tags">${tags.join("")}</div></article>`;
  }).join("");
  $("#empty-state").hidden = data.total !== 0;
}

async function load() {
  const params = new URLSearchParams({ q: state.q, subject: state.subject, status: state.status, split: state.split, page: state.page, page_size: state.pageSize });
  try { renderRecords(await api(`/gold/cases?${params}`)); } catch (error) { $("#result-count").textContent = "Could not load archive"; console.error(error); }
}

function openDrawer(record) {
  $("#drawer-id").textContent = record.id;
  $("#drawer-meta").innerHTML = [record.subject, `expects ${record.expected_status}`, record.split, record.split_file].filter(Boolean).map((item) => `<span class="tag">${escapeHtml(item)}</span>`).join("");
  const rows = [
    ["Question", escapeHtml(record.query)],
    ["Expected behavior", escapeHtml(record.expected_status)],
    ["Expected file", escapeHtml(record.expected_path || "— (behavior-only case)")],
    ["Expected unit", escapeHtml(record.expected_unit || "—")],
    ["Keywords", escapeHtml((record.keywords || []).join(", ") || "—")],
  ];
  $("#case-view").innerHTML = `<table style="width:100%;font-size:14px">${rows.map(([k, v]) => `<tr><td style="color:#888;width:150px;vertical-align:top">${k}</td><td>${v}</td></tr>`).join("")}</table>`;
  $("#json-view").textContent = JSON.stringify(record, null, 2);
  $("#drawer").classList.add("open"); $("#drawer").setAttribute("aria-hidden", "false"); document.body.style.overflow = "hidden";
  activateTab("case");
}

function closeDrawer() { $("#drawer").classList.remove("open"); $("#drawer").setAttribute("aria-hidden", "true"); document.body.style.overflow = ""; }
function activateTab(name) { document.querySelectorAll(".tab").forEach((tab) => tab.classList.toggle("active", tab.dataset.tab === name)); document.querySelectorAll(".tab-panel").forEach((panel) => panel.classList.remove("active")); $(`#${name}-view`).classList.add("active"); }

function debounce(callback, delay) { let timer; return (...args) => { clearTimeout(timer); timer = setTimeout(() => callback(...args), delay); }; }

$("#record-list").addEventListener("click", async (event) => { const card = event.target.closest("[data-record-id]"); if (!card) return; openDrawer(await api(`/gold/cases/${encodeURIComponent(card.dataset.recordId)}`)); });
document.querySelectorAll("[data-close]").forEach((node) => node.addEventListener("click", closeDrawer));
document.querySelectorAll(".tab").forEach((tab) => tab.addEventListener("click", () => activateTab(tab.dataset.tab)));
$("#search").addEventListener("input", debounce((event) => { state.q = event.target.value; state.page = 1; load(); }, 240));
$("#subject").addEventListener("change", (event) => { state.subject = event.target.value; state.page = 1; load(); });
$("#status").addEventListener("change", (event) => { state.status = event.target.value; state.page = 1; load(); });
$("#split").addEventListener("change", (event) => { state.split = event.target.value; state.page = 1; load(); });
$("#reset").addEventListener("click", () => { state.q = ""; state.subject = "all"; state.status = "all"; state.split = "all"; state.page = 1; $("#search").value = ""; $("#subject").value = "all"; $("#status").value = "all"; $("#split").value = "all"; load(); });
$("#prev").addEventListener("click", () => { if (state.page > 1) { state.page -= 1; load(); } });
$("#next").addEventListener("click", () => { if (state.page < 99999) { state.page += 1; load(); } });
document.addEventListener("keydown", (event) => { if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") { event.preventDefault(); $("#search").focus(); } if (event.key === "Escape") closeDrawer(); });

(async () => { renderStats(await api("/gold/summary")); load(); })();

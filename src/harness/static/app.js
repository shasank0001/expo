const state = { page: 1, pageSize: 20, q: "", family: "all", status: "all", record: null };
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

function promptText(record) {
  const user = record.messages.find((message) => message.role === "user");
  return user?.content || "No user prompt";
}

function isToolRecord(record) {
  return record.messages.some((message) => message.role === "assistant" && message.content.includes('"name"'));
}

function renderStats(summary) {
  $("#stat-records").textContent = formatNumber(summary.records);
  $("#stat-sources").textContent = formatNumber(summary.source_notes);
  $("#stat-tools").textContent = formatNumber(summary.tool_call_records);
  $("#stat-html").textContent = formatNumber(summary.html_records);
  $("#dataset-file").textContent = `${formatNumber(summary.records)} records`;
}

function renderFamilyOptions(summary) {
  const select = $("#family");
  Object.entries(summary.families || {}).sort().forEach(([family, count]) => {
    const option = document.createElement("option");
    option.value = family; option.textContent = `${family.replaceAll("_", " ")} · ${formatNumber(count)}`;
    select.append(option);
  });
}

function renderRecords(data) {
  renderStats(data.summary);
  $("#result-count").textContent = `${formatNumber(data.total)} matching case${data.total === 1 ? "" : "s"}`;
  $("#filter-note").textContent = state.q || state.family !== "all" || state.status !== "all" ? "filtered view" : "All generated cases";
  $("#page-label").textContent = `${data.page} / ${data.pages}`;
  $("#prev").disabled = data.page <= 1;
  $("#next").disabled = data.page >= data.pages;
  const list = $("#record-list");
  list.innerHTML = data.items.map((record, index) => {
    const meta = record.metadata || {};
    const tags = [`<span class="tag family">${escapeHtml(meta.task_family || "unknown")}</span>`, `<span class="tag ${meta.source_status === "draft" ? "draft" : ""}">${escapeHtml(meta.source_status || "no source")}</span>`];
    if (isToolRecord(record)) tags.push('<span class="tag tool">tool call</span>');
    if (meta.source_ref?.topic) tags.push(`<span class="tag">${escapeHtml(meta.source_ref.topic)}</span>`);
    return `<article class="record-card" data-record-id="${escapeHtml(record.id)}" style="animation-delay:${index * 35}ms"><div><h3>${escapeHtml(record.id)}</h3><p>${escapeHtml(promptText(record))}</p></div><div class="record-id">${escapeHtml(record.dataset_file || "train.jsonl")}</div><div class="record-tags">${tags.join("")}</div></article>`;
  }).join("");
  $("#empty-state").hidden = data.total !== 0;
}

async function load() {
  const params = new URLSearchParams({ q: state.q, family: state.family, status: state.status, page: state.page, page_size: state.pageSize });
  try { renderRecords(await api(`/data/records?${params}`)); } catch (error) { $("#result-count").textContent = "Could not load archive"; console.error(error); }
}

function messageMarkup(message) {
  const label = message.role.toUpperCase();
  return `<div class="message ${escapeHtml(message.role)}"><div class="message-label">${label}${message.name ? ` / ${escapeHtml(message.name)}` : ""}</div><pre>${escapeHtml(message.content)}</pre></div>`;
}

function openDrawer(record) {
  state.record = record;
  const meta = record.metadata || {};
  $("#drawer-id").textContent = record.id;
  $("#drawer-meta").innerHTML = [meta.task_family, meta.template_id, meta.prompt_id, meta.source_status].filter(Boolean).map((item) => `<span class="tag">${escapeHtml(item)}</span>`).join("");
  $("#conversation-view").innerHTML = record.messages.map(messageMarkup).join("");
  $("#json-view").textContent = JSON.stringify(record, null, 2);
  const assistant = [...record.messages].reverse().find((message) => message.role === "assistant");
  let html = "";
  try { html = JSON.parse(assistant?.content || "{}").html || ""; } catch { /* not an HTML record */ }
  $(".html-frame").innerHTML = html || '<p style="font-family:monospace;color:#666">No HTML output in this case.</p>';
  $("#drawer").classList.add("open"); $("#drawer").setAttribute("aria-hidden", "false"); document.body.style.overflow = "hidden";
  activateTab("conversation");
}

function closeDrawer() { $("#drawer").classList.remove("open"); $("#drawer").setAttribute("aria-hidden", "true"); document.body.style.overflow = ""; }
function activateTab(name) { document.querySelectorAll(".tab").forEach((tab) => tab.classList.toggle("active", tab.dataset.tab === name)); document.querySelectorAll(".tab-panel").forEach((panel) => panel.classList.remove("active")); $(`#${name}-view`).classList.add("active"); }

function debounce(callback, delay) { let timer; return (...args) => { clearTimeout(timer); timer = setTimeout(() => callback(...args), delay); }; }

$("#record-list").addEventListener("click", async (event) => { const card = event.target.closest("[data-record-id]"); if (!card) return; openDrawer(await api(`/data/records/${encodeURIComponent(card.dataset.recordId)}`)); });
document.querySelectorAll("[data-close]").forEach((node) => node.addEventListener("click", closeDrawer));
document.querySelectorAll(".tab").forEach((tab) => tab.addEventListener("click", () => activateTab(tab.dataset.tab)));
$("#search").addEventListener("input", debounce((event) => { state.q = event.target.value; state.page = 1; load(); }, 240));
$("#family").addEventListener("change", (event) => { state.family = event.target.value; state.page = 1; load(); });
$("#status").addEventListener("change", (event) => { state.status = event.target.value; state.page = 1; load(); });
$("#reset").addEventListener("click", () => { state.q = ""; state.family = "all"; state.status = "all"; state.page = 1; $("#search").value = ""; $("#family").value = "all"; $("#status").value = "all"; load(); });
$("#prev").addEventListener("click", () => { if (state.page > 1) { state.page -= 1; load(); } });
$("#next").addEventListener("click", () => { state.page += 1; load(); });
document.addEventListener("keydown", (event) => { if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") { event.preventDefault(); $("#search").focus(); } if (event.key === "Escape") closeDrawer(); });

(async () => { const summary = await api("/data/summary"); renderFamilyOptions(summary); renderStats(summary); load(); })();

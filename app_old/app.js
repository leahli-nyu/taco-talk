// Loads ./data.json and renders. Static, deploys anywhere.

const DATA_URL = "./data.json";

// ============== Theme toggle ==============
const themeBtn = document.getElementById("theme-toggle");
function applyTheme(mode) {
  if (mode === "auto") {
    document.documentElement.removeAttribute("data-theme");
  } else {
    document.documentElement.setAttribute("data-theme", mode);
  }
  localStorage.setItem("theme", mode);
  themeBtn.textContent = mode;
}
themeBtn.addEventListener("click", () => {
  const cur = localStorage.getItem("theme") || "auto";
  const next = cur === "auto" ? "light" : cur === "light" ? "dark" : "auto";
  applyTheme(next);
});
applyTheme(localStorage.getItem("theme") || "auto");

// ============== Helpers ==============
const fmt = (n, d = 0) => (n == null || isNaN(n)) ? "—" :
  Number(n).toLocaleString("en-US", { maximumFractionDigits: d });
const pct = (n, d = 1) => (n == null || isNaN(n)) ? "—" : (n * 100).toFixed(d) + "%";
const carPct = (n) => (n == null || isNaN(n)) ? "—" : (n * 100 >= 0 ? "+" : "") + (n * 100).toFixed(2) + "%";
const escape = (s) => (s ?? "").toString().replace(/[<>&"]/g, c =>
  ({ "<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;" })[c]);

const OUTCOME_LABELS = {
  executed: "Executed",
  modified_or_withdrawn: "Modified / withdrawn",
  struck_down: "Struck down",
  announced_unresolved: "Unresolved",
  investigation: "Investigation",
  other: "Other",
  unmatched: "Unmatched",
};
const OUTCOME_DESC = {
  executed: "Policy enacted in Federal Register",
  modified_or_withdrawn: "Threat softened or retracted (TACO)",
  struck_down: "Invalidated by court / Congress",
  announced_unresolved: "Announced, not yet acted on",
  investigation: "Formal investigation underway",
  other: "Mixed / unclear",
  unmatched: "No policy event found",
};

// ============== Main ==============
async function load() {
  // Prefer inline data (works on file://). Fall back to fetch (works on http://).
  if (window.__APP_DATA__) return window.__APP_DATA__;
  const r = await fetch(DATA_URL);
  if (!r.ok) throw new Error(`data.json: ${r.status}`);
  return r.json();
}

function paintKPIs(d) {
  const s = d.summary, t = d.ticker;
  document.getElementById("meta-date").textContent = s.data_through;
  document.getElementById("meta-n").textContent = fmt(s.n_threats);

  document.getElementById("kpi-threats").textContent = fmt(s.n_threats);
  document.getElementById("kpi-match").textContent = pct(s.match_rate);
  document.getElementById("kpi-exec").textContent = pct(t.execution_rate);
  document.getElementById("kpi-taco").textContent = pct(t.taco_rate);
  document.getElementById("kpi-lead").textContent = (t.median_anticipation_days == null) ? "—" :
    `${t.median_anticipation_days.toFixed(0)}d`;
  const carEl = document.getElementById("kpi-car");
  carEl.textContent = carPct(t.avg_car_30d);
  carEl.classList.toggle("pos", (t.avg_car_30d ?? 0) > 0);
  carEl.classList.toggle("neg", (t.avg_car_30d ?? 0) < 0);
}

function paintOutcomeTable(d) {
  const tbody = document.getElementById("outcome-tbody");
  const total = Object.values(d.outcome_counts || {}).reduce((a, b) => a + b, 0);
  document.getElementById("agg-meta").textContent = `N = ${fmt(total)} threats`;
  tbody.innerHTML = "";
  // Sort by count desc
  const rows = Object.entries(d.outcome_counts).sort((a, b) => b[1] - a[1]);
  const maxN = Math.max(...rows.map(r => r[1]));
  for (const [outcome, n] of rows) {
    const tr = document.createElement("tr");
    const pctW = maxN ? (n / maxN * 100).toFixed(1) : 0;
    tr.innerHTML = `
      <td><span class="tag tag-outcome-${outcome}">${OUTCOME_LABELS[outcome] || outcome}</span></td>
      <td class="num">${fmt(n)}</td>
      <td class="num">${pct(n / total)}</td>
      <td><span class="bar-mini" style="width: ${Math.max(pctW, 2)}%;"></span></td>
      <td class="faint">${OUTCOME_DESC[outcome] || ""}</td>`;
    tbody.appendChild(tr);
  }
}

function paintStats(d) {
  const t = d.ticker, s = d.summary;
  document.getElementById("stat-drawdown").textContent = carPct(t.avg_peak_drawdown_30d);
  document.getElementById("stat-recovery").textContent = carPct(t.avg_max_recovery_30d);
  document.getElementById("stat-anticip").textContent = (t.median_anticipation_days == null) ? "—" :
    `${t.median_anticipation_days.toFixed(1)} d`;
  document.getElementById("stat-eps").textContent = fmt(s.n_episodes);
  document.getElementById("callout-drawdown").textContent = carPct(t.avg_peak_drawdown_30d);
  document.getElementById("callout-recovery").textContent = carPct(t.avg_max_recovery_30d);
}

function paintThreats(d) {
  const tgSel = document.getElementById("filter-target");
  const targets = [...new Set(d.threats.map(t => t.target).filter(Boolean))].sort();
  for (const t of targets) {
    const opt = document.createElement("option");
    opt.value = t; opt.textContent = t;
    tgSel.appendChild(opt);
  }
  const render = () => {
    const oc = document.getElementById("filter-outcome").value;
    const tg = document.getElementById("filter-target").value;
    const sort = document.getElementById("filter-sort").value;
    let rows = d.threats.slice();
    if (oc) rows = rows.filter(t => t.y1_outcome === oc);
    if (tg) rows = rows.filter(t => t.target === tg);
    if (sort === "date_asc")
      rows.sort((a, b) => (a.date || "").localeCompare(b.date || ""));
    else if (sort === "car_30d_desc")
      rows.sort((a, b) => (b.car_30d ?? -999) - (a.car_30d ?? -999));
    else if (sort === "car_30d_asc")
      rows.sort((a, b) => (a.car_30d ?? 999) - (b.car_30d ?? 999));
    else
      rows.sort((a, b) => (b.date || "").localeCompare(a.date || ""));
    document.getElementById("filter-count").textContent = `${fmt(rows.length)} threats`;

    const root = document.getElementById("threats-list");
    root.innerHTML = "";
    rows.slice(0, 60).forEach(t => {
      const c = document.createElement("div");
      c.className = "threat-card";
      const carClass = (t.car_30d ?? 0) > 0 ? "pos" : (t.car_30d ?? 0) < 0 ? "neg" : "";
      c.innerHTML = `
        <div class="threat-head">
          <span class="mono">${escape((t.date || "").slice(0, 16))}</span>
          <span class="tag tag-outcome-${t.y1_outcome || "unmatched"}">${OUTCOME_LABELS[t.y1_outcome] || (t.y1_outcome || "unmatched").replace(/_/g, " ")}</span>
        </div>
        <div class="threat-text">${escape(t.text_preview)}</div>
        <div class="threat-meta">
          ${t.target ? `<span class="tag tag-target">${escape(t.target)}</span>` : ""}
          ${t.car_1d != null ? `<span class="tag tag-num ${(t.car_1d > 0 ? "pos" : "neg")}">SP 1d ${carPct(t.car_1d)}</span>` : ""}
          ${t.car_30d != null ? `<span class="tag tag-num ${carClass}">SP 30d ${carPct(t.car_30d)}</span>` : ""}
        </div>`;
      root.appendChild(c);
    });
  };
  document.getElementById("filter-outcome").addEventListener("change", render);
  document.getElementById("filter-target").addEventListener("change", render);
  document.getElementById("filter-sort").addEventListener("change", render);
  render();
}

load().then(d => {
  paintKPIs(d);
  paintOutcomeTable(d);
  paintStats(d);
  paintThreats(d);
}).catch(err => {
  document.querySelector(".hero .container").insertAdjacentHTML(
    "beforeend",
    `<div class="note" style="border-left-color: var(--danger); background: var(--danger-soft); margin-top: 20px;">
      <strong>data.json not loaded.</strong> Run <code class="mono">python3 src/build_app_data.py</code> in the project root to regenerate.
      <div class="small faint" style="margin-top: 4px;">Error: ${escape(err.message)}</div>
    </div>`
  );
});

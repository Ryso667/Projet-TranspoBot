const API_BASE = '';

async function fetchAPI(path) {
  const res = await fetch(API_BASE + path);
  if (!res.ok) throw new Error(`Erreur ${res.status}`);
  return res.json();
}

function getStatusBadge(statut) {
  const map = {
    actif: '<span class="badge badge-success">Actif</span>',
    inactif: '<span class="badge badge-secondary">Inactif</span>',
    'en service': '<span class="badge badge-success">En service</span>',
    maintenance: '<span class="badge badge-warning">Maintenance</span>',
    'hors service': '<span class="badge badge-danger">Hors service</span>',
    terminé: '<span class="badge badge-info">Terminé</span>',
    'en cours': '<span class="badge badge-success">En cours</span>',
    annulé: '<span class="badge badge-danger">Annulé</span>',
  };
  return map[statut] || `<span class="badge badge-secondary">${statut || 'N/A'}</span>`;
}

function getGraviteBadge(gravite) {
  const map = {
    faible: '<span class="badge badge-success">Faible</span>',
    moyen: '<span class="badge badge-warning">Moyen</span>',
    grave: '<span class="badge badge-danger">Grave</span>',
  };
  return map[gravite] || `<span class="badge badge-secondary">${gravite || 'N/A'}</span>`;
}

function formatDate(dt) {
  if (!dt) return '—';
  return new Date(dt).toLocaleString('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

function showLoading(container) {
  container.innerHTML =
    '<div class="skeleton skeleton-table" style="min-height:160px" aria-hidden="true"></div>';
}

function showError(container, msg) {
  container.innerHTML = `<div class="empty-state"><i class="fa-solid fa-triangle-exclamation" aria-hidden="true"></i> ${msg}</div>`;
}

/** Skeleton cards for KPI row (dashboard). */
function renderKpiSkeletons(container, count = 8) {
  const cells = Array.from({ length: count }, () => '<div class="skeleton skeleton-kpi-card" aria-hidden="true"></div>').join('');
  container.innerHTML = `<div class="skeleton-kpi-grid">${cells}</div>`;
}

/** Animate numeric .kpi-value elements with data-target="number". */
function runKpiCountUp(root) {
  if (!root) return;
  root.querySelectorAll('.kpi-value[data-target]').forEach((el) => {
    const raw = el.getAttribute('data-target');
    const end = parseInt(raw, 10);
    if (Number.isNaN(end)) {
      el.textContent = raw;
      return;
    }
    el.textContent = '0';
    const duration = 950;
    const t0 = performance.now();
    function frame(now) {
      const t = Math.min(1, (now - t0) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      el.textContent = String(Math.round(eased * end));
      if (t < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  });
}

function initLiveClock() {
  const el = document.getElementById('liveClock');
  if (!el) return;
  function tick() {
    el.textContent = new Date().toLocaleTimeString('fr-FR', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    });
  }
  tick();
  setInterval(tick, 1000);
}

function initSidebarToggle() {
  const toggle = document.querySelector('.sidebar-toggle');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');
  if (!toggle || !sidebar) return;

  function close() {
    document.body.classList.remove('sidebar-open');
    toggle.setAttribute('aria-expanded', 'false');
  }

  function open() {
    document.body.classList.add('sidebar-open');
    toggle.setAttribute('aria-expanded', 'true');
  }

  toggle.addEventListener('click', () => {
    if (document.body.classList.contains('sidebar-open')) close();
    else open();
  });
  overlay?.addEventListener('click', close);
  window.addEventListener('resize', () => {
    if (window.innerWidth > 900) close();
  });
}

function initThemeToggle() {
  const btn = document.getElementById('themeToggle');
  if (!btn) return;
  const stored = localStorage.getItem('transpobot-theme');
  if (stored === 'dark') {
    document.documentElement.classList.add('theme-dark');
  } else {
    document.documentElement.classList.remove('theme-dark');
  }
  updateThemeIcon(btn);

  btn.addEventListener('click', () => {
    document.documentElement.classList.toggle('theme-dark');
    const dark = document.documentElement.classList.contains('theme-dark');
    localStorage.setItem('transpobot-theme', dark ? 'dark' : 'light');
    updateThemeIcon(btn);
  });
}

function updateThemeIcon(btn) {
  const dark = document.documentElement.classList.contains('theme-dark');
  btn.innerHTML = dark ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
  btn.setAttribute('title', dark ? 'Passer au thème clair' : 'Passer au thème sombre');
}

function initTabBars() {
  document.querySelectorAll('.tabs-root').forEach((root) => {
    const buttons = root.querySelectorAll('.tab-btn');
    const panels = root.querySelectorAll('.tab-panel');
    buttons.forEach((btn) => {
      btn.addEventListener('click', () => {
        const target = btn.getAttribute('data-tab');
        if (!target) return;
        buttons.forEach((b) => {
          const on = b === btn;
          b.classList.toggle('active', on);
          b.setAttribute('aria-selected', on ? 'true' : 'false');
        });
        panels.forEach((p) => {
          p.classList.toggle('active', p.id === `tab-panel-${target}`);
        });
      });
    });
  });
}

function initTranspoBotShell() {
  initLiveClock();
  initSidebarToggle();
  initThemeToggle();
  initTabBars();
}

document.addEventListener('DOMContentLoaded', initTranspoBotShell);

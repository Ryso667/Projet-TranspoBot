const API_BASE = '';

async function fetchAPI(path) {
  const res = await fetch(API_BASE + path);
  if (!res.ok) throw new Error(`Erreur ${res.status}`);
  return res.json();
}

function getStatusBadge(statut) {
  const map = {
    'actif': '<span class="badge badge-success">Actif</span>',
    'inactif': '<span class="badge badge-secondary">Inactif</span>',
    'en service': '<span class="badge badge-success">En service</span>',
    'maintenance': '<span class="badge badge-warning">Maintenance</span>',
    'hors service': '<span class="badge badge-danger">Hors service</span>',
    'terminé': '<span class="badge badge-info">Terminé</span>',
    'en cours': '<span class="badge badge-success">En cours</span>',
    'annulé': '<span class="badge badge-danger">Annulé</span>',
  };
  return map[statut] || `<span class="badge badge-secondary">${statut || 'N/A'}</span>`;
}

function getGraviteBadge(gravite) {
  const map = {
    'faible': '<span class="badge badge-success">Faible</span>',
    'moyen': '<span class="badge badge-warning">Moyen</span>',
    'grave': '<span class="badge badge-danger">Grave</span>',
  };
  return map[gravite] || `<span class="badge badge-secondary">${gravite || 'N/A'}</span>`;
}

function formatDate(dt) {
  if (!dt) return '—';
  return new Date(dt).toLocaleString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' });
}

function showLoading(container) {
  container.innerHTML = '<div class="loading"><div class="spinner"></div> Chargement...</div>';
}

function showError(container, msg) {
  container.innerHTML = `<div class="empty-state">⚠️ ${msg}</div>`;
}

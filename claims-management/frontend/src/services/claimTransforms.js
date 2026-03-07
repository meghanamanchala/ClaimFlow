export function formatCurrency(amount) {
  return `$${Number(amount || 0).toLocaleString()}`;
}

export function formatDate(value) {
  if (!value) {
    return 'Pending';
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return String(value);
  }

  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
}

export function toTitleCase(value) {
  return String(value || '')
    .replaceAll('_', ' ')
    .replace(/\b\w/g, (ch) => ch.toUpperCase());
}

export function getStatusLabel(status) {
  const normalized = String(status || '').toLowerCase();

  if (normalized === 'submitted') {
    return 'Pending';
  }

  if (normalized === 'under_review') {
    return 'Under Review';
  }

  return toTitleCase(normalized || 'unknown');
}

export function getStatusClass(status) {
  const normalized = String(status || '').toLowerCase();

  if (normalized === 'approved' || normalized === 'paid') {
    return 'badge-approved';
  }

  if (normalized === 'rejected') {
    return 'badge-rejected';
  }

  if (normalized === 'under_review') {
    return 'badge-review';
  }

  return 'badge-pending';
}

export function getPriorityClass(priority) {
  const normalized = String(priority || '').toLowerCase();

  if (normalized === 'high') {
    return 'badge-priority-high';
  }

  if (normalized === 'medium') {
    return 'badge-priority-medium';
  }

  return 'badge-priority-low';
}

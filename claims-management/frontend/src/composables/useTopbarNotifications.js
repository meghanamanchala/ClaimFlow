import { computed, onBeforeUnmount, onMounted, ref } from 'vue';
import { getClaims, getMessages } from '../services/api';

function toTime(value) {
  const date = new Date(value || 0);
  const time = date.getTime();
  return Number.isNaN(time) ? 0 : time;
}

function toRelativeTime(value) {
  const timestamp = toTime(value);
  if (!timestamp) {
    return 'Now';
  }

  const diffMs = Math.max(0, Date.now() - timestamp);
  const minute = 60 * 1000;
  const hour = 60 * minute;
  const day = 24 * hour;

  if (diffMs < minute) {
    return 'Just now';
  }

  if (diffMs < hour) {
    return `${Math.floor(diffMs / minute)}m ago`;
  }

  if (diffMs < day) {
    return `${Math.floor(diffMs / hour)}h ago`;
  }

  return `${Math.floor(diffMs / day)}d ago`;
}

function normalizeStatus(status) {
  const raw = String(status || '').toLowerCase();
  if (!raw) {
    return 'updated';
  }

  return raw.replaceAll('_', ' ');
}

export function useTopbarNotifications(roleKey) {
  const AUTO_REFRESH_MS = 10 * 1000;
  const notificationsRef = ref(null);
  const showNotifications = ref(false);
  const notifications = ref([]);
  const lastSeenKey = `claimflow_notifications_last_seen_${roleKey}`;
  let refreshTimer = null;
  let isLoading = false;

  const hasUnreadNotifications = computed(() => notifications.value.some((item) => !item.read));

  function getLastSeen() {
    return Number(localStorage.getItem(lastSeenKey) || '0');
  }

  function markAllRead() {
    const now = Date.now();
    localStorage.setItem(lastSeenKey, String(now));
    notifications.value = notifications.value.map((item) => ({ ...item, read: true }));
  }

  function mapNotifications(claims, messages) {
    const claimItems = (claims || []).map((claim) => {
      const timestampValue = claim.reviewedAt || claim.approvedAt || claim.resolvedAt || claim.createdAt || claim.incidentDate;
      return {
        id: `claim-${claim.id}`,
        title: 'Claim Status Updated',
        message: `${claim.claimNumber || `Claim #${claim.id}`} is ${normalizeStatus(claim.status)}.`,
        timestamp: toTime(timestampValue),
      };
    });

    const messageItems = (messages || []).map((message) => ({
      id: `message-${message.id}`,
      title: `Message from ${message.senderName || 'User'}`,
      message: message.content || 'You have a new message update.',
      timestamp: toTime(message.createdAt),
    }));

    const merged = [...claimItems, ...messageItems]
      .filter((item) => item.timestamp > 0)
      .sort((a, b) => b.timestamp - a.timestamp)
      .slice(0, 8);

    const lastSeen = getLastSeen();

    return merged.map((item) => ({
      ...item,
      time: toRelativeTime(item.timestamp),
      read: item.timestamp <= lastSeen,
    }));
  }

  async function loadNotifications() {
    if (isLoading) {
      return;
    }

    isLoading = true;
    try {
      const [claimsResponse, messagesResponse] = await Promise.all([getClaims(), getMessages()]);
      notifications.value = mapNotifications(claimsResponse.data || [], messagesResponse.data || []);
    } catch {
      notifications.value = [];
    } finally {
      isLoading = false;
    }
  }

  function toggleNotifications() {
    showNotifications.value = !showNotifications.value;
  }

  function handleOutsideNotificationClick(event) {
    if (!notificationsRef.value?.contains(event.target)) {
      showNotifications.value = false;
    }
  }

  onMounted(() => {
    loadNotifications();
    refreshTimer = window.setInterval(loadNotifications, AUTO_REFRESH_MS);
    document.addEventListener('click', handleOutsideNotificationClick);
  });

  onBeforeUnmount(() => {
    if (refreshTimer) {
      window.clearInterval(refreshTimer);
      refreshTimer = null;
    }
    document.removeEventListener('click', handleOutsideNotificationClick);
  });

  return {
    notificationsRef,
    showNotifications,
    notifications,
    hasUnreadNotifications,
    toggleNotifications,
    markAllRead,
    loadNotifications,
  };
}

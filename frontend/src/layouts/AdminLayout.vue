<template>
  <div class="policyholder-shell" :class="{ 'is-sidebar-collapsed': isSidebarCollapsed }">
    <aside class="dashboard-sidebar">
      <div class="sidebar-brand">
        <div class="brand-badge" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 3l7 4v5c0 5-3.2 8-7 9-3.8-1-7-4-7-9V7z"></path>
          </svg>
        </div>
        <div class="brand-text">ClaimFlow</div>
      </div>

      <div class="sidebar-nav-wrap">
        <p class="sidebar-label">Navigation</p>
        <nav class="sidebar-nav">
          <RouterLink
            v-for="item in navItems"
            :key="item.to"
            :to="item.to"
            class="sidebar-link"
            :title="isSidebarCollapsed ? item.label : ''"
          >
            <span class="sidebar-link-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path v-for="(segment, index) in item.iconPaths" :key="index" :d="segment"></path>
              </svg>
            </span>
            <span class="sidebar-link-label">{{ item.label }}</span>
          </RouterLink>
        </nav>
      </div>

      <p class="sidebar-copyright">(c) 2026 ClaimFlow Inc.</p>
    </aside>

    <div class="dashboard-main">
      <header class="dashboard-topbar">
        <div class="topbar-breadcrumb">
          <button
            type="button"
            class="sidebar-toggle-btn"
            @click="toggleSidebar"
            :aria-expanded="String(!isSidebarCollapsed)"
            aria-label="Toggle navigation sidebar"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <rect x="3" y="5" width="18" height="14" rx="2"></rect>
              <path d="M9 5v14"></path>
            </svg>
          </button>
          <span>Admin Dashboard</span>
        </div>

        <div class="topbar-user-block">
          <div class="topbar-notifications" ref="notificationsRef">
            <button
              type="button"
              class="topbar-bell"
              :class="{ 'is-open': showNotifications }"
              aria-label="Open notifications"
              @click="handleBellClick"
              @dblclick.stop="handleBellDoubleClick"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M15 17h5l-1.4-1.4a2 2 0 0 1-.6-1.4V11a6 6 0 1 0-12 0v3.2a2 2 0 0 1-.6 1.4L4 17h5"></path>
                <path d="M9 17a3 3 0 0 0 6 0"></path>
              </svg>
              <span v-if="hasUnreadNotifications" class="notification-dot"></span>
            </button>

            <div v-if="showNotifications" class="topbar-notifications-panel">
              <div class="notifications-head">
                <p>Notifications</p>
                <button type="button" @click="markAllRead">Mark all read</button>
              </div>

              <ul class="notification-list" v-if="notifications.length">
                <li
                  v-for="item in notifications"
                  :key="item.id"
                  class="notification-item"
                  :class="{ 'is-unread': !item.read }"
                >
                  <p class="notification-title">{{ item.title }}</p>
                  <p class="notification-copy">{{ item.message }}</p>
                  <p class="notification-time">{{ item.time }}</p>
                </li>
              </ul>

              <p v-else class="notification-empty">No notifications yet.</p>
            </div>
          </div>

          <div class="topbar-avatar">{{ avatarInitials }}</div>
          <RouterLink to="/admin/profile" class="topbar-name topbar-name-link">{{ displayName }}</RouterLink>
          <button type="button" class="topbar-logout" @click="logout" aria-label="Logout">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M10 17l5-5-5-5"></path>
              <path d="M15 12H3"></path>
              <path d="M21 3v18"></path>
            </svg>
          </button>
        </div>
      </header>

      <main class="dashboard-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useNavbarProfile } from '../composables/useNavbarProfile';
import { useTopbarNotifications } from '../composables/useTopbarNotifications';

const router = useRouter();
const { displayName, avatarInitials } = useNavbarProfile();
const {
  notificationsRef,
  showNotifications,
  notifications,
  hasUnreadNotifications,
  toggleNotifications,
  markAllRead,
} = useTopbarNotifications('admin');
const SIDEBAR_STATE_KEY = 'claimflow_sidebar_collapsed';
const isSidebarCollapsed = ref(false);
let bellClickTimer = null;

const navItems = [
  {
    to: '/admin/dashboard',
    label: 'Dashboard',
    iconPaths: ['M3 12l9-9 9 9', 'M5 10v10h5v-6h4v6h5V10'],
  },
  {
    to: '/admin/all-claims',
    label: 'All Claims',
    iconPaths: ['M14 2H7a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z', 'M14 2v6h6', 'M9 13h6', 'M9 17h6'],
  },
  {
    to: '/admin/user-management',
    label: 'User Management',
    iconPaths: ['M16 21v-2a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v2', 'M9.5 7a3 3 0 1 0 0 6 3 3 0 0 0 0-6', 'M19 8v6', 'M16 11h6'],
  },
  {
    to: '/admin/analytics',
    label: 'Analytics',
    iconPaths: ['M18 20V10', 'M12 20V4', 'M6 20v-6'],
  },
  {
    to: '/admin/permissions',
    label: 'Permissions',
    iconPaths: ['M12 3l7 4v5c0 5-3.2 8-7 9-3.8-1-7-4-7-9V7z', 'M9.5 12l2 2 3.5-4'],
  },
  {
    to: '/admin/settings',
    label: 'Settings',
    iconPaths: ['M12 2v2', 'M12 20v2', 'M4.93 4.93l1.41 1.41', 'M17.66 17.66l1.41 1.41', 'M2 12h2', 'M20 12h2', 'M4.93 19.07l1.41-1.41', 'M17.66 6.34l1.41-1.41', 'M12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8'],
  },
];

onMounted(() => {
  isSidebarCollapsed.value = localStorage.getItem(SIDEBAR_STATE_KEY) === 'true';
});

onBeforeUnmount(() => {
  if (bellClickTimer) {
    window.clearTimeout(bellClickTimer);
    bellClickTimer = null;
  }
});

function toggleSidebar() {
  isSidebarCollapsed.value = !isSidebarCollapsed.value;
  localStorage.setItem(SIDEBAR_STATE_KEY, String(isSidebarCollapsed.value));
}

function goToNotifications() {
  router.push('/admin/notifications');
}

function handleBellClick() {
  if (bellClickTimer) {
    window.clearTimeout(bellClickTimer);
  }

  bellClickTimer = window.setTimeout(() => {
    toggleNotifications();
    bellClickTimer = null;
  }, 220);
}

function handleBellDoubleClick() {
  if (bellClickTimer) {
    window.clearTimeout(bellClickTimer);
    bellClickTimer = null;
  }
  goToNotifications();
}

function logout() {
  localStorage.removeItem('claimflow_token');
  localStorage.removeItem('claimflow_role');
  router.replace('/login');
}
</script>

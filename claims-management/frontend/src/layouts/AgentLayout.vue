<template>
  <div class="policyholder-shell">
    <aside class="dashboard-sidebar">
      <div class="sidebar-brand">
        <div class="brand-badge">O</div>
        <div class="brand-text">ClaimFlow</div>
      </div>

      <div class="sidebar-nav-wrap">
        <p class="sidebar-label">Navigation</p>
        <nav class="sidebar-nav">
          <RouterLink to="/agent/dashboard" class="sidebar-link">Dashboard</RouterLink>
          <RouterLink to="/agent/assigned-claims" class="sidebar-link">Assigned Claims</RouterLink>
          <RouterLink to="/agent/review-claims" class="sidebar-link">Review Claims</RouterLink>
          <RouterLink to="/agent/messages" class="sidebar-link">Messages</RouterLink>
        </nav>
      </div>

      <p class="sidebar-copyright">(c) 2026 ClaimFlow Inc.</p>
    </aside>

    <div class="dashboard-main">
      <header class="dashboard-topbar">
        <div class="topbar-breadcrumb">Agent Dashboard</div>

        <div class="topbar-user-block">
          <button type="button" class="topbar-bell" aria-label="Open notifications">
            <span class="notification-dot"></span>
          </button>
          <div class="topbar-avatar">{{ avatarInitials }}</div>
          <RouterLink to="/agent/profile" class="topbar-name topbar-name-link">{{ displayName }}</RouterLink>
          <button type="button" class="topbar-logout" @click="logout">Logout</button>
        </div>
      </header>

      <main class="dashboard-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useNavbarProfile } from '../composables/useNavbarProfile';

const router = useRouter();
const { displayName, avatarInitials } = useNavbarProfile();

function logout() {
  localStorage.removeItem('claimflow_token');
  localStorage.removeItem('claimflow_role');
  router.replace('/login');
}
</script>

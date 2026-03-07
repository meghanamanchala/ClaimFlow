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
          <RouterLink to="/admin/dashboard" class="sidebar-link">Dashboard</RouterLink>
          <RouterLink to="/admin/all-claims" class="sidebar-link">All Claims</RouterLink>
          <RouterLink to="/admin/user-management" class="sidebar-link">User Management</RouterLink>
          <RouterLink to="/admin/analytics" class="sidebar-link">Analytics</RouterLink>
          <RouterLink to="/admin/permissions" class="sidebar-link">Permissions</RouterLink>
          <RouterLink to="/admin/settings" class="sidebar-link">Settings</RouterLink>
        </nav>
      </div>

      <p class="sidebar-copyright">(c) 2026 ClaimFlow Inc.</p>
    </aside>

    <div class="dashboard-main">
      <header class="dashboard-topbar">
        <div class="topbar-breadcrumb">Admin Dashboard</div>

        <div class="topbar-user-block">
          <button type="button" class="topbar-bell" aria-label="Open notifications">
            <span class="notification-dot"></span>
          </button>
          <div class="topbar-avatar">AU</div>
          <span class="topbar-name">Admin User</span>
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

const router = useRouter();

function logout() {
  localStorage.removeItem('claimflow_token');
  localStorage.removeItem('claimflow_role');
  router.replace('/login');
}
</script>

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
          <RouterLink to="/dashboard" class="sidebar-link">
            <span>Dashboard</span>
          </RouterLink>
          <RouterLink to="/submit-claim" class="sidebar-link">
            <span>Submit Claim</span>
          </RouterLink>
          <RouterLink to="/my-claims" class="sidebar-link">
            <span>My Claims</span>
          </RouterLink>
          <RouterLink to="/documents" class="sidebar-link">
            <span>Documents</span>
          </RouterLink>
          <RouterLink to="/claim-history" class="sidebar-link">
            <span>Claim History</span>
          </RouterLink>
        </nav>
      </div>

      <p class="sidebar-copyright">(c) 2026 ClaimFlow Inc.</p>
    </aside>

    <div class="dashboard-main">
      <header class="dashboard-topbar">
        <div class="topbar-breadcrumb">Policyholder Dashboard</div>

        <div class="topbar-user-block">
          <button type="button" class="topbar-bell" aria-label="Open notifications">
            <span class="notification-dot"></span>
          </button>
          <div class="topbar-avatar">SM</div>
          <span class="topbar-name">Sarah Mitchell</span>
        </div>
      </header>

      <main class="dashboard-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

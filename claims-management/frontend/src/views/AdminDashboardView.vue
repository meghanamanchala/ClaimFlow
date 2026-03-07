<template>
  <section>
    <header class="page-head">
      <h1>Admin Dashboard</h1>
      <p>System overview and management</p>
    </header>

    <section class="stat-grid">
      <article class="stat-card">
        <p class="stat-title">Total Claims</p>
        <p class="stat-value">156</p>
        <p class="stat-note positive">+12% this month</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Active Users</p>
        <p class="stat-value">342</p>
        <p class="stat-note positive">+8%</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Agents Online</p>
        <p class="stat-value">8</p>
        <p class="stat-note">of 12 total</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Avg Processing</p>
        <p class="stat-value">2.4 days</p>
        <p class="stat-note positive">-0.3 days</p>
      </article>
    </section>

    <section class="dashboard-grid admin-grid">
      <article class="panel">
        <div class="panel-head-row">
          <h2>All Claims</h2>
          <button type="button" class="ghost-btn">Export</button>
        </div>

        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Policyholder</th>
              <th>Agent</th>
              <th>Type</th>
              <th>Amount</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="claim in claims" :key="claim.id">
              <td><a href="#" @click.prevent>{{ claim.id }}</a></td>
              <td>{{ claim.policyholder }}</td>
              <td>{{ claim.agent }}</td>
              <td>{{ claim.type }}</td>
              <td>{{ claim.amount }}</td>
              <td><span class="badge" :class="claim.statusClass">{{ claim.status }}</span></td>
            </tr>
          </tbody>
        </table>
      </article>

      <article class="panel">
        <h2>Claim Distribution</h2>

        <div class="distribution-item" v-for="item in distribution" :key="item.label">
          <div class="distribution-row">
            <span>{{ item.label }}</span>
            <span>{{ item.percent }}%</span>
          </div>
          <div class="distribution-track">
            <div class="distribution-fill" :style="{ width: `${item.percent}%`, background: item.color }"></div>
          </div>
        </div>
      </article>
    </section>
  </section>
</template>

<script setup>
const claims = [
  { id: 'CLM-2024-001', policyholder: 'Sarah Mitchell', agent: 'James Carter', type: 'Auto', amount: '$4,500', status: 'Under Review', statusClass: 'badge-review' },
  { id: 'CLM-2024-002', policyholder: 'Sarah Mitchell', agent: 'James Carter', type: 'Health', amount: '$1,200', status: 'Approved', statusClass: 'badge-approved' },
  { id: 'CLM-2024-004', policyholder: 'John Davis', agent: 'James Carter', type: 'Health', amount: '$2,800', status: 'Pending', statusClass: 'badge-pending' },
  { id: 'CLM-2024-005', policyholder: 'Emily Brown', agent: 'Lisa Anderson', type: 'Property', amount: '$18,500', status: 'Under Review', statusClass: 'badge-review' },
  { id: 'CLM-2024-007', policyholder: 'Tom Harris', agent: 'Lisa Anderson', type: 'Life', amount: '$50,000', status: 'Rejected', statusClass: 'badge-rejected' }
];

const distribution = [
  { label: 'Pending', percent: 25, color: '#f59e0b' },
  { label: 'Under Review', percent: 40, color: '#0ea5e9' },
  { label: 'Approved', percent: 65, color: '#22c55e' },
  { label: 'Rejected', percent: 15, color: '#ef4444' }
];
</script>

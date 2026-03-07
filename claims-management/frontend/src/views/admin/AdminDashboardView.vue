<template>
  <section>
    <header class="page-head">
      <h1>Admin Dashboard</h1>
      <p>System overview and management</p>
    </header>

    <section class="stat-grid">
      <article class="stat-card">
        <p class="stat-title">Total Claims</p>
        <p class="stat-value">{{ stats.totalClaims }}</p>
        <p class="stat-note positive">Live from backend</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Active Users</p>
        <p class="stat-value">{{ stats.activeUsers }}</p>
        <p class="stat-note positive">Non-inactive accounts</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Agents Online</p>
        <p class="stat-value">{{ stats.agentsOnline }}</p>
        <p class="stat-note">of {{ stats.totalAgents }} agents</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Avg Processing</p>
        <p class="stat-value">{{ stats.avgProcessing }}</p>
        <p class="stat-note">From claim timeline</p>
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
            <tr v-for="claim in previewClaims" :key="claim.id">
              <td><a href="#" @click.prevent>{{ claim.claimNumber }}</a></td>
              <td>User #{{ claim.userId }}</td>
              <td>{{ claim.agentId ? `Agent #${claim.agentId}` : '-' }}</td>
              <td>{{ claim.claimType }}</td>
              <td>{{ formatCurrency(claim.estimatedAmount) }}</td>
              <td><span class="badge" :class="getStatusClass(claim.status)">{{ getStatusLabel(claim.status) }}</span></td>
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
import { computed, onMounted, ref } from 'vue';
import { getClaims, getUsers } from '../../services/api';
import { formatCurrency, getStatusClass, getStatusLabel } from '../../services/claimTransforms';

const claims = ref([]);
const users = ref([]);

const previewClaims = computed(() => {
  return [...claims.value]
    .sort((a, b) => new Date(b.createdAt || b.incidentDate) - new Date(a.createdAt || a.incidentDate))
    .slice(0, 6);
});

const stats = computed(() => {
  const totalClaims = claims.value.length;
  const activeUsers = users.value.filter((user) => String(user.status || '').toLowerCase() !== 'inactive').length;
  const totalAgents = users.value.filter((user) => String(user.role || '').toLowerCase() === 'agent').length;
  const agentsOnline = users.value.filter((user) => String(user.role || '').toLowerCase() === 'agent' && user.isOnline).length;

  const completed = claims.value.filter((claim) => claim.timeline?.length > 1);
  const avgDays = completed.length
    ? completed.reduce((sum, claim) => {
        const first = new Date(claim.timeline[0]?.date);
        const last = new Date(claim.timeline[claim.timeline.length - 1]?.date);
        const days = Math.max(0, (last - first) / (1000 * 60 * 60 * 24));
        return sum + days;
      }, 0) / completed.length
    : 0;

  return {
    totalClaims,
    activeUsers,
    totalAgents,
    agentsOnline,
    avgProcessing: `${avgDays.toFixed(1)} days`
  };
});

const distribution = computed(() => {
  const colorMap = {
    Pending: '#f59e0b',
    'Under Review': '#0ea5e9',
    Approved: '#22c55e',
    Rejected: '#ef4444'
  };

  const total = claims.value.length || 1;
  const groups = {
    Pending: 0,
    'Under Review': 0,
    Approved: 0,
    Rejected: 0
  };

  claims.value.forEach((claim) => {
    const status = getStatusLabel(claim.status);
    if (groups[status] !== undefined) {
      groups[status] += 1;
    }
  });

  return Object.entries(groups).map(([label, count]) => ({
    label,
    percent: Math.round((count / total) * 100),
    color: colorMap[label]
  }));
});

onMounted(async () => {
  try {
    const [claimsResponse, usersResponse] = await Promise.all([getClaims(), getUsers()]);
    claims.value = claimsResponse.data || [];
    users.value = usersResponse.data || [];
  } catch {
    claims.value = [];
    users.value = [];
  }
});
</script>

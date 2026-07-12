<template>
  <section>
    <header class="page-head page-head-row">
      <div>
        <h1>All Claims</h1>
        <p>View and manage all claims across the system</p>
      </div>
      <button type="button" class="ghost-btn">Export</button>
    </header>

    <div class="toolbar-row">
      <input v-model="search" class="search-input" type="text" placeholder="Search claims..." />
      <select v-model="statusFilter" class="filter-select">
        <option value="all">All Status</option>
        <option value="under_review">Under Review</option>
        <option value="approved">Approved</option>
        <option value="submitted">Pending</option>
        <option value="rejected">Rejected</option>
      </select>
      <select v-model="agentFilter" class="filter-select">
        <option value="all">All Agents</option>
        <option v-for="agent in agentOptions" :key="agent" :value="agent">{{ agent }}</option>
      </select>
    </div>

    <article class="panel">
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Policyholder</th>
            <th>Agent</th>
            <th>Type</th>
            <th>Amount</th>
            <th>Date</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="claim in filteredClaims" :key="claim.id">
            <td><a href="#" @click.prevent>{{ claim.claimNumber }}</a></td>
            <td>User #{{ claim.userId }}</td>
            <td>{{ claim.agentId ? `Agent #${claim.agentId}` : '-' }}</td>
            <td>{{ claim.claimType }}</td>
            <td>{{ formatCurrency(claim.estimatedAmount) }}</td>
            <td>{{ formatDate(claim.incidentDate) }}</td>
            <td><span class="badge" :class="getStatusClass(claim.status)">{{ getStatusLabel(claim.status) }}</span></td>
            <td><a href="#" class="link-btn" @click.prevent>View</a></td>
          </tr>
        </tbody>
      </table>
      <p v-if="!filteredClaims.length" class="empty-state">No claims found.</p>
    </article>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { getClaims } from '../../services/api';
import { formatCurrency, formatDate, getStatusClass, getStatusLabel } from '../../services/claimTransforms';

const search = ref('');
const statusFilter = ref('all');
const agentFilter = ref('all');
const claims = ref([]);

const agentOptions = computed(() => {
  const ids = [...new Set(claims.value.filter((claim) => claim.agentId).map((claim) => `Agent #${claim.agentId}`))];
  return ids;
});

const filteredClaims = computed(() => {
  const q = search.value.trim().toLowerCase();

  return claims.value.filter((claim) => {
    const matchesSearch = !q || `${claim.claimNumber} ${claim.claimType} user ${claim.userId}`.toLowerCase().includes(q);
    const matchesStatus = statusFilter.value === 'all' || String(claim.status || '').toLowerCase() === statusFilter.value;
    const agentLabel = claim.agentId ? `Agent #${claim.agentId}` : '-';
    const matchesAgent = agentFilter.value === 'all' || agentLabel === agentFilter.value;
    return matchesSearch && matchesStatus && matchesAgent;
  });
});

onMounted(async () => {
  try {
    const { data } = await getClaims();
    claims.value = data || [];
  } catch {
    claims.value = [];
  }
});
</script>

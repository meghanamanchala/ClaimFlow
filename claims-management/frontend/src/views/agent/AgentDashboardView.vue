<template>
  <section>
    <header class="page-head">
      <h1>Agent Dashboard</h1>
      <p>Manage and review your assigned claims</p>
    </header>

    <section class="stat-grid">
      <article class="stat-card">
        <p class="stat-title">Assigned Claims</p>
        <p class="stat-value">{{ stats.assigned }}</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Pending Review</p>
        <p class="stat-value">{{ stats.pendingReview }}</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Resolved Today</p>
        <p class="stat-value">{{ stats.resolvedToday }}</p>
        <p class="stat-note positive">Claims finalized today</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Active Policyholders</p>
        <p class="stat-value">{{ stats.activePolicyholders }}</p>
      </article>
    </section>

    <article class="panel">
      <div class="panel-head-row">
        <h2>Assigned Claims</h2>
        <RouterLink class="ghost-link" to="/agent/assigned-claims">View All</RouterLink>
      </div>

      <p v-if="loading" class="empty-state">Loading claims...</p>
      <p v-else-if="errorMessage" class="message error">{{ errorMessage }}</p>

      <table v-else class="data-table">
        <thead>
          <tr>
            <th>Claim ID</th>
            <th>Policyholder</th>
            <th>Type</th>
            <th>Amount</th>
            <th>Priority</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="claim in previewClaims" :key="claim.id">
            <td><a href="#" @click.prevent>{{ claim.claimNumber }}</a></td>
            <td>User #{{ claim.userId }}</td>
            <td>{{ claim.claimType }}</td>
            <td>{{ formatCurrency(claim.estimatedAmount) }}</td>
            <td><span class="badge" :class="getPriorityClass(claim.priority)">{{ claim.priority }}</span></td>
            <td><span class="badge" :class="getStatusClass(claim.status)">{{ getStatusLabel(claim.status) }}</span></td>
            <td>
              <RouterLink :to="{ path: '/agent/review-claims', query: { claimId: claim.id } }" class="link-btn">Review</RouterLink>
            </td>
          </tr>
          <tr v-if="previewClaims.length === 0">
            <td colspan="7" class="empty-state">No claims available.</td>
          </tr>
        </tbody>
      </table>
    </article>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { getClaims } from '../../services/api';
import { formatCurrency, getPriorityClass, getStatusClass, getStatusLabel } from '../../services/claimTransforms';

const claims = ref([]);
const loading = ref(true);
const errorMessage = ref('');

const previewClaims = computed(() => {
  return [...claims.value]
    .sort((a, b) => new Date(b.createdAt || b.incidentDate) - new Date(a.createdAt || a.incidentDate))
    .slice(0, 6);
});

const stats = computed(() => {
  const all = claims.value;
  const assigned = all.length;
  const pendingReview = all.filter((claim) => String(claim.status || '').toLowerCase() === 'under_review').length;
  const resolvedToday = all.filter((claim) => {
    const status = String(claim.status || '').toLowerCase();
    const resolvedAt = claim.resolvedAt || claim.reviewedAt || claim.approvedAt;
    if (!['approved', 'rejected', 'paid'].includes(status) || !resolvedAt) {
      return false;
    }

    const date = new Date(resolvedAt);
    const now = new Date();
    return date.toDateString() === now.toDateString();
  }).length;
  const activePolicyholders = new Set(all.map((claim) => claim.userId)).size;

  return { assigned, pendingReview, resolvedToday, activePolicyholders };
});

onMounted(async () => {
  loading.value = true;
  errorMessage.value = '';

  try {
    const { data } = await getClaims();
    claims.value = data || [];
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Unable to load assigned claims.';
  } finally {
    loading.value = false;
  }
});
</script>

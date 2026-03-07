<template>
  <section>
    <header class="page-head">
      <h1>Welcome back{{ displayName ? `, ${displayName}` : '' }}</h1>
      <p>Here&apos;s an overview of your insurance claims</p>
    </header>

    <section class="stat-grid">
      <article class="stat-card">
        <p class="stat-title">Active Claims</p>
        <p class="stat-value">{{ stats.active }}</p>
        <p class="stat-note">In progress claims</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Pending Review</p>
        <p class="stat-value">{{ stats.pendingReview }}</p>
        <p class="stat-note">Awaiting agent decision</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Approved</p>
        <p class="stat-value">{{ stats.approved }}</p>
        <p class="stat-note positive">Resolved successfully</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Total Claimed</p>
        <p class="stat-value">{{ stats.totalClaimed }}</p>
        <p class="stat-note">Across all claims</p>
      </article>
    </section>

    <section class="dashboard-grid">
      <article class="panel">
        <h2>Recent Claims</h2>
        <p v-if="loading" class="empty-state">Loading claims...</p>
        <p v-else-if="errorMessage" class="message error">{{ errorMessage }}</p>

        <table v-else class="data-table">
          <thead>
            <tr>
              <th>Claim ID</th>
              <th>Type</th>
              <th>Date</th>
              <th>Amount</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="claim in recentClaims" :key="claim.id">
              <td><a href="#" @click.prevent>{{ claim.claimNumber }}</a></td>
              <td>{{ claim.claimType }}</td>
              <td>{{ formatDate(claim.incidentDate) }}</td>
              <td>{{ formatCurrency(claim.estimatedAmount) }}</td>
              <td><span class="badge" :class="getStatusClass(claim.status)">{{ getStatusLabel(claim.status) }}</span></td>
            </tr>
            <tr v-if="recentClaims.length === 0">
              <td colspan="5" class="empty-state">No claims found yet.</td>
            </tr>
          </tbody>
        </table>
      </article>

      <article class="panel">
        <h2>Claim Progress</h2>
        <ol class="progress-list">
          <li v-for="step in progressTimeline" :key="`${step.step}-${step.date}`" class="progress-item">
            <div class="progress-dot" :class="step.state"></div>
            <div>
              <p class="progress-title">{{ step.step }}</p>
              <p class="progress-date">{{ formatDate(step.date) }}</p>
            </div>
          </li>
          <li v-if="progressTimeline.length === 0" class="empty-state">No timeline data available.</li>
        </ol>
      </article>
    </section>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { getClaims, getMe } from '../../services/api';
import { formatCurrency, formatDate, getStatusClass, getStatusLabel } from '../../services/claimTransforms';

const claims = ref([]);
const displayName = ref('');
const loading = ref(true);
const errorMessage = ref('');

const recentClaims = computed(() => {
  return [...claims.value]
    .sort((a, b) => new Date(b.createdAt || b.incidentDate) - new Date(a.createdAt || a.incidentDate))
    .slice(0, 5);
});

const progressTimeline = computed(() => {
  const latestClaim = recentClaims.value[0];
  if (!latestClaim) {
    return [];
  }

  const timeline = latestClaim.timeline || [];
  if (timeline.length === 0) {
    return [];
  }

  return timeline.map((item, index) => {
    const isLast = index === timeline.length - 1;
    return {
      ...item,
      state: isLast ? 'is-active' : 'is-done'
    };
  });
});

const stats = computed(() => {
  const all = claims.value;
  const activeStatuses = new Set(['submitted', 'documents_verified', 'verified', 'under_review']);

  const active = all.filter((claim) => activeStatuses.has(String(claim.status || '').toLowerCase())).length;
  const pendingReview = all.filter((claim) => String(claim.status || '').toLowerCase() === 'under_review').length;
  const approved = all.filter((claim) => ['approved', 'paid'].includes(String(claim.status || '').toLowerCase())).length;
  const totalClaimed = formatCurrency(all.reduce((sum, claim) => sum + Number(claim.estimatedAmount || 0), 0));

  return { active, pendingReview, approved, totalClaimed };
});

onMounted(async () => {
  loading.value = true;
  errorMessage.value = '';

  try {
    const [claimsResponse, meResponse] = await Promise.all([getClaims(), getMe()]);
    claims.value = claimsResponse.data || [];

    const email = meResponse.data?.email || '';
    displayName.value = email ? email.split('@')[0] : '';
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Unable to load dashboard data.';
  } finally {
    loading.value = false;
  }
});
</script>

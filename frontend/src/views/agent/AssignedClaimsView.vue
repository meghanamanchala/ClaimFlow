<template>
  <section>
    <header class="page-head">
      <h1>Assigned Claims</h1>
      <p>Claims assigned to you for review and processing</p>
    </header>

    <div class="toolbar-row">
      <input v-model="query" class="search-input" type="text" placeholder="Search by claim ID or policyholder..." />
      <select v-model="statusFilter" class="filter-select">
        <option value="all">All Status</option>
        <option value="under_review">Under Review</option>
        <option value="submitted">Pending</option>
        <option value="approved">Approved</option>
        <option value="rejected">Rejected</option>
      </select>
    </div>

    <article class="panel">
      <p v-if="loading" class="empty-state">Loading claims...</p>
      <p v-else-if="errorMessage" class="message error">{{ errorMessage }}</p>

      <table v-else class="data-table">
        <thead>
          <tr>
            <th>Claim ID</th>
            <th>Policyholder</th>
            <th>Type</th>
            <th>Date</th>
            <th>Amount</th>
            <th>Priority</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="claim in filteredClaims" :key="claim.id">
            <td><a href="#" @click.prevent>{{ claim.claimNumber }}</a></td>
            <td>User #{{ claim.userId }}</td>
            <td>{{ claim.claimType }}</td>
            <td>{{ formatDate(claim.incidentDate) }}</td>
            <td>{{ formatCurrency(claim.estimatedAmount) }}</td>
            <td><span class="badge" :class="getPriorityClass(claim.priority)">{{ claim.priority }}</span></td>
            <td><span class="badge" :class="getStatusClass(claim.status)">{{ getStatusLabel(claim.status) }}</span></td>
            <td>
              <RouterLink :to="{ path: '/agent/review-claims', query: { claimId: claim.id } }" class="link-btn">Review</RouterLink>
            </td>
          </tr>
        </tbody>
      </table>

      <p v-if="!loading && !errorMessage && !filteredClaims.length" class="empty-state">No claims match your filters.</p>
    </article>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { getClaims } from '../../services/api';
import { formatCurrency, formatDate, getPriorityClass, getStatusClass, getStatusLabel } from '../../services/claimTransforms';

const query = ref('');
const statusFilter = ref('all');
const claims = ref([]);
const loading = ref(true);
const errorMessage = ref('');

const filteredClaims = computed(() => {
  const q = query.value.trim().toLowerCase();

  return claims.value.filter((claim) => {
    const matchesQuery = !q || `${claim.claimNumber} user ${claim.userId}`.toLowerCase().includes(q);
    const matchesStatus = statusFilter.value === 'all' || String(claim.status || '').toLowerCase() === statusFilter.value;
    return matchesQuery && matchesStatus;
  });
});

onMounted(async () => {
  loading.value = true;
  errorMessage.value = '';

  try {
    const { data } = await getClaims();
    claims.value = data || [];
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Unable to load claims.';
  } finally {
    loading.value = false;
  }
});
</script>

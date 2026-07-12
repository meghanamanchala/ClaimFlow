<template>
  <section>
    <header class="page-head page-head-row">
      <div>
        <h1>My Claims</h1>
        <p>Track and manage your insurance claims</p>
      </div>
      <input v-model="search" class="search-input" type="text" placeholder="Search claims..." />
    </header>

    <p v-if="loading" class="empty-state">Loading claims...</p>
    <p v-else-if="errorMessage" class="message error">{{ errorMessage }}</p>

    <article v-for="claim in filteredClaims" :key="claim.id" class="panel claim-card">
      <div class="claim-card-head">
        <div>
          <h2>{{ claim.claimNumber }}</h2>
          <p>{{ claim.claimType }} - {{ formatDate(claim.incidentDate) }}</p>
        </div>
        <div class="claim-meta">
          <strong>{{ formatCurrency(claim.estimatedAmount) }}</strong>
          <span class="badge" :class="getStatusClass(claim.status)">{{ getStatusLabel(claim.status) }}</span>
        </div>
      </div>

      <ol class="progress-list progress-list-inline">
        <li v-for="step in timelineWithState(claim.timeline)" :key="`${claim.id}-${step.step}-${step.date}`" class="progress-item">
          <div class="progress-dot" :class="step.state"></div>
          <div>
            <p class="progress-title">{{ step.step }}</p>
            <p class="progress-date">{{ formatDate(step.date) }}</p>
          </div>
        </li>
      </ol>
    </article>

    <p v-if="!loading && !errorMessage && !filteredClaims.length" class="empty-state">
      No claims found for your search.
    </p>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { getClaims } from '../../services/api';
import { formatCurrency, formatDate, getStatusClass, getStatusLabel } from '../../services/claimTransforms';

const search = ref('');
const claims = ref([]);
const loading = ref(true);
const errorMessage = ref('');

const filteredClaims = computed(() => {
  const q = search.value.trim().toLowerCase();

  if (!q) {
    return claims.value;
  }

  return claims.value.filter((claim) => {
    return [claim.claimNumber, claim.claimType, getStatusLabel(claim.status)]
      .join(' ')
      .toLowerCase()
      .includes(q);
  });
});

function timelineWithState(timeline) {
  const list = timeline || [];
  return list.map((item, index) => {
    const isLast = index === list.length - 1;
    return {
      ...item,
      state: isLast ? 'is-active' : 'is-done'
    };
  });
}

onMounted(async () => {
  loading.value = true;
  errorMessage.value = '';

  try {
    const { data } = await getClaims();
    claims.value = (data || []).sort((a, b) => new Date(b.createdAt || b.incidentDate) - new Date(a.createdAt || a.incidentDate));
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Unable to load claims.';
  } finally {
    loading.value = false;
  }
});
</script>

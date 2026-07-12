<template>
  <section>
    <header class="page-head">
      <h1>Claim History</h1>
      <p>Review all historical claim activities and decisions</p>
    </header>

    <article class="panel">
      <h2>Timeline</h2>
      <p v-if="loading" class="empty-state">Loading timeline...</p>
      <p v-else-if="errorMessage" class="message error">{{ errorMessage }}</p>

      <ol v-else class="history-list">
        <li v-for="item in history" :key="item.id" class="history-item">
          <div class="history-date">{{ formatDate(item.date) }}</div>
          <div>
            <p class="history-title">{{ item.title }}</p>
            <p class="history-copy">{{ item.copy }}</p>
          </div>
          <span class="badge" :class="item.badgeClass">{{ item.status }}</span>
        </li>
        <li v-if="history.length === 0" class="empty-state">No historical events yet.</li>
      </ol>
    </article>

    <article class="panel">
      <h2>Summary By Status</h2>
      <div class="summary-grid">
        <div class="summary-card" v-for="item in summary" :key="item.label">
          <p class="summary-label">{{ item.label }}</p>
          <p class="summary-value">{{ item.value }}</p>
        </div>
      </div>
    </article>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { getClaims } from '../../services/api';
import { formatDate, getStatusClass, getStatusLabel } from '../../services/claimTransforms';

const claims = ref([]);
const loading = ref(true);
const errorMessage = ref('');

const history = computed(() => {
  const events = [];

  claims.value.forEach((claim) => {
    (claim.timeline || []).forEach((timelineItem, index) => {
      events.push({
        id: `${claim.id}-${index}`,
        date: timelineItem.date,
        title: `${claim.claimNumber} - ${timelineItem.step}`,
        copy: `${claim.claimType} claim is currently ${getStatusLabel(claim.status).toLowerCase()}.`,
        status: getStatusLabel(claim.status),
        badgeClass: getStatusClass(claim.status)
      });
    });
  });

  return events.sort((a, b) => new Date(b.date) - new Date(a.date));
});

const summary = computed(() => {
  const grouped = {
    Approved: 0,
    'Under Review': 0,
    Pending: 0,
    Rejected: 0
  };

  claims.value.forEach((claim) => {
    const status = getStatusLabel(claim.status);
    if (grouped[status] !== undefined) {
      grouped[status] += 1;
    }
  });

  return Object.entries(grouped).map(([label, value]) => ({ label: `${label} Claims`, value }));
});

onMounted(async () => {
  loading.value = true;
  errorMessage.value = '';

  try {
    const { data } = await getClaims();
    claims.value = data || [];
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Unable to load claim history.';
  } finally {
    loading.value = false;
  }
});
</script>

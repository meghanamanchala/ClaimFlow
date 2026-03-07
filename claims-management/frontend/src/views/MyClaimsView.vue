<template>
  <section>
    <header class="page-head page-head-row">
      <div>
        <h1>My Claims</h1>
        <p>Track and manage your insurance claims</p>
      </div>
      <input v-model="search" class="search-input" type="text" placeholder="Search claims..." />
    </header>

    <article v-for="claim in filteredClaims" :key="claim.id" class="panel claim-card">
      <div class="claim-card-head">
        <div>
          <h2>{{ claim.id }}</h2>
          <p>{{ claim.type }} - {{ claim.date }}</p>
        </div>
        <div class="claim-meta">
          <strong>{{ claim.amount }}</strong>
          <span class="badge" :class="claim.statusClass">{{ claim.status }}</span>
        </div>
      </div>

      <ol class="progress-list progress-list-inline">
        <li v-for="step in claim.steps" :key="step.title" class="progress-item">
          <div class="progress-dot" :class="step.state"></div>
          <div>
            <p class="progress-title">{{ step.title }}</p>
            <p class="progress-date">{{ step.date }}</p>
          </div>
        </li>
      </ol>
    </article>

    <p v-if="!filteredClaims.length" class="empty-state">No claims found for your search.</p>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue';

const search = ref('');

const claims = [
  {
    id: 'CLM-2024-001',
    type: 'Auto Insurance',
    date: 'Mar 2, 2026',
    amount: '$4,500',
    status: 'Under Review',
    statusClass: 'badge-review',
    steps: [
      { title: 'Claim Submitted', date: 'Mar 2, 2026', state: 'is-done' },
      { title: 'Documents Verified', date: 'Mar 3, 2026', state: 'is-done' },
      { title: 'Under Agent Review', date: 'Mar 5, 2026', state: 'is-active' },
      { title: 'Final Approval', date: 'Pending', state: 'is-upcoming' },
      { title: 'Payment Processed', date: 'Pending', state: 'is-upcoming' }
    ]
  },
  {
    id: 'CLM-2024-002',
    type: 'Health Insurance',
    date: 'Feb 15, 2026',
    amount: '$1,200',
    status: 'Approved',
    statusClass: 'badge-approved',
    steps: [
      { title: 'Claim Submitted', date: 'Feb 15, 2026', state: 'is-done' },
      { title: 'Documents Verified', date: 'Feb 15, 2026', state: 'is-done' },
      { title: 'Under Agent Review', date: 'Feb 16, 2026', state: 'is-done' },
      { title: 'Final Approval', date: 'Feb 17, 2026', state: 'is-done' },
      { title: 'Payment Processed', date: 'Feb 20, 2026', state: 'is-done' }
    ]
  },
  {
    id: 'CLM-2024-003',
    type: 'Property Insurance',
    date: 'Jan 28, 2026',
    amount: '$12,000',
    status: 'Pending',
    statusClass: 'badge-pending',
    steps: [
      { title: 'Claim Submitted', date: 'Jan 28, 2026', state: 'is-done' },
      { title: 'Documents Verified', date: 'Jan 29, 2026', state: 'is-done' },
      { title: 'Under Agent Review', date: 'Jan 30, 2026', state: 'is-done' },
      { title: 'Final Approval', date: 'Pending', state: 'is-upcoming' },
      { title: 'Payment Processed', date: 'Pending', state: 'is-upcoming' }
    ]
  }
];

const filteredClaims = computed(() => {
  const q = search.value.trim().toLowerCase();

  if (!q) {
    return claims;
  }

  return claims.filter((claim) => {
    return [claim.id, claim.type, claim.status].join(' ').toLowerCase().includes(q);
  });
});
</script>

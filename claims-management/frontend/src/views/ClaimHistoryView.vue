<template>
  <section>
    <header class="page-head">
      <h1>Claim History</h1>
      <p>Review all historical claim activities and decisions</p>
    </header>

    <article class="panel">
      <h2>Timeline</h2>
      <ol class="history-list">
        <li v-for="item in history" :key="item.id" class="history-item">
          <div class="history-date">{{ item.date }}</div>
          <div>
            <p class="history-title">{{ item.title }}</p>
            <p class="history-copy">{{ item.copy }}</p>
          </div>
          <span class="badge" :class="item.badgeClass">{{ item.status }}</span>
        </li>
      </ol>
    </article>

    <article class="panel">
      <h2>Summary By Status</h2>
      <div class="summary-grid">
        <div class="summary-card">
          <p class="summary-label">Approved Claims</p>
          <p class="summary-value">8</p>
        </div>
        <div class="summary-card">
          <p class="summary-label">Under Review</p>
          <p class="summary-value">1</p>
        </div>
        <div class="summary-card">
          <p class="summary-label">Pending</p>
          <p class="summary-value">2</p>
        </div>
      </div>
    </article>
  </section>
</template>

<script setup>
const history = [
  {
    id: 1,
    date: 'Mar 5, 2026',
    title: 'CLM-2024-001 moved to agent review',
    copy: 'Your auto insurance claim is currently being evaluated by the assigned agent.',
    status: 'Under Review',
    badgeClass: 'badge-review'
  },
  {
    id: 2,
    date: 'Feb 17, 2026',
    title: 'CLM-2024-002 approved',
    copy: 'Health claim was approved and payment was scheduled for processing.',
    status: 'Approved',
    badgeClass: 'badge-approved'
  },
  {
    id: 3,
    date: 'Jan 30, 2026',
    title: 'CLM-2024-003 waiting final approval',
    copy: 'Property claim documents are complete and pending final manager sign-off.',
    status: 'Pending',
    badgeClass: 'badge-pending'
  }
];
</script>

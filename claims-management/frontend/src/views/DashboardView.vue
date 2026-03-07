<template>
  <section>
    <header class="page-head">
      <h1>Welcome back, Sarah</h1>
      <p>Here&apos;s an overview of your insurance claims</p>
    </header>

    <section class="stat-grid">
      <article class="stat-card">
        <p class="stat-title">Active Claims</p>
        <p class="stat-value">3</p>
        <p class="stat-note">2 in progress</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Pending Review</p>
        <p class="stat-value">1</p>
        <p class="stat-note">Awaiting final decision</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Approved</p>
        <p class="stat-value">8</p>
        <p class="stat-note positive">+2 this month</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Total Claimed</p>
        <p class="stat-value">$32,400</p>
        <p class="stat-note">Across all policies</p>
      </article>
    </section>

    <section class="dashboard-grid">
      <article class="panel">
        <h2>Recent Claims</h2>
        <table class="data-table">
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
            <tr v-for="claim in claims" :key="claim.id">
              <td>
                <a href="#" @click.prevent>{{ claim.id }}</a>
              </td>
              <td>{{ claim.type }}</td>
              <td>{{ claim.date }}</td>
              <td>{{ claim.amount }}</td>
              <td>
                <span class="badge" :class="claim.statusClass">{{ claim.status }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </article>

      <article class="panel">
        <h2>Claim Progress</h2>
        <ol class="progress-list">
          <li v-for="step in progress" :key="step.title" class="progress-item">
            <div class="progress-dot" :class="step.state"></div>
            <div>
              <p class="progress-title">{{ step.title }}</p>
              <p class="progress-date">{{ step.date }}</p>
            </div>
          </li>
        </ol>
      </article>
    </section>
  </section>
</template>

<script setup>
const claims = [
  {
    id: 'CLM-2024-001',
    type: 'Auto Insurance',
    date: 'Mar 2, 2026',
    amount: '$4,500',
    status: 'Under Review',
    statusClass: 'badge-review'
  },
  {
    id: 'CLM-2024-002',
    type: 'Health Insurance',
    date: 'Feb 15, 2026',
    amount: '$1,200',
    status: 'Approved',
    statusClass: 'badge-approved'
  },
  {
    id: 'CLM-2024-003',
    type: 'Property Insurance',
    date: 'Jan 28, 2026',
    amount: '$12,000',
    status: 'Pending',
    statusClass: 'badge-pending'
  }
];

const progress = [
  { title: 'Claim Submitted', date: 'Mar 2, 2026', state: 'is-done' },
  { title: 'Documents Verified', date: 'Mar 3, 2026', state: 'is-done' },
  { title: 'Under Agent Review', date: 'Mar 5, 2026', state: 'is-active' },
  { title: 'Final Approval', date: 'Pending', state: 'is-upcoming' },
  { title: 'Payment Processed', date: 'Pending', state: 'is-upcoming' }
];
</script>

<template>
  <section>
    <header class="page-head">
      <h1>Agent Dashboard</h1>
      <p>Manage and review your assigned claims</p>
    </header>

    <section class="stat-grid">
      <article class="stat-card">
        <p class="stat-title">Assigned Claims</p>
        <p class="stat-value">12</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Pending Review</p>
        <p class="stat-value">4</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Resolved Today</p>
        <p class="stat-value">3</p>
        <p class="stat-note positive">+15% vs avg</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Active Policyholders</p>
        <p class="stat-value">28</p>
      </article>
    </section>

    <article class="panel">
      <div class="panel-head-row">
        <h2>Assigned Claims</h2>
        <RouterLink class="ghost-link" to="/agent/assigned-claims">View All</RouterLink>
      </div>

      <table class="data-table">
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
          <tr v-for="claim in claims" :key="claim.id">
            <td><a href="#" @click.prevent>{{ claim.id }}</a></td>
            <td>{{ claim.policyholder }}</td>
            <td>{{ claim.type }}</td>
            <td>{{ claim.amount }}</td>
            <td><span class="badge" :class="claim.priorityClass">{{ claim.priority }}</span></td>
            <td><span class="badge" :class="claim.statusClass">{{ claim.status }}</span></td>
            <td>
              <RouterLink class="link-btn" to="/agent/review-claims">Review</RouterLink>
            </td>
          </tr>
        </tbody>
      </table>
    </article>
  </section>
</template>

<script setup>
const claims = [
  {
    id: 'CLM-2024-001',
    policyholder: 'Sarah Mitchell',
    type: 'Auto',
    amount: '$4,500',
    priority: 'High',
    priorityClass: 'badge-priority-high',
    status: 'Under Review',
    statusClass: 'badge-review'
  },
  {
    id: 'CLM-2024-004',
    policyholder: 'John Davis',
    type: 'Health',
    amount: '$2,800',
    priority: 'Medium',
    priorityClass: 'badge-priority-medium',
    status: 'Pending',
    statusClass: 'badge-pending'
  },
  {
    id: 'CLM-2024-005',
    policyholder: 'Emily Brown',
    type: 'Property',
    amount: '$18,500',
    priority: 'High',
    priorityClass: 'badge-priority-high',
    status: 'Under Review',
    statusClass: 'badge-review'
  },
  {
    id: 'CLM-2024-006',
    policyholder: 'Mike Wilson',
    type: 'Auto',
    amount: '$3,200',
    priority: 'Low',
    priorityClass: 'badge-priority-low',
    status: 'Pending',
    statusClass: 'badge-pending'
  }
];
</script>

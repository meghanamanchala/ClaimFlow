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
        <option value="Under Review">Under Review</option>
        <option value="Pending">Pending</option>
      </select>
    </div>

    <article class="panel">
      <table class="data-table">
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
            <td><a href="#" @click.prevent>{{ claim.id }}</a></td>
            <td>{{ claim.policyholder }}</td>
            <td>{{ claim.type }}</td>
            <td>{{ claim.date }}</td>
            <td>{{ claim.amount }}</td>
            <td><span class="badge" :class="claim.priorityClass">{{ claim.priority }}</span></td>
            <td><span class="badge" :class="claim.statusClass">{{ claim.status }}</span></td>
            <td>
              <RouterLink class="link-btn" to="/agent/review-claims">Review</RouterLink>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="!filteredClaims.length" class="empty-state">No claims match your filters.</p>
    </article>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue';

const query = ref('');
const statusFilter = ref('all');

const claims = [
  {
    id: 'CLM-2024-001',
    policyholder: 'Sarah Mitchell',
    type: 'Auto',
    date: 'Mar 2, 2026',
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
    date: 'Mar 4, 2026',
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
    date: 'Mar 1, 2026',
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
    date: 'Feb 28, 2026',
    amount: '$3,200',
    priority: 'Low',
    priorityClass: 'badge-priority-low',
    status: 'Pending',
    statusClass: 'badge-pending'
  },
  {
    id: 'CLM-2024-009',
    policyholder: 'Anna Lee',
    type: 'Health',
    date: 'Mar 5, 2026',
    amount: '$1,900',
    priority: 'Medium',
    priorityClass: 'badge-priority-medium',
    status: 'Pending',
    statusClass: 'badge-pending'
  }
];

const filteredClaims = computed(() => {
  const q = query.value.trim().toLowerCase();

  return claims.filter((claim) => {
    const matchesQuery = !q || `${claim.id} ${claim.policyholder}`.toLowerCase().includes(q);
    const matchesStatus = statusFilter.value === 'all' || claim.status === statusFilter.value;
    return matchesQuery && matchesStatus;
  });
});
</script>

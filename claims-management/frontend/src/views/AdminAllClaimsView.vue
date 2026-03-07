<template>
  <section>
    <header class="page-head page-head-row">
      <div>
        <h1>All Claims</h1>
        <p>View and manage all claims across the system</p>
      </div>
      <button type="button" class="ghost-btn">Export</button>
    </header>

    <div class="toolbar-row">
      <input v-model="search" class="search-input" type="text" placeholder="Search claims..." />
      <select v-model="statusFilter" class="filter-select">
        <option value="all">All Status</option>
        <option value="Under Review">Under Review</option>
        <option value="Approved">Approved</option>
        <option value="Pending">Pending</option>
        <option value="Rejected">Rejected</option>
      </select>
      <select v-model="agentFilter" class="filter-select">
        <option value="all">All Agents</option>
        <option value="James Carter">James Carter</option>
        <option value="Lisa Anderson">Lisa Anderson</option>
        <option value="-">Unassigned</option>
      </select>
    </div>

    <article class="panel">
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Policyholder</th>
            <th>Agent</th>
            <th>Type</th>
            <th>Amount</th>
            <th>Date</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="claim in filteredClaims" :key="claim.id">
            <td><a href="#" @click.prevent>{{ claim.id }}</a></td>
            <td>{{ claim.policyholder }}</td>
            <td>{{ claim.agent }}</td>
            <td>{{ claim.type }}</td>
            <td>{{ claim.amount }}</td>
            <td>{{ claim.date }}</td>
            <td><span class="badge" :class="claim.statusClass">{{ claim.status }}</span></td>
            <td><a href="#" class="link-btn" @click.prevent>View</a></td>
          </tr>
        </tbody>
      </table>
    </article>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue';

const search = ref('');
const statusFilter = ref('all');
const agentFilter = ref('all');

const claims = [
  { id: 'CLM-2024-001', policyholder: 'Sarah Mitchell', agent: 'James Carter', type: 'Auto', amount: '$4,500', date: 'Mar 2, 2026', status: 'Under Review', statusClass: 'badge-review' },
  { id: 'CLM-2024-002', policyholder: 'Sarah Mitchell', agent: 'James Carter', type: 'Health', amount: '$1,200', date: 'Feb 15, 2026', status: 'Approved', statusClass: 'badge-approved' },
  { id: 'CLM-2024-003', policyholder: 'Sarah Mitchell', agent: '-', type: 'Property', amount: '$12,000', date: 'Jan 28, 2026', status: 'Pending', statusClass: 'badge-pending' },
  { id: 'CLM-2024-004', policyholder: 'John Davis', agent: 'James Carter', type: 'Health', amount: '$2,800', date: 'Mar 4, 2026', status: 'Pending', statusClass: 'badge-pending' },
  { id: 'CLM-2024-005', policyholder: 'Emily Brown', agent: 'Lisa Anderson', type: 'Property', amount: '$18,500', date: 'Mar 1, 2026', status: 'Under Review', statusClass: 'badge-review' },
  { id: 'CLM-2024-006', policyholder: 'Mike Wilson', agent: 'James Carter', type: 'Auto', amount: '$3,200', date: 'Feb 28, 2026', status: 'Pending', statusClass: 'badge-pending' },
  { id: 'CLM-2024-007', policyholder: 'Tom Harris', agent: 'Lisa Anderson', type: 'Life', amount: '$50,000', date: 'Feb 20, 2026', status: 'Rejected', statusClass: 'badge-rejected' }
];

const filteredClaims = computed(() => {
  const q = search.value.trim().toLowerCase();

  return claims.filter((claim) => {
    const matchesSearch = !q || `${claim.id} ${claim.policyholder}`.toLowerCase().includes(q);
    const matchesStatus = statusFilter.value === 'all' || claim.status === statusFilter.value;
    const matchesAgent = agentFilter.value === 'all' || claim.agent === agentFilter.value;
    return matchesSearch && matchesStatus && matchesAgent;
  });
});
</script>

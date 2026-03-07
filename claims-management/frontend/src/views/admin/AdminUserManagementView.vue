<template>
  <section>
    <header class="page-head page-head-row">
      <div>
        <h1>User Management</h1>
        <p>Manage policyholders and agents</p>
      </div>
      <button type="button" class="primary-btn">Add User</button>
    </header>

    <div class="toolbar-row">
      <input v-model="search" class="search-input" type="text" placeholder="Search users..." />
    </div>

    <article class="panel">
      <table class="data-table">
        <thead>
          <tr>
            <th>User</th>
            <th>Role</th>
            <th>Status</th>
            <th>Claims</th>
            <th>Joined</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.email">
            <td>
              <div class="user-cell">
                <div class="avatar-soft">{{ user.initials }}</div>
                <div>
                  <p class="user-name">{{ user.name }}</p>
                  <p class="user-email">{{ user.email }}</p>
                </div>
              </div>
            </td>
            <td><span class="badge" :class="user.roleClass">{{ user.role }}</span></td>
            <td><span class="badge" :class="user.statusClass">{{ user.status }}</span></td>
            <td>{{ user.claims }}</td>
            <td>{{ user.joined }}</td>
            <td><button type="button" class="icon-btn">...</button></td>
          </tr>
        </tbody>
      </table>
    </article>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue';

const search = ref('');

const users = [
  { initials: 'SM', name: 'Sarah Mitchell', email: 'sarah@example.com', role: 'Policyholder', roleClass: 'badge-pending', status: 'Active', statusClass: 'badge-approved', claims: 3, joined: 'Jan 15, 2026' },
  { initials: 'JD', name: 'John Davis', email: 'john@example.com', role: 'Policyholder', roleClass: 'badge-pending', status: 'Active', statusClass: 'badge-approved', claims: 1, joined: 'Feb 2, 2026' },
  { initials: 'EB', name: 'Emily Brown', email: 'emily@example.com', role: 'Policyholder', roleClass: 'badge-pending', status: 'Active', statusClass: 'badge-approved', claims: 2, joined: 'Dec 10, 2025' },
  { initials: 'JC', name: 'James Carter', email: 'james@claimflow.com', role: 'Agent', roleClass: 'badge-review', status: 'Active', statusClass: 'badge-approved', claims: 12, joined: 'Oct 1, 2025' },
  { initials: 'LA', name: 'Lisa Anderson', email: 'lisa@claimflow.com', role: 'Agent', roleClass: 'badge-review', status: 'Active', statusClass: 'badge-approved', claims: 8, joined: 'Nov 15, 2025' },
  { initials: 'MW', name: 'Mike Wilson', email: 'mike@example.com', role: 'Policyholder', roleClass: 'badge-pending', status: 'Inactive', statusClass: 'badge-inactive', claims: 0, joined: 'Mar 1, 2026' }
];

const filteredUsers = computed(() => {
  const q = search.value.trim().toLowerCase();
  if (!q) {
    return users;
  }

  return users.filter((user) => `${user.name} ${user.email}`.toLowerCase().includes(q));
});
</script>

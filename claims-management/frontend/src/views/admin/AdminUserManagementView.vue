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
          <tr v-for="user in filteredUsers" :key="user.id">
            <td>
              <div class="user-cell">
                <div class="avatar-soft">{{ initialsFor(user.name) }}</div>
                <div>
                  <p class="user-name">{{ user.name }}</p>
                  <p class="user-email">{{ user.email }}</p>
                </div>
              </div>
            </td>
            <td><span class="badge" :class="roleClass(user.role)">{{ roleLabel(user.role) }}</span></td>
            <td><span class="badge" :class="statusClass(user.status)">{{ roleLabel(user.status) }}</span></td>
            <td>{{ claimCount[user.id] || 0 }}</td>
            <td>{{ formatDate(user.createdAt) }}</td>
            <td><button type="button" class="icon-btn">...</button></td>
          </tr>
        </tbody>
      </table>
    </article>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { getClaims, getUsers } from '../../services/api';
import { formatDate, toTitleCase } from '../../services/claimTransforms';

const search = ref('');
const users = ref([]);
const claims = ref([]);

const claimCount = computed(() => {
  return claims.value.reduce((acc, claim) => {
    acc[claim.userId] = (acc[claim.userId] || 0) + 1;
    return acc;
  }, {});
});

const filteredUsers = computed(() => {
  const q = search.value.trim().toLowerCase();

  if (!q) {
    return users.value;
  }

  return users.value.filter((user) => `${user.name} ${user.email}`.toLowerCase().includes(q));
});

function initialsFor(name) {
  return String(name || '')
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((token) => token[0]?.toUpperCase())
    .join('');
}

function roleClass(role) {
  return String(role || '').toLowerCase() === 'agent' ? 'badge-review' : 'badge-pending';
}

function statusClass(status) {
  return String(status || '').toLowerCase() === 'active' ? 'badge-approved' : 'badge-inactive';
}

function roleLabel(value) {
  return toTitleCase(value || 'unknown');
}

onMounted(async () => {
  try {
    const [usersResponse, claimsResponse] = await Promise.all([getUsers(), getClaims()]);
    users.value = usersResponse.data || [];
    claims.value = claimsResponse.data || [];
  } catch {
    users.value = [];
    claims.value = [];
  }
});
</script>

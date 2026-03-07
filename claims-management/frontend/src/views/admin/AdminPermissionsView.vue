<template>
  <section>
    <header class="page-head">
      <h1>Permissions</h1>
      <p>Manage role-based access control</p>
    </header>

    <section class="permission-grid">
      <article class="panel permission-card" v-for="role in roles" :key="role.name">
        <h2>{{ role.name }}</h2>
        <p class="stat-note">{{ role.enabled }} of {{ role.items.length }} enabled</p>

        <ul class="permission-list">
          <li v-for="item in role.items" :key="item.name">
            <span>{{ item.name }}</span>
            <button type="button" class="switch" :class="{ on: item.enabled }" @click="item.enabled = !item.enabled">
              <span></span>
            </button>
          </li>
        </ul>
      </article>
    </section>
  </section>
</template>

<script setup>
import { reactive } from 'vue';

const roles = reactive([
  {
    name: 'Policyholder',
    enabled: 4,
    items: [
      { name: 'View own claims', enabled: true },
      { name: 'Submit new claims', enabled: true },
      { name: 'Upload documents', enabled: true },
      { name: 'View claim history', enabled: true },
      { name: 'Edit submitted claims', enabled: false },
      { name: 'Delete claims', enabled: false }
    ]
  },
  {
    name: 'Agent',
    enabled: 4,
    items: [
      { name: 'View assigned claims', enabled: true },
      { name: 'Review & update status', enabled: true },
      { name: 'Verify documents', enabled: true },
      { name: 'Message policyholders', enabled: true },
      { name: 'Reassign claims', enabled: false },
      { name: 'View all claims', enabled: false }
    ]
  },
  {
    name: 'Administrator',
    enabled: 6,
    items: [
      { name: 'Full system access', enabled: true },
      { name: 'Manage users', enabled: true },
      { name: 'Assign claims', enabled: true },
      { name: 'View analytics', enabled: true },
      { name: 'Manage permissions', enabled: true },
      { name: 'System settings', enabled: true }
    ]
  }
]);
</script>

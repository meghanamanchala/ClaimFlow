<template>
  <section>
    <header class="page-head page-head-row">
      <div>
        <h1>Permissions</h1>
        <p>Manage role-based access control</p>
      </div>
      <button type="button" class="primary-btn" @click="savePermissions" :disabled="saving">
        {{ saving ? 'Saving...' : 'Save Changes' }}
      </button>
    </header>

    <p v-if="loading" class="empty-state">Loading permissions...</p>
    <p v-else-if="errorMessage" class="message error">{{ errorMessage }}</p>

    <section v-else class="permission-grid">
      <article class="panel permission-card" v-for="role in roles" :key="role.role">
        <h2>{{ role.role }}</h2>
        <p class="stat-note">{{ enabledCount(role.items) }} of {{ role.items.length }} enabled</p>

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

    <p v-if="successMessage" class="form-message success">{{ successMessage }}</p>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { getAdminPermissions, updateAdminPermissions } from '../../services/api';

const roles = ref([]);
const loading = ref(true);
const saving = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

function enabledCount(items) {
  return (items || []).filter((item) => item.enabled).length;
}

async function savePermissions() {
  saving.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  try {
    await updateAdminPermissions({ roles: roles.value });
    successMessage.value = 'Permissions saved successfully.';
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Unable to save permissions.';
  } finally {
    saving.value = false;
  }
}

onMounted(async () => {
  loading.value = true;
  errorMessage.value = '';

  try {
    const { data } = await getAdminPermissions();
    roles.value = data?.roles || [];
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Unable to load permissions.';
    roles.value = [];
  } finally {
    loading.value = false;
  }
});
</script>

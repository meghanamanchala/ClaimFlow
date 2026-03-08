<template>
  <section class="profile-page">
    <header class="page-head">
      <h1>Edit Profile</h1>
      <p>{{ subtitle }}</p>
    </header>

    <article class="panel profile-panel">
      <form class="profile-form" @submit.prevent="saveProfile">
        <label class="field" for="profile-name">
          <span>Full Name</span>
          <input
            id="profile-name"
            v-model.trim="form.name"
            type="text"
            autocomplete="name"
            required
            placeholder="Enter your full name"
          />
        </label>

        <label class="field" for="profile-email">
          <span>Email</span>
          <input
            id="profile-email"
            v-model.trim="form.email"
            type="email"
            autocomplete="email"
            required
            placeholder="you@example.com"
          />
        </label>

        <div class="profile-actions">
          <button type="submit" class="primary-btn" :disabled="loading || saving">
            {{ saving ? 'Saving...' : 'Save Changes' }}
          </button>
        </div>

        <p v-if="message" class="message success">{{ message }}</p>
        <p v-if="errorMessage" class="message error">{{ errorMessage }}</p>
      </form>
    </article>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue';
import { getMe, updateMe } from '../../services/api';

const roleLabelMap = {
  policyholder: 'policyholder dashboard',
  agent: 'agent workspace',
  admin: 'admin workspace'
};

const subtitle = computed(() => {
  const role = (localStorage.getItem('claimflow_role') || '').toLowerCase();
  const area = roleLabelMap[role] || 'dashboard';
  return `Update your account details used across the ${area}.`;
});

const form = reactive({
  name: '',
  email: ''
});

const loading = ref(true);
const saving = ref(false);
const message = ref('');
const errorMessage = ref('');

async function loadProfile() {
  loading.value = true;
  errorMessage.value = '';

  try {
    const { data } = await getMe();
    form.name = data?.name || '';
    form.email = data?.email || '';
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Unable to load profile details.';
  } finally {
    loading.value = false;
  }
}

async function saveProfile() {
  saving.value = true;
  message.value = '';
  errorMessage.value = '';

  try {
    const { data } = await updateMe({
      name: form.name,
      email: form.email
    });

    form.name = data?.name || form.name;
    form.email = data?.email || form.email;
    message.value = 'Profile updated successfully.';
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Unable to save your profile.';
  } finally {
    saving.value = false;
  }
}

onMounted(loadProfile);
</script>

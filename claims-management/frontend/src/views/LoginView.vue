<template>
  <AuthLayout>
    <form class="auth-form" @submit.prevent="submitLogin">
      <h2>Welcome back</h2>
      <p class="subtext">Sign in to your account to continue</p>

      <label class="field">
        <span>Email</span>
        <input v-model="form.email" type="email" required placeholder="you@example.com" />
      </label>

      <label class="field">
        <div class="field-head">
          <span>Password</span>
          <a href="#" @click.prevent>Forgot password?</a>
        </div>
        <input v-model="form.password" type="password" required placeholder="Enter password" />
      </label>

      <fieldset class="role-group">
        <legend>Role</legend>
        <div class="role-options">
          <label v-for="option in roles" :key="option.value" class="role-option">
            <input v-model="form.role" type="radio" :value="option.value" name="role" />
            <span>{{ option.label }}</span>
          </label>
        </div>
      </fieldset>

      <button class="submit-btn" type="submit" :disabled="loading">
        {{ loading ? 'Signing In...' : 'Sign In' }}
      </button>

      <p v-if="errorMessage" class="message error">{{ errorMessage }}</p>
      <p v-if="successMessage" class="message success">{{ successMessage }}</p>

      <p class="switch-link">
        Don't have an account?
        <RouterLink to="/register">Register here</RouterLink>
      </p>
    </form>
  </AuthLayout>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { RouterLink } from 'vue-router';
import AuthLayout from './AuthLayout.vue';
import { loginUser } from '../services/api';

const roles = [
  { label: 'Policyholder', value: 'policyholder' },
  { label: 'Agent', value: 'agent' },
  { label: 'Admin', value: 'admin' }
];

const form = reactive({
  email: '',
  password: '',
  role: 'policyholder'
});

const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

async function submitLogin() {
  loading.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  try {
    const { data } = await loginUser(form.email, form.password);
    localStorage.setItem('claimflow_token', data.access_token);
    localStorage.setItem('claimflow_role', form.role);
    successMessage.value = 'Login successful. Token saved to localStorage.';
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Login failed. Please try again.';
  } finally {
    loading.value = false;
  }
}
</script>

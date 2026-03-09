<template>
  <AuthLayout>
    <form class="auth-form" @submit.prevent="submitLogin">
      <h2>Welcome back</h2>
      <p class="subtext">Sign in to your account to continue</p>

      <label class="field">
        <span>Email</span>
        <input v-model="form.email" type="email" autocomplete="username" required placeholder="you@example.com" />
      </label>

      <label class="field">
        <div class="field-head">
          <span>Password</span>
          <a href="#" @click.prevent>Forgot password?</a>
        </div>
        <input
          v-model="form.password"
          type="password"
          autocomplete="current-password"
          required
          placeholder="Enter password"
        />
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
import { RouterLink, useRouter } from 'vue-router';
import AuthLayout from '../../layouts/AuthLayout.vue';
import { loginUser } from '../../services/api';

const router = useRouter();

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
    const normalizedEmail = String(form.email || '').trim().toLowerCase();
    const { data } = await loginUser(normalizedEmail, form.password);
    localStorage.setItem('claimflow_token', data.access_token);
    localStorage.setItem('claimflow_role', form.role);

    if (form.role === 'agent') {
      router.push('/agent/dashboard');
      return;
    }

    if (form.role === 'admin') {
      router.push('/admin/dashboard');
      return;
    }

    router.push('/dashboard');
  } catch (error) {
    localStorage.removeItem('claimflow_token');
    localStorage.removeItem('claimflow_role');
    errorMessage.value = error.response?.data?.detail || 'Login failed. Please try again.';
  } finally {
    loading.value = false;
  }
}
</script>

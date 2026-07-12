<template>
  <AuthLayout>
    <form class="auth-form" @submit.prevent="submitRegister">
      <h2>Create an account</h2>
      <p class="subtext">Join ClaimFlow to manage your insurance claims with ease.</p>

      <label class="field">
        <span>Full Name</span>
        <input v-model="form.name" type="text" autocomplete="name" required placeholder="John Doe" />
      </label>

      <label class="field">
        <span>Email</span>
        <input v-model="form.email" type="email" autocomplete="email" required placeholder="you@example.com" />
      </label>

      <label class="field">
        <span>Password</span>
        <input
          v-model="form.password"
          type="password"
          autocomplete="new-password"
          minlength="6"
          required
          placeholder="Create password"
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
        {{ loading ? 'Creating Account...' : 'Create Account' }}
      </button>

      <p v-if="errorMessage" class="message error">{{ errorMessage }}</p>
      <p v-if="successMessage" class="message success">{{ successMessage }}</p>

      <p class="switch-link">
        Already have an account?
        <RouterLink to="/login">Sign In</RouterLink>
      </p>
    </form>
  </AuthLayout>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import AuthLayout from '../../layouts/AuthLayout.vue';
import { registerUser } from '../../services/api';

const router = useRouter();

const roles = [
  { label: 'Policyholder', value: 'policyholder' },
  { label: 'Agent', value: 'agent' },
  { label: 'Admin', value: 'admin' }
];

const form = reactive({
  name: '',
  email: '',
  password: '',
  role: 'policyholder'
});

const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

async function submitRegister() {
  loading.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  try {
    await registerUser({
      name: form.name,
      email: form.email,
      password: form.password,
      role: form.role
    });

    successMessage.value = 'Registration successful. Redirecting to login...';
    setTimeout(() => {
      router.push('/login');
    }, 900);
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Registration failed. Please try again.';
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <section>
    <header class="page-head">
      <h1>Settings</h1>
      <p>System configuration and preferences</p>
    </header>

    <p v-if="loading" class="empty-state">Loading settings...</p>
    <p v-else-if="errorMessage" class="message error">{{ errorMessage }}</p>

    <template v-else>
      <article class="panel settings-panel">
        <h2>General</h2>
        <label class="field">
          <span>Company Name</span>
          <input type="text" v-model="form.general.companyName" />
        </label>
        <label class="field">
          <span>Support Email</span>
          <input type="email" v-model="form.general.supportEmail" />
        </label>
      </article>

      <article class="panel settings-panel">
        <h2>Notifications</h2>
        <ul class="setting-list">
          <li>
            <span>Email notifications for new claims</span>
            <button type="button" class="switch" :class="{ on: form.notifications.emailNotificationsForNewClaims }" @click="form.notifications.emailNotificationsForNewClaims = !form.notifications.emailNotificationsForNewClaims"><span></span></button>
          </li>
          <li>
            <span>SMS alerts for status updates</span>
            <button type="button" class="switch" :class="{ on: form.notifications.smsAlertsForStatusUpdates }" @click="form.notifications.smsAlertsForStatusUpdates = !form.notifications.smsAlertsForStatusUpdates"><span></span></button>
          </li>
          <li>
            <span>Daily summary reports</span>
            <button type="button" class="switch" :class="{ on: form.notifications.dailySummaryReports }" @click="form.notifications.dailySummaryReports = !form.notifications.dailySummaryReports"><span></span></button>
          </li>
          <li>
            <span>Agent assignment notifications</span>
            <button type="button" class="switch" :class="{ on: form.notifications.agentAssignmentNotifications }" @click="form.notifications.agentAssignmentNotifications = !form.notifications.agentAssignmentNotifications"><span></span></button>
          </li>
        </ul>
      </article>

      <article class="panel settings-panel">
        <h2>Claim Processing</h2>
        <label class="field">
          <span>Auto-assign threshold ($)</span>
          <input type="number" v-model.number="form.claimProcessing.autoAssignThreshold" />
        </label>
        <label class="field">
          <span>Review deadline (days)</span>
          <input type="number" v-model.number="form.claimProcessing.reviewDeadlineDays" />
        </label>
        <ul class="setting-list">
          <li>
            <span>Auto-assignment</span>
            <button type="button" class="switch" :class="{ on: form.claimProcessing.autoAssignment }" @click="form.claimProcessing.autoAssignment = !form.claimProcessing.autoAssignment"><span></span></button>
          </li>
        </ul>
      </article>

      <button type="button" class="primary-btn" @click="saveSettings" :disabled="saving">
        {{ saving ? 'Saving...' : 'Save Changes' }}
      </button>
      <p v-if="successMessage" class="form-message success">{{ successMessage }}</p>
    </template>
  </section>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue';
import { getAdminSettings, updateAdminSettings } from '../../services/api';

const loading = ref(true);
const saving = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const form = reactive({
  general: {
    companyName: '',
    supportEmail: ''
  },
  notifications: {
    emailNotificationsForNewClaims: true,
    smsAlertsForStatusUpdates: false,
    dailySummaryReports: true,
    agentAssignmentNotifications: true
  },
  claimProcessing: {
    autoAssignThreshold: 5000,
    reviewDeadlineDays: 7,
    autoAssignment: true
  }
});

async function loadSettings() {
  loading.value = true;
  errorMessage.value = '';

  try {
    const { data } = await getAdminSettings();
    form.general = data.general;
    form.notifications = data.notifications;
    form.claimProcessing = data.claimProcessing;
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Unable to load settings.';
  } finally {
    loading.value = false;
  }
}

async function saveSettings() {
  saving.value = true;
  successMessage.value = '';
  errorMessage.value = '';

  try {
    await updateAdminSettings({
      general: form.general,
      notifications: form.notifications,
      claimProcessing: form.claimProcessing
    });
    successMessage.value = 'Settings saved successfully.';
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Unable to save settings.';
  } finally {
    saving.value = false;
  }
}

onMounted(loadSettings);
</script>

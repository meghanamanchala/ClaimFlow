<template>
  <section class="notifications-page panel">
    <div class="page-head-row notifications-page-head">
      <div>
        <h1>Notifications</h1>
        <p>Recent claim and message updates.</p>
      </div>
      <div class="notifications-actions">
        <button type="button" class="ghost-btn" @click="loadNotifications">Refresh</button>
        <button type="button" class="primary-btn" @click="markAllRead" :disabled="!hasUnreadNotifications">Mark all read</button>
      </div>
    </div>

    <ul v-if="notifications.length" class="notifications-page-list">
      <li
        v-for="item in notifications"
        :key="item.id"
        class="notifications-page-item"
        :class="{ 'is-unread': !item.read }"
      >
        <div>
          <p class="notification-title">{{ item.title }}</p>
          <p class="notification-copy">{{ item.message }}</p>
        </div>
        <p class="notification-time">{{ item.time }}</p>
      </li>
    </ul>

    <p v-else class="notification-empty">No notifications yet.</p>
  </section>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { useTopbarNotifications } from '../../composables/useTopbarNotifications';

const route = useRoute();

const roleKey = computed(() => {
  if (route.path.startsWith('/admin')) {
    return 'admin';
  }

  if (route.path.startsWith('/agent')) {
    return 'agent';
  }

  return 'policyholder';
});

const { notifications, hasUnreadNotifications, markAllRead, loadNotifications } = useTopbarNotifications(roleKey.value);
</script>

<template>
  <section>
    <header class="page-head">
      <h1>Messages</h1>
      <p>Communicate with policyholders about claim updates</p>
    </header>

    <section class="agent-messages-grid panel">
      <aside class="chat-list">
        <input v-model="query" class="search-input" type="text" placeholder="Search conversations..." />

        <button
          v-for="chat in filteredChats"
          :key="chat.id"
          class="chat-item"
          :class="{ active: chat.id === selectedChat.id }"
          type="button"
          @click="selectedChat = chat"
        >
          <div class="avatar-soft">{{ chat.initials }}</div>
          <div class="chat-meta">
            <p>{{ chat.name }}</p>
            <small>{{ chat.claimId }}</small>
          </div>
        </button>
      </aside>

      <article class="chat-window">
        <header class="chat-window-head">
          <h2>{{ selectedChat.name }}</h2>
          <p>{{ selectedChat.claimId }}</p>
        </header>

        <div class="chat-bubbles">
          <div
            v-for="message in selectedChat.messages"
            :key="message.id"
            class="chat-bubble"
            :class="message.from"
          >
            {{ message.text }}
          </div>
        </div>

        <form class="chat-input-row" @submit.prevent="sendMessage">
          <input v-model="draft" type="text" placeholder="Type a message..." />
          <button type="submit" class="primary-btn">Send</button>
        </form>
      </article>
    </section>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue';

const query = ref('');
const draft = ref('');

const chats = ref([
  {
    id: 1,
    name: 'Sarah Mitchell',
    initials: 'SM',
    claimId: 'CLM-2024-001',
    messages: [
      { id: 1, from: 'in', text: 'Hi, has my claim review started?' },
      { id: 2, from: 'out', text: 'Yes, I am currently reviewing your documents.' }
    ]
  },
  {
    id: 2,
    name: 'John Davis',
    initials: 'JD',
    claimId: 'CLM-2024-004',
    messages: [
      { id: 1, from: 'in', text: 'Uploaded additional medical bill.' },
      { id: 2, from: 'out', text: 'Received, thank you. I will validate it today.' }
    ]
  }
]);

const selectedChat = ref(chats.value[0]);

const filteredChats = computed(() => {
  const q = query.value.trim().toLowerCase();

  if (!q) {
    return chats.value;
  }

  return chats.value.filter((chat) => `${chat.name} ${chat.claimId}`.toLowerCase().includes(q));
});

function sendMessage() {
  const text = draft.value.trim();

  if (!text) {
    return;
  }

  selectedChat.value.messages.push({
    id: Date.now(),
    from: 'out',
    text
  });
  draft.value = '';
}
</script>

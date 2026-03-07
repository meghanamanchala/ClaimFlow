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
          :class="{ active: chat.id === selectedChat?.id }"
          type="button"
          @click="selectedChat = chat"
        >
          <div class="avatar-soft">{{ chat.initials }}</div>
          <div class="chat-meta">
            <p>{{ chat.name }}</p>
            <small>{{ chat.claimNumber }}</small>
          </div>
        </button>
      </aside>

      <article class="chat-window">
        <header class="chat-window-head" v-if="selectedChat">
          <h2>{{ selectedChat.name }}</h2>
          <p>{{ selectedChat.claimNumber }}</p>
        </header>

        <div class="chat-bubbles" v-if="selectedChat">
          <div v-for="message in selectedChat.messages" :key="message.id" class="chat-bubble" :class="message.from">
            {{ message.text }}
          </div>
        </div>

        <p v-if="!selectedChat" class="empty-state">No conversations available.</p>

        <form class="chat-input-row" @submit.prevent="sendMessage" v-if="selectedChat">
          <input v-model="draft" type="text" placeholder="Type a message..." />
          <button type="submit" class="primary-btn">Send</button>
        </form>
      </article>
    </section>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { createMessage, getClaims, getMessages } from '../../services/api';
import { formatDate, getStatusLabel } from '../../services/claimTransforms';

const query = ref('');
const draft = ref('');
const chats = ref([]);
const selectedChat = ref(null);

const filteredChats = computed(() => {
  const q = query.value.trim().toLowerCase();

  if (!q) {
    return chats.value;
  }

  return chats.value.filter((chat) => `${chat.name} ${chat.claimNumber}`.toLowerCase().includes(q));
});

async function sendMessage() {
  const text = draft.value.trim();

  if (!text || !selectedChat.value) {
    return;
  }

  try {
    await createMessage({
      claimId: selectedChat.value.id,
      content: text
    });

    const { data } = await getMessages({ claimId: selectedChat.value.id });
    selectedChat.value.messages = (data || []).map((message) => ({
      id: message.id,
      from: 'out',
      text: `${message.senderName || 'User'}: ${message.content}`
    }));
    draft.value = '';
  } catch {
    selectedChat.value.messages.push({
      id: Date.now(),
      from: 'out',
      text
    });
    draft.value = '';
  }
}

onMounted(async () => {
  try {
    const { data } = await getClaims();
    const claimList = data || [];
    chats.value = await Promise.all(claimList.map(async (claim) => {
      const timelineMessages = (claim.timeline || []).map((item, index) => ({
        id: `${claim.id}-${index}`,
        from: 'in',
        text: `${item.step} on ${formatDate(item.date)}.`
      }));

      let persistedMessages = [];
      try {
        const response = await getMessages({ claimId: claim.id });
        persistedMessages = (response.data || []).map((message) => ({
          id: message.id,
          from: 'in',
          text: `${message.senderName || 'User'}: ${message.content}`
        }));
      } catch {
        persistedMessages = [];
      }

      return {
        id: claim.id,
        name: `User #${claim.userId}`,
        initials: 'U',
        claimNumber: claim.claimNumber,
        messages: [
          {
            id: `${claim.id}-status`,
            from: 'in',
            text: `Current status: ${getStatusLabel(claim.status)}.`
          },
          ...persistedMessages,
          ...timelineMessages
        ]
      };
    }));

    selectedChat.value = chats.value[0] || null;
  } catch {
    chats.value = [];
    selectedChat.value = null;
  }
});
</script>

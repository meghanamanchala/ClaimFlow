<template>
  <section>
    <header class="page-head page-head-row">
      <div>
        <h1>User Management</h1>
        <p>Manage policyholders and agents</p>
      </div>
      <button type="button" class="primary-btn" @click="openCreateModal">Add User</button>
    </header>

    <div class="toolbar-row">
      <input v-model="search" class="search-input" type="text" placeholder="Search users..." />
    </div>

    <p v-if="errorMessage" class="message error">{{ errorMessage }}</p>
    <p v-if="successMessage" class="message success">{{ successMessage }}</p>

    <article class="panel">
      <table class="data-table">
        <thead>
          <tr>
            <th>User</th>
            <th>Role</th>
            <th>Status</th>
            <th>Claims</th>
            <th>Joined</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id">
            <td>
              <div class="user-cell">
                <div class="avatar-soft">{{ initialsFor(user.name) }}</div>
                <div>
                  <p class="user-name">{{ user.name }}</p>
                  <p class="user-email">{{ user.email }}</p>
                </div>
              </div>
            </td>
            <td><span class="badge" :class="roleClass(user.role)">{{ roleLabel(user.role) }}</span></td>
            <td><span class="badge" :class="statusClass(user.status)">{{ roleLabel(user.status) }}</span></td>
            <td>{{ claimCount[user.id] || 0 }}</td>
            <td>{{ formatDate(user.createdAt) }}</td>
            <td class="actions-cell">
              <button type="button" class="icon-btn" @click="toggleUserActions(user.id)">...</button>
              <Transition name="action-menu-fade">
                <div v-if="actionMenuFor === user.id" class="action-menu">
                  <button
                    type="button"
                    class="action-menu-item"
                    :disabled="statusBusyUserId === user.id"
                    @click="setUserStatus(user, user.status === 'active' ? 'inactive' : 'active')"
                  >
                    {{ user.status === 'active' ? 'Deactivate' : 'Activate' }}
                  </button>
                  <button
                    type="button"
                    class="action-menu-item"
                    :disabled="statusBusyUserId === user.id"
                    @click="setUserStatus(user, 'suspended')"
                  >
                    Suspend
                  </button>
                </div>
              </Transition>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="!filteredUsers.length" class="empty-state">No users found.</p>
    </article>

    <div v-if="showCreateModal" class="modal-backdrop" @click.self="closeCreateModal">
      <div class="modal-card">
        <h3>Add User</h3>
        <p class="modal-subtitle">Create a new policyholder, agent, or admin account.</p>

        <label class="field">
          <span>Name</span>
          <input v-model="newUser.name" type="text" placeholder="Full name" />
        </label>

        <label class="field">
          <span>Email</span>
          <input v-model="newUser.email" type="email" placeholder="name@example.com" />
        </label>

        <label class="field">
          <span>Password</span>
          <input v-model="newUser.password" type="password" placeholder="Create a password" />
        </label>

        <label class="field">
          <span>Role</span>
          <select v-model="newUser.role" class="filter-select">
            <option value="policyholder">Policyholder</option>
            <option value="agent">Agent</option>
            <option value="admin">Admin</option>
          </select>
        </label>

        <div class="modal-actions">
          <button type="button" class="ghost-btn" :disabled="createLoading" @click="closeCreateModal">Cancel</button>
          <button type="button" class="primary-btn" :disabled="createLoading" @click="createUser">
            {{ createLoading ? 'Creating...' : 'Create User' }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';
import { getClaims, getUsers, registerUser, updateUserStatus } from '../../services/api';
import { formatDate, toTitleCase } from '../../services/claimTransforms';

const search = ref('');
const users = ref([]);
const claims = ref([]);
const showCreateModal = ref(false);
const createLoading = ref(false);
const statusBusyUserId = ref(null);
const actionMenuFor = ref(null);
const errorMessage = ref('');
const successMessage = ref('');
let actionMenuSwitchTimeoutId = null;

const newUser = ref({
  name: '',
  email: '',
  password: '',
  role: 'policyholder'
});

const claimCount = computed(() => {
  return claims.value.reduce((acc, claim) => {
    acc[claim.userId] = (acc[claim.userId] || 0) + 1;
    return acc;
  }, {});
});

const filteredUsers = computed(() => {
  const q = search.value.trim().toLowerCase();

  if (!q) {
    return users.value;
  }

  return users.value.filter((user) => `${user.name} ${user.email}`.toLowerCase().includes(q));
});

function initialsFor(name) {
  return String(name || '')
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((token) => token[0]?.toUpperCase())
    .join('');
}

function roleClass(role) {
  return String(role || '').toLowerCase() === 'agent' ? 'badge-review' : 'badge-pending';
}

function statusClass(status) {
  return String(status || '').toLowerCase() === 'active' ? 'badge-approved' : 'badge-inactive';
}

function roleLabel(value) {
  return toTitleCase(value || 'unknown');
}

function openCreateModal() {
  errorMessage.value = '';
  successMessage.value = '';
  showCreateModal.value = true;
}

function closeCreateModal() {
  showCreateModal.value = false;
  newUser.value = {
    name: '',
    email: '',
    password: '',
    role: 'policyholder'
  };
}

function toggleUserActions(userId) {
  if (actionMenuSwitchTimeoutId) {
    window.clearTimeout(actionMenuSwitchTimeoutId);
    actionMenuSwitchTimeoutId = null;
  }

  if (actionMenuFor.value === userId) {
    actionMenuFor.value = null;
    return;
  }

  if (!actionMenuFor.value) {
    actionMenuFor.value = userId;
    return;
  }

  actionMenuFor.value = null;
  actionMenuSwitchTimeoutId = window.setTimeout(() => {
    actionMenuFor.value = userId;
    actionMenuSwitchTimeoutId = null;
  }, 110);
}

function closeActionMenu() {
  actionMenuFor.value = null;
}

function handleDocumentClick(event) {
  if (!actionMenuFor.value) {
    return;
  }

  const target = event.target;
  if (!(target instanceof Element)) {
    closeActionMenu();
    return;
  }

  if (!target.closest('.actions-cell')) {
    closeActionMenu();
  }
}

function handleDocumentKeydown(event) {
  if (event.key === 'Escape') {
    closeActionMenu();
  }
}

async function loadUsersAndClaims() {
  const [usersResponse, claimsResponse] = await Promise.all([getUsers(), getClaims()]);
  users.value = usersResponse.data || [];
  claims.value = claimsResponse.data || [];
}

async function createUser() {
  const payload = {
    name: String(newUser.value.name || '').trim(),
    email: String(newUser.value.email || '').trim().toLowerCase(),
    password: newUser.value.password,
    role: newUser.value.role
  };

  if (!payload.name || !payload.email || !payload.password) {
    errorMessage.value = 'Please fill name, email, and password.';
    return;
  }

  try {
    createLoading.value = true;
    errorMessage.value = '';
    successMessage.value = '';
    await registerUser(payload);
    await loadUsersAndClaims();
    closeCreateModal();
    successMessage.value = 'User created successfully.';
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to create user.';
  } finally {
    createLoading.value = false;
  }
}

async function setUserStatus(user, status) {
  try {
    statusBusyUserId.value = user.id;
    errorMessage.value = '';
    successMessage.value = '';
    await updateUserStatus(user.id, status);
    await loadUsersAndClaims();
    successMessage.value = `${user.name} is now ${status}.`;
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to update user status.';
  } finally {
    statusBusyUserId.value = null;
    actionMenuFor.value = null;
  }
}

onMounted(async () => {
  document.addEventListener('click', handleDocumentClick);
  document.addEventListener('keydown', handleDocumentKeydown);

  try {
    await loadUsersAndClaims();
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to load users.';
    users.value = [];
    claims.value = [];
  }
});

onBeforeUnmount(() => {
  if (actionMenuSwitchTimeoutId) {
    window.clearTimeout(actionMenuSwitchTimeoutId);
    actionMenuSwitchTimeoutId = null;
  }

  document.removeEventListener('click', handleDocumentClick);
  document.removeEventListener('keydown', handleDocumentKeydown);
});
</script>

<style scoped>
.actions-cell {
  position: relative;
}

.action-menu {
  position: absolute;
  top: calc(100% + 0.3rem);
  right: 0;
  min-width: 140px;
  background: #fff;
  border: 1px solid #d8e1f0;
  border-radius: 10px;
  box-shadow: 0 12px 22px rgba(11, 28, 53, 0.14);
  z-index: 20;
}

.action-menu-item {
  width: 100%;
  text-align: left;
  border: 0;
  background: transparent;
  padding: 0.55rem 0.7rem;
  cursor: pointer;
}

.action-menu-item:hover:not(:disabled) {
  background: #f3f7ff;
}

.action-menu-fade-enter-active,
.action-menu-fade-leave-active {
  transition: opacity 110ms ease, transform 110ms ease;
}

.action-menu-fade-enter-from,
.action-menu-fade-leave-to {
  opacity: 0;
  transform: translateY(-3px);
}

.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(13, 23, 39, 0.45);
  display: grid;
  place-items: center;
  z-index: 60;
  padding: 1rem;
}

.modal-card {
  width: min(460px, 100%);
  background: #fff;
  border-radius: 14px;
  padding: 1rem;
  box-shadow: 0 18px 42px rgba(11, 28, 53, 0.2);
}

.modal-card h3 {
  margin: 0;
}

.modal-subtitle {
  margin: 0.3rem 0 1rem;
  color: #5f7394;
}

.modal-actions {
  margin-top: 1rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}
</style>

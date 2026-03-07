<template>
  <section>
    <header class="page-head">
      <h1>Review Claim</h1>
      <p>Review details and track progress on this claim</p>
    </header>

    <p v-if="loading" class="empty-state">Loading claim details...</p>
    <p v-else-if="errorMessage" class="message error">{{ errorMessage }}</p>

    <div v-else-if="selectedClaim" class="agent-review-grid">
      <div>
        <article class="panel">
          <div class="review-card-header">
            <h2>{{ selectedClaim.claimNumber }}</h2>
            <span class="badge" :class="getStatusClass(selectedClaim.status)">{{ getStatusLabel(selectedClaim.status) }}</span>
          </div>

          <div class="review-info-grid">
            <div>
              <p class="review-label">Type</p>
              <p>{{ selectedClaim.claimType }}</p>
            </div>
            <div>
              <p class="review-label">Policy #</p>
              <p>{{ selectedClaim.policyNumber }}</p>
            </div>
            <div>
              <p class="review-label">Incident Date</p>
              <p>{{ formatDate(selectedClaim.incidentDate) }}</p>
            </div>
            <div>
              <p class="review-label">Claimed Amount</p>
              <p>{{ formatCurrency(selectedClaim.estimatedAmount) }}</p>
            </div>
          </div>

          <div>
            <p class="review-label">Description</p>
            <p>{{ selectedClaim.description }}</p>
          </div>
        </article>

        <article class="panel claim-documents-panel">
          <h2>Attached Documents</h2>
          <ul class="document-items">
            <li v-for="doc in selectedClaim.documents" :key="doc.fileName + doc.uploadedAt">
              <span>{{ doc.fileName }}</span>
              <button type="button" class="link-btn" @click="openDocument(doc.fileUrl)">View</button>
            </li>
            <li v-if="!selectedClaim.documents?.length" class="empty-state">No documents attached.</li>
          </ul>
        </article>
      </div>

      <div class="review-side-stack">
        <article class="panel">
          <h2>Policyholder</h2>
          <div class="policyholder-mini-card">
            <div class="avatar-soft">U</div>
            <div>
              <p class="policyholder-name">User #{{ selectedClaim.userId }}</p>
              <p class="policyholder-email">Policy {{ selectedClaim.policyNumber }}</p>
            </div>
          </div>
          <RouterLink class="ghost-btn full-width" to="/agent/messages">Send Message</RouterLink>
        </article>

        <article class="panel">
          <h2>Claim Progress</h2>
          <ol class="progress-list">
            <li v-for="step in progressSteps" :key="`${step.step}-${step.date}`" class="progress-item">
              <div class="progress-dot" :class="step.state"></div>
              <div>
                <p class="progress-title">{{ step.step }}</p>
                <p class="progress-date">{{ formatDate(step.date) }}</p>
              </div>
            </li>
            <li v-if="progressSteps.length === 0" class="empty-state">No timeline available.</li>
          </ol>
        </article>

        <article class="panel">
          <h2>Decision</h2>
          <label class="field">
            <span>Notes</span>
            <textarea rows="4" v-model="notes" placeholder="Add review notes..."></textarea>
          </label>
          <p v-if="decisionMessage" class="form-message success">{{ decisionMessage }}</p>
          <div class="decision-actions">
            <button type="button" class="danger-btn" :disabled="decisionLoading" @click="applyDecision('rejected')">
              {{ decisionLoading ? 'Saving...' : 'Reject' }}
            </button>
            <button type="button" class="primary-btn" :disabled="decisionLoading" @click="applyDecision('approved')">
              {{ decisionLoading ? 'Saving...' : 'Approve' }}
            </button>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { getClaimById, getClaims, updateClaimDecision } from '../../services/api';
import { formatCurrency, formatDate, getStatusClass, getStatusLabel } from '../../services/claimTransforms';

const route = useRoute();
const selectedClaim = ref(null);
const notes = ref('');
const loading = ref(true);
const errorMessage = ref('');
const decisionLoading = ref(false);
const decisionMessage = ref('');

const progressSteps = computed(() => {
  const timeline = selectedClaim.value?.timeline || [];

  return timeline.map((item, index) => {
    const isLast = index === timeline.length - 1;
    return {
      ...item,
      state: isLast ? 'is-active' : 'is-done'
    };
  });
});

function openDocument(url) {
  if (!url) {
    return;
  }

  window.open(url, '_blank', 'noopener,noreferrer');
}

async function loadClaim() {
  const claimId = Number(route.query.claimId || 0);

  if (claimId) {
    const { data } = await getClaimById(claimId);
    selectedClaim.value = data;
    return;
  }

  const { data } = await getClaims();
  selectedClaim.value = (data || [])[0] || null;
}

async function applyDecision(decision) {
  if (!selectedClaim.value?.id) {
    return;
  }

  decisionLoading.value = true;
  decisionMessage.value = '';
  errorMessage.value = '';

  try {
    await updateClaimDecision(selectedClaim.value.id, {
      decision,
      agentNotes: notes.value,
      rejectionReason: decision === 'rejected' ? notes.value || 'Rejected by agent' : undefined
    });
    decisionMessage.value = `Claim ${decision} successfully.`;
    await loadClaim();
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Unable to update claim decision.';
  } finally {
    decisionLoading.value = false;
  }
}

onMounted(async () => {
  loading.value = true;
  errorMessage.value = '';

  try {
    await loadClaim();
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Unable to load claim details.';
  } finally {
    loading.value = false;
  }
});
</script>

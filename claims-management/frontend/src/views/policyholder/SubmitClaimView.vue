<template>
  <section>
    <header class="page-head">
      <h1>Submit New Claim</h1>
      <p>Complete all steps to submit your insurance claim</p>
    </header>

    <section class="panel submit-panel">
      <ol class="wizard-steps">
        <li v-for="step in steps" :key="step.id" class="wizard-step">
          <div class="wizard-dot" :class="dotClass(step.id)">{{ step.id }}</div>
          <span :class="{ 'is-current-label': step.id === currentStep }">{{ step.label }}</span>
        </li>
      </ol>

      <div v-if="currentStep === 1" class="wizard-body">
        <label class="field">
          <span>Claim Type</span>
          <select v-model="form.claimType">
            <option disabled value="">Select claim type</option>
            <option>Auto Insurance</option>
            <option>Health Insurance</option>
            <option>Property Insurance</option>
            <option>Travel Insurance</option>
          </select>
        </label>

        <label class="field">
          <span>Policy Number</span>
          <input v-model="form.policyNumber" type="text" placeholder="POL-XXXX-XXXX" />
        </label>
      </div>

      <div v-if="currentStep === 2" class="wizard-body">
        <label class="field">
          <span>Incident Date</span>
          <input v-model="form.incidentDate" type="date" />
        </label>

        <label class="field">
          <span>Estimated Amount ($)</span>
          <input v-model.number="form.amount" type="number" min="0" step="0.01" />
        </label>

        <label class="field">
          <span>Description</span>
          <textarea v-model="form.description" rows="4" placeholder="Describe the incident..."></textarea>
        </label>
      </div>

      <div v-if="currentStep === 3" class="wizard-body">
        <label class="upload-box" for="claim-documents">
          <input id="claim-documents" type="file" multiple @change="onFileSelected" />
          <p class="upload-title">Drop files here or click to upload</p>
          <p class="upload-help">PDF, JPG, PNG up to 10MB each</p>
          <span class="select-files-btn">Select Files</span>
        </label>

        <ul v-if="documents.length" class="file-list">
          <li v-for="file in documents" :key="file.name + file.size">{{ file.name }}</li>
        </ul>
      </div>

      <div v-if="currentStep === 4" class="wizard-body">
        <h2 class="review-title">Review Your Claim</h2>
        <div class="review-grid">
          <article>
            <p class="review-label">Claim Type</p>
            <p>{{ form.claimType || '-' }}</p>
          </article>
          <article>
            <p class="review-label">Policy Number</p>
            <p>{{ form.policyNumber || '-' }}</p>
          </article>
          <article>
            <p class="review-label">Incident Date</p>
            <p>{{ displayDate }}</p>
          </article>
          <article>
            <p class="review-label">Amount</p>
            <p>{{ displayAmount }}</p>
          </article>
          <article>
            <p class="review-label">Description</p>
            <p>{{ form.description || '-' }}</p>
          </article>
          <article>
            <p class="review-label">Documents</p>
            <p>{{ documents.length }} file(s)</p>
          </article>
        </div>
      </div>

      <div class="wizard-actions">
        <button type="button" class="ghost-btn" @click="goBack" :disabled="currentStep === 1">Back</button>
        <button
          v-if="currentStep < 4"
          type="button"
          class="primary-btn"
          @click="goNext"
          :disabled="nextDisabled"
        >
          Next
        </button>
        <button v-else type="button" class="primary-btn" @click="submitClaim">Submit Claim</button>
      </div>

      <p v-if="message" class="form-message success">{{ message }}</p>
    </section>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue';

const currentStep = ref(1);
const message = ref('');

const form = ref({
  claimType: '',
  policyNumber: '',
  incidentDate: '',
  amount: 0,
  description: ''
});

const documents = ref([]);

const steps = [
  { id: 1, label: 'Claim Type' },
  { id: 2, label: 'Details' },
  { id: 3, label: 'Documents' },
  { id: 4, label: 'Review' }
];

const nextDisabled = computed(() => {
  if (currentStep.value === 1) {
    return !form.value.claimType || !form.value.policyNumber;
  }

  if (currentStep.value === 2) {
    return !form.value.incidentDate || !form.value.amount || !form.value.description;
  }

  return false;
});

const displayDate = computed(() => form.value.incidentDate || '-');
const displayAmount = computed(() => {
  if (!form.value.amount) {
    return '-';
  }

  return `$${Number(form.value.amount).toLocaleString()}`;
});

function onFileSelected(event) {
  const files = Array.from(event.target.files || []);
  documents.value = files;
}

function dotClass(stepId) {
  if (stepId < currentStep.value) {
    return 'is-done';
  }

  if (stepId === currentStep.value) {
    return 'is-current';
  }

  return 'is-upcoming';
}

function goNext() {
  if (currentStep.value < 4) {
    currentStep.value += 1;
  }
}

function goBack() {
  if (currentStep.value > 1) {
    currentStep.value -= 1;
  }
}

function submitClaim() {
  message.value = 'Claim submitted successfully.';
  currentStep.value = 1;
  form.value = {
    claimType: '',
    policyNumber: '',
    incidentDate: '',
    amount: 0,
    description: ''
  };
  documents.value = [];
}
</script>

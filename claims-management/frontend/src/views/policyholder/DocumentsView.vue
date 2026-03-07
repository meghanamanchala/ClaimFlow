<template>
  <section>
    <header class="page-head page-head-row">
      <div>
        <h1>Documents</h1>
        <p>Manage your uploaded files and claim documents</p>
      </div>
      <div class="upload-controls">
        <select v-model="selectedClaimId" class="filter-select">
          <option disabled value="">Select Claim</option>
          <option v-for="claim in claims" :key="claim.id" :value="claim.id">
            {{ claim.claimNumber }}
          </option>
        </select>
        <button type="button" class="primary-btn" @click="openPicker">Upload Document</button>
      </div>
      <input ref="picker" type="file" class="hidden-file-input" @change="addDocument" />
    </header>

    <article class="panel">
      <h2>All Documents</h2>
      <p v-if="loading" class="empty-state">Loading documents...</p>
      <p v-else-if="errorMessage" class="message error">{{ errorMessage }}</p>

      <table v-else class="data-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Size</th>
            <th>Date</th>
            <th>Claim</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="doc in documents" :key="doc.id">
            <td>{{ doc.name }}</td>
            <td>{{ doc.type }}</td>
            <td>{{ doc.size }}</td>
            <td>{{ doc.date }}</td>
            <td>{{ doc.claimNumber }}</td>
            <td>
              <div class="table-actions">
                <button type="button" @click="previewDocument(doc)">View</button>
                <button type="button" @click="downloadDocument(doc)">Download</button>
              </div>
            </td>
          </tr>
          <tr v-if="documents.length === 0">
            <td colspan="6" class="empty-state">No documents uploaded yet.</td>
          </tr>
        </tbody>
      </table>
      <p v-if="toast" class="form-message">{{ toast }}</p>
    </article>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { getClaims, uploadClaimDocument } from '../../services/api';
import { formatDate } from '../../services/claimTransforms';

const picker = ref(null);
const toast = ref('');
const claims = ref([]);
const selectedClaimId = ref('');
const loading = ref(true);
const errorMessage = ref('');

const documents = computed(() => {
  const flattened = [];

  claims.value.forEach((claim) => {
    (claim.documents || []).forEach((doc, index) => {
      flattened.push({
        id: `${claim.id}-${index}-${doc.fileName}`,
        name: doc.fileName,
        type: doc.fileType,
        size: `${Number(doc.size || 0).toFixed(1)} MB`,
        date: formatDate(doc.uploadedAt),
        claimNumber: claim.claimNumber,
        fileUrl: doc.fileUrl
      });
    });
  });

  return flattened.sort((a, b) => String(b.date).localeCompare(String(a.date)));
});

function openPicker() {
  if (!selectedClaimId.value) {
    toast.value = 'Select a claim before uploading a document.';
    return;
  }

  picker.value?.click();
}

async function addDocument(event) {
  const file = event.target.files?.[0];

  if (!file || !selectedClaimId.value) {
    return;
  }

  try {
    await uploadClaimDocument(selectedClaimId.value, {
      fileName: file.name,
      fileUrl: file.name,
      fileType: (file.name.split('.').pop() || 'file').toUpperCase(),
      size: Number((file.size / 1024 / 1024).toFixed(3))
    });

    const { data } = await getClaims();
    claims.value = data || [];
    toast.value = 'Document uploaded successfully.';
  } catch (error) {
    toast.value = error.response?.data?.detail || 'Document upload failed.';
  } finally {
    event.target.value = '';
  }
}

function previewDocument(doc) {
  if (!doc.fileUrl) {
    toast.value = 'No file URL available for preview.';
    return;
  }

  window.open(doc.fileUrl, '_blank', 'noopener,noreferrer');
}

function downloadDocument(doc) {
  previewDocument(doc);
}

onMounted(async () => {
  loading.value = true;
  errorMessage.value = '';

  try {
    const { data } = await getClaims();
    claims.value = data || [];
    if (claims.value[0]) {
      selectedClaimId.value = claims.value[0].id;
    }
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Unable to load documents.';
  } finally {
    loading.value = false;
  }
});
</script>

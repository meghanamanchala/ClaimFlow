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
            <td>
              <div class="file-name-wrap">
                <span class="file-type-icon" :class="`is-${getFileKind(doc.type, doc.name)}`" aria-hidden="true">
                  <svg v-if="getFileKind(doc.type, doc.name) === 'pdf'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H7a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"></path>
                    <path d="M14 2v6h6"></path>
                    <path d="M9 14h6"></path>
                  </svg>
                  <svg v-else-if="getFileKind(doc.type, doc.name) === 'image'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="4" width="18" height="16" rx="2"></rect>
                    <circle cx="9" cy="10" r="1.5"></circle>
                    <path d="m21 16-5-5-8 8"></path>
                  </svg>
                  <svg v-else-if="getFileKind(doc.type, doc.name) === 'archive'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 7h16v13H4z"></path>
                    <path d="M9 7V3h6v4"></path>
                    <path d="M10 12h4"></path>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H7a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"></path>
                    <path d="M14 2v6h6"></path>
                    <path d="M9 13h6"></path>
                    <path d="M9 17h6"></path>
                  </svg>
                </span>
                <span>{{ doc.name }}</span>
              </div>
            </td>
            <td>{{ doc.type }}</td>
            <td>{{ doc.size }}</td>
            <td>{{ doc.date }}</td>
            <td>{{ doc.claimNumber }}</td>
            <td>
              <div class="table-actions">
                <button type="button" class="action-icon action-view" aria-label="View document" @click="previewDocument(doc)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                </button>
                <button type="button" class="action-icon action-download" aria-label="Download document" @click="downloadDocument(doc)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <path d="M12 3v12"></path>
                    <path d="m7 10 5 5 5-5"></path>
                    <path d="M5 21h14"></path>
                  </svg>
                </button>
                <button type="button" class="action-icon danger-action" aria-label="Delete document" @click="removeDocument(doc)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <path d="M3 6h18"></path>
                    <path d="M8 6V4h8v2"></path>
                    <path d="M19 6l-1 14H6L5 6"></path>
                    <path d="M10 11v6"></path>
                    <path d="M14 11v6"></path>
                  </svg>
                </button>
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
import { deleteClaimDocument, getClaims, uploadClaimDocumentFile } from '../../services/api';
import { formatDate } from '../../services/claimTransforms';

const picker = ref(null);
const toast = ref('');
const claims = ref([]);
const selectedClaimId = ref('');
const loading = ref(true);
const errorMessage = ref('');
const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');

const documents = computed(() => {
  const flattened = [];

  claims.value.forEach((claim) => {
    (claim.documents || []).forEach((doc, index) => {
      flattened.push({
        id: `${claim.id}-${index}-${doc.fileName}`,
        claimId: claim.id,
        name: doc.fileName,
        type: doc.fileType,
        size: `${Number(doc.size || 0).toFixed(1)} MB`,
        uploadedAt: doc.uploadedAt,
        date: formatDate(doc.uploadedAt),
        claimNumber: claim.claimNumber,
        fileUrl: doc.fileUrl,
      });
    });
  });

  return flattened.sort((a, b) => new Date(b.uploadedAt || 0) - new Date(a.uploadedAt || 0));
});

function getFileKind(type, name) {
  const normalizedType = String(type || '').toLowerCase();
  const normalizedName = String(name || '').toLowerCase();

  if (normalizedType.includes('pdf') || normalizedName.endsWith('.pdf')) {
    return 'pdf';
  }

  if (
    normalizedType.includes('jpg') ||
    normalizedType.includes('jpeg') ||
    normalizedType.includes('png') ||
    normalizedType.includes('gif') ||
    normalizedType.includes('image') ||
    /\.(jpg|jpeg|png|gif|webp|bmp|svg)$/.test(normalizedName)
  ) {
    return 'image';
  }

  if (
    normalizedType.includes('zip') ||
    normalizedType.includes('rar') ||
    normalizedType.includes('tar') ||
    normalizedType.includes('archive') ||
    /\.(zip|rar|7z|tar|gz)$/.test(normalizedName)
  ) {
    return 'archive';
  }

  return 'file';
}

function isPreviewableUrl(value) {
  const raw = String(value || '').trim();
  if (!raw) {
    return false;
  }

  return /^(https?:|data:|blob:|\/uploads\/)/i.test(raw);
}

function resolveFileUrl(value) {
  const raw = String(value || '').trim();
  if (!raw) {
    return '';
  }

  if (/^https?:/i.test(raw)) {
    return raw;
  }

  if (raw.startsWith('/uploads/')) {
    return `${API_BASE_URL}${raw}`;
  }

  return raw;
}

function isLocalUploadUrl(rawValue, resolvedUrl) {
  const raw = String(rawValue || '').trim();
  const resolved = String(resolvedUrl || '').trim();
  return raw.startsWith('/uploads/') || resolved.startsWith(`${API_BASE_URL}/uploads/`);
}

async function ensureDocumentAvailable(doc) {
  const resolvedUrl = resolveFileUrl(doc.fileUrl);
  if (!resolvedUrl) {
    toast.value = 'File URL is missing.';
    return '';
  }

  if (!isLocalUploadUrl(doc.fileUrl, resolvedUrl)) {
    return resolvedUrl;
  }

  try {
    const response = await fetch(resolvedUrl, { method: 'HEAD' });
    if (response.ok) {
      return resolvedUrl;
    }

    if (response.status === 404) {
      toast.value = 'File missing on server, please re-upload.';
      return '';
    }

    toast.value = `Unable to access file (HTTP ${response.status}).`;
    return '';
  } catch {
    toast.value = 'Unable to reach file server right now.';
    return '';
  }
}

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
    await uploadClaimDocumentFile(selectedClaimId.value, file);

    const { data } = await getClaims();
    claims.value = data || [];
    toast.value = 'Document uploaded successfully.';
  } catch (error) {
    toast.value = error.response?.data?.detail || 'Document upload failed.';
  } finally {
    event.target.value = '';
  }
}

async function previewDocument(doc) {
  if (!isPreviewableUrl(doc.fileUrl)) {
    toast.value = 'Preview is unavailable because the file URL is not hosted.';
    return;
  }

  const resolvedUrl = await ensureDocumentAvailable(doc);
  if (!resolvedUrl) {
    return;
  }

  window.open(resolvedUrl, '_blank', 'noopener,noreferrer');
}

async function downloadDocument(doc) {
  if (!isPreviewableUrl(doc.fileUrl)) {
    toast.value = 'Download is unavailable because the file URL is not hosted.';
    return;
  }

  const resolvedUrl = await ensureDocumentAvailable(doc);
  if (!resolvedUrl) {
    return;
  }

  const link = document.createElement('a');
  link.href = resolvedUrl;
  link.download = doc.name || 'document';
  link.target = '_blank';
  link.rel = 'noopener noreferrer';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

async function removeDocument(doc) {
  if (!confirm(`Delete document "${doc.name}"?`)) {
    return;
  }

  try {
    await deleteClaimDocument(doc.claimId, {
      fileName: doc.name,
      fileUrl: doc.fileUrl,
      uploadedAt: doc.uploadedAt,
    });

    const { data } = await getClaims();
    claims.value = data || [];
    toast.value = 'Document deleted successfully.';
  } catch (error) {
    toast.value = error.response?.data?.detail || 'Unable to delete document.';
  }
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

<template>
  <section>
    <header class="page-head page-head-row">
      <div>
        <h1>Documents</h1>
        <p>Manage your uploaded files and claim documents</p>
      </div>
      <button type="button" class="primary-btn" @click="openPicker">Upload Document</button>
      <input ref="picker" type="file" class="hidden-file-input" @change="addDocument" />
    </header>

    <article class="panel">
      <h2>All Documents</h2>
      <table class="data-table">
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
            <td>{{ doc.claim }}</td>
            <td>
              <div class="table-actions">
                <button type="button" @click="previewDocument(doc)">View</button>
                <button type="button" @click="downloadDocument(doc)">Download</button>
                <button type="button" class="danger-action" @click="removeDocument(doc.id)">Delete</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="toast" class="form-message">{{ toast }}</p>
    </article>
  </section>
</template>

<script setup>
import { ref } from 'vue';

const picker = ref(null);
const toast = ref('');

const documents = ref([
  {
    id: 1,
    name: 'Police Report - Auto Incident',
    type: 'PDF',
    size: '2.4 MB',
    date: 'Mar 2, 2026',
    claim: 'CLM-2024-001'
  },
  {
    id: 2,
    name: 'Medical Bills Receipt',
    type: 'PDF',
    size: '1.1 MB',
    date: 'Feb 15, 2026',
    claim: 'CLM-2024-002'
  },
  {
    id: 3,
    name: 'Property Damage Photos',
    type: 'JPG',
    size: '5.8 MB',
    date: 'Jan 28, 2026',
    claim: 'CLM-2024-003'
  },
  {
    id: 4,
    name: 'Insurance Policy Copy',
    type: 'PDF',
    size: '890 KB',
    date: 'Jan 10, 2026',
    claim: '-'
  },
  {
    id: 5,
    name: 'Repair Estimate',
    type: 'PDF',
    size: '340 KB',
    date: 'Mar 4, 2026',
    claim: 'CLM-2024-001'
  }
]);

function openPicker() {
  picker.value?.click();
}

function addDocument(event) {
  const file = event.target.files?.[0];

  if (!file) {
    return;
  }

  documents.value.unshift({
    id: Date.now(),
    name: file.name,
    type: (file.name.split('.').pop() || 'FILE').toUpperCase(),
    size: `${(file.size / 1024 / 1024).toFixed(1)} MB`,
    date: 'Today',
    claim: '-'
  });

  toast.value = 'Document uploaded.';
  event.target.value = '';
}

function previewDocument(doc) {
  toast.value = `Preview requested for ${doc.name}.`;
}

function downloadDocument(doc) {
  toast.value = `Download requested for ${doc.name}.`;
}

function removeDocument(id) {
  documents.value = documents.value.filter((doc) => doc.id !== id);
  toast.value = 'Document deleted.';
}
</script>

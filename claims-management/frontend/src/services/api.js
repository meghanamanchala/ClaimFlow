import axios from 'axios';

function resolveApiBaseUrl() {
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }

  if (typeof window !== 'undefined') {
    const host = window.location.hostname;
    if (host === 'localhost' || host === '127.0.0.1') {
      return 'http://127.0.0.1:8000';
    }
  }

  return 'https://claimflow-uhsl.onrender.com';
}

const api = axios.create({
  baseURL: resolveApiBaseUrl()
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('claimflow_token');

  if (token) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export async function registerUser(payload) {
  return api.post('/register', payload);
}

export async function loginUser(email, password) {
  const body = new URLSearchParams();
  body.append('username', email);
  body.append('password', password);

  return api.post('/login', body, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  });
}

export async function getMe() {
  return api.get('/me');
}

export async function updateMe(payload) {
  return api.put('/me', payload);
}

export async function getPolicies() {
  return api.get('/policies');
}

export async function getClaims() {
  return api.get('/claims');
}

export async function getClaimById(claimId) {
  return api.get(`/claims/${claimId}`);
}

export async function getClaimTracking(claimId) {
  return api.get(`/claims/${claimId}/tracking`);
}

export async function createClaim(payload) {
  return api.post('/claims', payload);
}

export async function uploadClaimDocument(claimId, payload) {
  return api.post(`/claims/${claimId}/documents`, payload);
}

export async function uploadClaimDocumentFile(claimId, file) {
  const formData = new FormData();
  formData.append('file', file);

  return api.post(`/claims/${claimId}/documents/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

export async function deleteClaimDocument(claimId, params) {
  return api.delete(`/claims/${claimId}/documents`, { params });
}

export async function getUsers() {
  return api.get('/users');
}

export async function updateUserStatus(userId, status) {
  return api.patch(`/admin/users/${userId}/status`, { status });
}

export async function updateClaimDecision(claimId, payload) {
  return api.patch(`/claims/${claimId}/decision`, payload);
}

export async function getMessages(params = {}) {
  return api.get('/messages', { params });
}

export async function createMessage(payload) {
  return api.post('/messages', payload);
}

export async function getAdminPermissions() {
  return api.get('/admin/permissions');
}

export async function updateAdminPermissions(payload) {
  return api.put('/admin/permissions', payload);
}

export async function getAdminSettings() {
  return api.get('/admin/settings');
}

export async function updateAdminSettings(payload) {
  return api.put('/admin/settings', payload);
}

export default api;

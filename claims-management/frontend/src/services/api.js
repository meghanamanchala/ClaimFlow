import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
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

export default api;

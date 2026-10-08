import axios from 'axios';

const api = axios.create({ baseURL: import.meta.env.VITE_API_URL });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  const isAuthRoute = config.url === '/login/' || config.url === '/register/';
  if (token && !isAuthRoute) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export default api;
import axios from 'axios';
import { User, KnowledgeEntry, MarketListing } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://backend:5001/';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  register: (userData: any) => api.post('/auth/register', userData),
  login: (credentials: any) => api.post('/auth/login', credentials),
  getProfile: () => api.get('/auth/profile'),
};

export const knowledgeAPI = {
  getAll: (): Promise<{data: KnowledgeEntry[]}> => api.get('/knowledge/'),
  create: (data: any) => api.post('/knowledge/', data),
  getById: (id: number) => api.get(`/knowledge/${id}`),
};

export const marketAPI = {
  getAll: (): Promise<{data: MarketListing[]}> => api.get('/market/'),
  create: (data: any) => api.post('/market/', data),
};

export default api;
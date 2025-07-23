import axios from 'axios';

// Create axios instance with base URL and default headers
const api = axios.create({
  baseURL: 'http://135.222.41.13:5001/api', // Updated port to match backend
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include JWT token in headers if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Authentication APIs
// export const register = (userData) => api.post('/auth/register', userData);
// export const login = (credentials) => api.post('/auth/login', credentials);
// export const getProfile = () => api.get('/auth/profile');

// // Knowledge APIs
// export const getKnowledgeEntries = () => api.get('/knowledge');
// export const createKnowledgeEntry = (entryData) => api.post('/knowledge', entryData);

// // Market APIs
// export const getMarketListings = (availableOnly = true) => 
//   api.get(`/market?available_only=${availableOnly}`);
// export const createMarketListing = (listingData) => api.post('/market', listingData);

export default api;
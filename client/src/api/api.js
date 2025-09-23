import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});

// --- AUTH ---
export const login = (credentials) => api.post('/login', credentials).then(res => res.data);
export const signup = (userData) => api.post('/signup', userData).then(res => res.data);

// --- NGO ---
export const getNGOCredits = () => api.get('/NGO/credits').then(res => res.data);
export const createNGOCredit = (creditData) => api.post('/NGO/credits', creditData).then(res => res.data);
export const getTransactions = () => api.get('/NGO/transactions').then(res => res.data);
export const expireCreditApi = (expireCreditId) => api.patch(`/NGO/credits/expire/${expireCreditId}`).then(res => res.data);
export const verifyBeforeExpire = (verificationData) => api.post(`/NGO/expire-req`, verificationData).then(res => res.data);
export const checkAuditorsNumber = (amount) => api.get(`/NGO/audit-req`, { params: { amount } }).then(res => res.data);

// --- BUYER ---
export const getBuyerCredits = () => api.get('/buyer/credits').then(res => res.data);
export const purchaseCredit = (purchaseData) => api.post('/buyer/purchase', purchaseData).then(res => res.data);
export const sellCreditApi = (sellData) => api.patch('/buyer/sell', sellData).then(res => res.data);
export const removeSaleCreditApi = (removeData) => api.patch('/buyer/remove-from-sale', removeData).then(res => res.data);
export const getPurchasedCredits = () => api.get('/buyer/purchased').then(res => res.data);
export const generateCertificate = (creditId) => api.get(`/buyer/generate-certificate/${creditId}`).then(res => res.data);
export const downloadCertificate = (creditId) => api.get(`/buyer/download-certificate/${creditId}`).then(res => res.data);
export const getCreditDetailsAPI = (creditId) => api.get(`/buyer/credits/${creditId}`).then(res => res.data);

// --- AUDITOR ---
export const getAssignedCredits = () => api.get('/auditor/credits').then(res => res.data);
export const auditCreditApi = (auditData) => api.patch(`/auditor/audit/${auditData["creditId"]}`, auditData).then(res => res.data);

export default api;

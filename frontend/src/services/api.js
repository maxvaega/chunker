import axios from 'axios';

// Crea un'istanza di axios con l'URL di base del backend
const api = axios.create({
  baseURL: process.env.REACT_APP_BACKEND_URL, // URL del backend definito nelle variabili d’ambiente
});

// Intercetta le richieste per aggiungere l'header Authorization
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token'); // Recupera il token dal localStorage
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`; // Aggiunge il token all'header
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
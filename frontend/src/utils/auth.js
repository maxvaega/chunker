/frontend/src/utils/auth.js
// Funzione per ottenere il token dal localStorage
export const getToken = () => {
  return localStorage.getItem('token');
};

// Funzione per rimuovere il token (es. durante il logout)
export const removeToken = () => {
  localStorage.removeItem('token');
};
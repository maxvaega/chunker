import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api.js';
import ErrorAlert from './ErrorAlert.jsx';

const Login = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/auth/login', { username, password });
      localStorage.setItem('token', response.data.token); // Salva il token
      navigate('/dashboard'); // Reindirizza alla dashboard
    } catch (err) {
      setError(err.response?.data?.message || 'Errore di autenticazione');
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      {error && <ErrorAlert message={error} />} {/* Mostra errore se presente */}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username:</label>
          <input 
            type="text" 
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
            required 
          />
        </div>
        <div>
          <label>Password:</label>
          <input 
            type="password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required 
          />
        </div>
        <button type="submit">Accedi</button>
      </form>
    </div>
  );
};

export default Login;
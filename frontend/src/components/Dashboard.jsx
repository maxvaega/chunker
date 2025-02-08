import React, { useState } from 'react';
import api from '../services/api.js';
import ErrorAlert from './ErrorAlert.jsx';

const Dashboard = () => {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Nessun file selezionato');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      setStatus('Caricamento in corso...');
      const response = await api.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setStatus('File caricato con successo');
    } catch (err) {
      setError(err.response?.data?.message || 'Errore nel caricamento del file');
      setStatus('');
    }
  };

  return (
    <div className="dashboard-container">
      <h2>Dashboard</h2>
      {error && <ErrorAlert message={error} />} {/* Mostra errore se presente */}
      <div>
        <input type="file" accept=".md" onChange={handleFileChange} />
        <button onClick={handleUpload}>Carica File Markdown</button>
      </div>
      {status && <p>{status}</p>} {/* Mostra lo stato delle operazioni */}
    </div>
  );
};

export default Dashboard;
import React from 'react';

const ErrorAlert = ({ message }) => {
  return (
    <div className="error-alert">
      <p>{message}</p>
    </div>
  );
};

export default ErrorAlert;
import React from 'react';
import './Welcome.css';

const Welcome = () => {
  return (
    <div className="welcome-container">
      <header className="main-header">
        <h1>Boas vindas, Dr. Amelia Harper</h1>
        <p>Você está conectado como Professor. Use o menu à esquerda para gerenciar sua agenda.</p>
      </header>
    </div>
  );
};

export default Welcome;
// src/components/Card.js
import React from 'react';

const Card = ({ title, content, onClose }) => {
  return (
    <div className="card">
      <div className="card-header">
        <h2>{title}</h2>
        <button onClick={onClose}>Закрыть</button>
      </div>
      <div className="card-content">
        {content}
      </div>
    </div>
  );
};

export default Card;
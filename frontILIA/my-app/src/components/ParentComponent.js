// src/components/ParentComponent.js
import React, { useState } from 'react';
import Card from './Card';
import Modal from './Modal';

const ParentComponent = () => {
  const [isCardVisible, setCardVisible] = useState(false);

  const handleClick = () => {
    setCardVisible(true);
  };

  const handleClose = () => {
    setCardVisible(false);
  };

  return (
    <div>
      <button onClick={handleClick}>Показать карточку</button>

      {isCardVisible && (
        <Modal onClose={handleClose}>
          <Card
            title="Заголовок карточки"
            content="Содержимое карточки"
            onClose={handleClose}
          />
        </Modal>
      )}
    </div>
  );
};

export default ParentComponent;
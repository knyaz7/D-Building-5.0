// src/components/MoveTaskModal.js
import React from 'react';
import './TaskModal.css'; // Импорт стилей

const MoveTaskModal = ({ task, onClose, onMoveTask }) => {
  const columns = ['To Do', 'In Progress', 'Done'];

  const handleMove = (newStatus) => {
    onMoveTask(task.id, newStatus);
    onClose();
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Переместить задачу "{task.title}"</h2>
        <ul>
          {columns.map((status) => (
            <li key={status}>
              <button onClick={() => handleMove(status)}>{status}</button>
            </li>
          ))}
        </ul>
        <button onClick={onClose}>Закрыть</button>
      </div>
    </div>
  );
};

export default MoveTaskModal;
// src/components/TaskView.js
import React from 'react';

const TaskView = ({ task, onEdit, onDelete, onClose }) => {
  return (
    <div className="modal-content">
      <h2>{task.title}</h2>
      <p>{task.body}</p>
      <p>Исполнитель: {task.assignee}</p>
      <p>Статус: {task.status}</p>
      <div>
        <h3>Меню задачи:</h3>
        <ul>
          {task.menu.map((action, index) => (
            <li key={index}>{action}</li>
          ))}
        </ul>
      </div>
      <button onClick={onEdit}>Редактировать</button>
      <button onClick={onDelete}>Удалить задачу</button>
      <button onClick={onClose}>Закрыть</button>
    </div>
  );
};

export default TaskView;
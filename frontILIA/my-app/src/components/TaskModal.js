// src/components/TaskModal.js
import React, { useState } from 'react';
import TaskView from './TaskView';
import TaskEdit from './TaskEdit';
import './TaskModal.css'; // Импорт стилей

const TaskModal = ({ task, onClose, onUpdateTask, onDeleteTask }) => {
  const [isEditing, setIsEditing] = useState(false);

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleSave = (updatedTask) => {
    onUpdateTask(updatedTask);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setIsEditing(false);
  };

  if (!task) return null;

  return (
    <div className="modal-overlay">
      {isEditing ? (
        <TaskEdit task={task} onSave={handleSave} onCancel={handleCancel} />
      ) : (
        <TaskView
          task={task}
          onEdit={handleEdit}
          onDelete={() => {
            onDeleteTask(task.id);
            onClose();
          }}
          onClose={onClose}
        />
      )}
    </div>
  );
};

export default TaskModal;
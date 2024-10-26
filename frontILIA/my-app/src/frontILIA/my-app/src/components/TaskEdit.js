// src/components/TaskEdit.js
import React, { useState } from 'react';

const TaskEdit = ({ task, onSave, onCancel }) => {
  const [title, setTitle] = useState(task.title);
  const [body, setBody] = useState(task.body);

  const handleTitleChange = (e) => {
    setTitle(e.target.value);
  };

  const handleBodyChange = (e) => {
    setBody(e.target.value);
  };

  const handleSave = () => {
    onSave({ ...task, title, body });
  };

  return (
    <div className="modal-content">
      <input type="text" value={title} onChange={handleTitleChange} />
      <textarea value={body} onChange={handleBodyChange} />
      <p>Исполнитель: {task.assignee}</p>
      <p>Статус: {task.status}</p>
      <button onClick={handleSave}>Сохранить</button>
      <button onClick={onCancel}>Отмена</button>
    </div>
  );
};

export default TaskEdit;
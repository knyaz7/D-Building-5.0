// src/components/TaskBoard.js
import React, { useRef, useState } from 'react';
import './TaskBoard.css'; // Импорт стилей
import { updateTaskStatus } from '../api';

const TaskBoard = ({ tasks, onDeleteTask, onOpenTask, onMoveTask }) => {
  const columns = {
    todo: 'To Do',
    todo_suka: 'To Do Faster',
    inProgress: 'In Progress',
    testing: 'Testing',
    done: 'Done',
  };

  const getTasksByStatus = (status) => {
    return tasks.filter((task) => task.status === status);
  };

  const [draggedTask, setDraggedTask] = useState(null);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleMouseDown = (e, task) => {
    const taskElement = e.currentTarget;
    const rect = taskElement.getBoundingClientRect();
    const offsetX = e.clientX - rect.left;
    const offsetY = e.clientY - rect.top;

    setDraggedTask(task);
    setDragOffset({ x: offsetX, y: offsetY });
    setIsDragging(true);
  };

  const handleMouseMove = (e) => {
    if (!isDragging || !draggedTask) return;

    const taskElement = document.getElementById(`task-${draggedTask.id}`);
    if (taskElement) {
      taskElement.style.position = 'absolute';
      taskElement.style.left = `${e.clientX - dragOffset.x}px`;
      taskElement.style.top = `${e.clientY - dragOffset.y}px`;
      taskElement.classList.add('dragging');
    }
  };

  const handleMouseUp = async (e) => {
    if (!isDragging || !draggedTask) return;

    const column = e.target.closest('.column');
    if (column) {
      const status = column.getAttribute('data-status');
      setIsLoading(true);
      try {
        await updateTaskStatus(draggedTask.id, status);
        onMoveTask(draggedTask.id, status);
      } catch (error) {
        console.error('Failed to update task status:', error);
      } finally {
        setIsLoading(false);
      }
    }

    const taskElement = document.getElementById(`task-${draggedTask.id}`);
    if (taskElement) {
      taskElement.classList.remove('dragging');
      taskElement.style.position = 'static';
    }

    setDraggedTask(null);
    setIsDragging(false);
  };

  return (
    <div
      className="task-board"
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
    >
      {Object.keys(columns).map((status) => (
        <div
          key={status}
          className="column"
          data-status={status}
        >
          <h2>{columns[status]}</h2>
          <ul>
            {getTasksByStatus(status).map((task) => (
              <li
                key={task.id}
                id={`task-${task.id}`}
                className="task"
                onMouseDown={(e) => handleMouseDown(e, task)}
              >
                <h3>{task.title}</h3>
                <p>Исполнитель: {task.assignee}</p>
                <div>
                  <button onClick={() => onOpenTask(task.id)}>Открыть</button>
                  <button onClick={() => onDeleteTask(task.id)}>Удалить</button>
                </div>
              </li>
            ))}
          </ul>
        </div>
      ))}
      {isLoading && <div className="loading-indicator">Перемещение задачи...</div>}
    </div>
  );
};

export default TaskBoard;
// src/components/TaskBoard.js
import React, { useState, useEffect } from 'react';
import './TaskBoard.css';
import { updateTaskStatus, GetTasks } from '../api';

const TaskBoard = ({ onDeleteTask, onOpenTask, onMoveTask }) => {
  const columns = {
    todo: 'To Do',
    todo_suka: 'To Do Faster',
    inProgress: 'In Progress',
    testing: 'Testing',
    done: 'Done',
  };

  const [tasks, setTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchTasks = async () => {
      setIsLoading(true);
      try {
        const stagesData = await GetTasks();
        const loadedTasks = stagesData.flatMap(stage => stage.tasks); // Извлечение всех задач
        setTasks(loadedTasks);
      } catch (error) {
        console.error('Ошибка при загрузке задач:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchTasks();
  }, []);

  // Остальной код компонента

  return (
    <div className="task-board">
      {isLoading ? (
        <div className="loading-indicator">Загрузка задач...</div>
      ) : (
        Object.keys(columns).map((status) => (
          <div key={status} className="column" data-status={status}>
            <h2>{columns[status]}</h2>
            <ul>
              {tasks
                .filter(task => task.status === status)
                .map(task => (
                  <li key={task.id} className="task">
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
        ))
      )}
    </div>
  );
};

export default TaskBoard;
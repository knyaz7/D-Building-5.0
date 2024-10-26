// src/App.js
import React, { useState, useEffect } from 'react';
import TaskBoard from './components/TaskBoard';
import TaskModal from './components/TaskModal';
import tasksData from './data/tasks';
import { updateTaskStatus } from './api';

function App() {
  const [tasks, setTasks] = useState(tasksData);
  const [selectedTask, setSelectedTask] = useState(null);

  const handleDeleteTask = (taskId) => {
    const updatedTasks = tasks.filter((task) => task.id !== taskId);
    setTasks(updatedTasks);
  };

  const handleOpenTask = (taskId) => {
    const task = tasks.find((task) => task.id === taskId);
    setSelectedTask(task);
  };

  const handleCloseModal = () => {
    setSelectedTask(null);
  };

  const handleUpdateTask = (updatedTask) => {
    const updatedTasks = tasks.map((task) =>
      task.id === updatedTask.id ? updatedTask : task
    );
    setTasks(updatedTasks);
    setSelectedTask(updatedTask);
  };

  const handleMoveTask = async (taskId, newStatus) => {
    try {
      await updateTaskStatus(taskId, newStatus);
      const updatedTasks = tasks.map((task) =>
        task.id === taskId ? { ...task, status: newStatus } : task
      );
      setTasks(updatedTasks);
    } catch (error) {
      console.error('Failed to update task status:', error);
    }
  };

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await fetch('/api/tasks');
        if (!response.ok) {
          throw new Error('Failed to fetch tasks');
        }
        const data = await response.json();
        setTasks(data);
      } catch (error) {
        console.error('Failed to fetch tasks:', error);
      }
    };

    fetchTasks();
  }, []);

  return (
    <div>
      <TaskBoard
        tasks={tasks}
        onDeleteTask={handleDeleteTask}
        onOpenTask={handleOpenTask}
        onMoveTask={handleMoveTask}
      />
      <TaskModal
        task={selectedTask}
        onClose={handleCloseModal}
        onUpdateTask={handleUpdateTask}
        onDeleteTask={handleDeleteTask}
      />
    </div>
  );
}

export default App;
// src/api.js


import axios from 'axios';

export const updateTaskStatus = async (taskId, FirstColumnId, SecondColumnId) => {
  try {
    const response = await fetch(`http://localhost:8000/api/v1/tasks/${taskId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InN0cmluZyIsImV4cCI6MTcyOTk2NDc5Nn0.hcq43DSk8FycbLcuXCHlffSmGvcJSvsWzoZy1n4abdU',
      },
      body: JSON.stringify(),
    });

    if (!response.ok) {
      throw new Error('Failed to update task');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
    throw error;
  }
};



const API_BASE_URL = 'http://localhost:8000/api/v1'; // Базовый URL

// Функция для получения задач по этапам
export const GetTasks = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/stages/`, {
      headers: {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InN0cmluZyIsImV4cCI6MTcyOTk3NDQ4MH0.MpE5o055E5lg5W9THSeIONu3_9584PFo8bApmFFL0FQ'
      }
    });
    return response.data; // Возвращаем данные этапов с задачами
  } catch (error) {
    console.error('Ошибка при получении задач:', error);
    throw error; // Перебрасываем ошибку для обработки в вызывающем коде
  }
};
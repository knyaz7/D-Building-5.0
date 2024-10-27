// src/api.js

import axiosInstance from '../../../axiosInstance.js';


// Функция для обновления статуса задачи
export const updateTaskStatus = async (taskId, FirstColumnId, SecondColumnId) => {
  try {
    const response = await axiosInstance.patch(`/stages/moves_task/${taskId}`, {
      from_stage_id: FirstColumnId,
      to_stage_id: SecondColumnId,
    });

    return response.data;
  } catch (error) {
    console.error('Ошибка при обновлении статуса задачи:', error);
    throw error;
  }
};

// Функция для получения задач по этапам
export const GetTasks = async () => {
  try {
    const response = await axiosInstance.get('/stages/');
    return response.data;
  } catch (error) {
    console.error('Ошибка при получении задач:', error);
    throw error;
  }
};
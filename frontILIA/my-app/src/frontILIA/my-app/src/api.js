// src/api.js
export const updateTaskStatus = async (taskId, FirstColumnId, SecondColumnId) => {
  try {
    const response = await fetch(`http://localhost:8000/api/v1/tasks/${taskId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InN0cmluZyIsImV4cCI6MTcyOTk2NDc5Nn0.hcq43DSk8FycbLcuXCHlffSmGvcJSvsWzoZy1n4abdU',
      },
      body: JSON.stringify(updateData),
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
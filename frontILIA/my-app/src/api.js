// src/api.js
export const updateTaskStatus = async (taskId, newStatus) => {
    try {
      const response = await fetch(`/api/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus }),
      });
  
      if (!response.ok) {
        throw new Error('Failed to update task status');
      }
  
      const data = await response.json();
      return data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  };
import React, { useEffect, useState } from "react";
import ProjectCard from "./ProjectCard";
import "./AdminPanel.css";
import womanAvatar1 from "./woman-avatar-1.png";


import axiosInstance from './axiosInstance'; 


// Функция для получения задач
export const getMasterTasks = async () => {
  try {
    const response = await axiosInstance.get(`/master_tasks/`); // Используем axiosInstance
    return response.data; // Возвращаем данные
  } catch (error) {
    console.error('Ошибка при получении задач:', error); // Логируем ошибку
    throw error; // Перебрасываем ошибку
  }
};

const AdminPanel = () => {
  const [projects, setProjects] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const data = await getMasterTasks();
        // Преобразуем данные из API в формат, подходящий для отображения
        const formattedProjects = data.map(task => ({
          name: task.name,
          peopleCount: task.tasks.length,
          createdAt: task.created_at,
          deadline: task.deadline
        }));
        setProjects(formattedProjects);
      } catch (error) {
        console.error('Ошибка при загрузке проектов:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProjects();
  }, []);

  return (
    <div className="admin-panel">
      <div className="sidebar">
        <div className="component-2">
          <div className="vertical-line"></div>
          <div className="vertical-line"></div>
          <div className="vertical-line"></div>
        </div>
      </div>
      <div className="main-content">
        <div className="header">
          <div className="user-info">
            <img className="woman-avatar" alt="Woman avatar" src={womanAvatar1} />
            <div className="text-wrapper-2">Admin</div>
          </div>
          <button className="add-project-button">Добавить проект</button>
        </div>
        <div className="projects-list">
          {isLoading ? (
            <div>Загрузка проектов...</div>
          ) : (
            projects.map((project, index) => (
              <ProjectCard key={index} project={project} />
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminPanel;

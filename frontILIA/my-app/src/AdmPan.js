import React from "react";
import ProjectCard from "./ProjectCard";
import "./AdminPanel.css";
import womanAvatar1 from "./woman-avatar-1.png";

const projects = [
    { name: "Project_1", peopleCount: 5 },
    { name: "Project_2", peopleCount: 10 },
    { name: "Project_3", peopleCount: 8 },
];

export default () => {
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
                        <img
                            className="woman-avatar"
                            alt="Woman avatar"
                            src={womanAvatar1}
                        />
                        <div className="text-wrapper-2">Admin</div>
                    </div>
                    <button className="add-project-button">Добавить проект</button>
                </div>
                <div className="projects-list">
                    {projects.map((project, index) => (
                        <ProjectCard key={index} project={project} />
                    ))}
                </div>
            </div>
        </div>
    );
};
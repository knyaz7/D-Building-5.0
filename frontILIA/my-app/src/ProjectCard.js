import React from "react";

const ProjectCard = ({ project }) => {
    return (
        <div className="project-card">
            <div className="project-name">{project.name}</div>
            <div className="project-details">
                <div className="detail-label">количество человек:</div>
                <div className="detail-value">{project.peopleCount}</div>
                <button className="go-button">перейти</button>
            </div>
        </div>
    );
};

export default ProjectCard;